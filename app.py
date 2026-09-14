import os
import sys
import json
import uuid
import logging
import threading
import traceback
import inspect
from datetime import datetime

from flask import Flask, render_template, request, jsonify, abort


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
CHATS_FILE = os.path.join(BASE_DIR, "chats.json")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

os.makedirs(UPLOAD_DIR, exist_ok=True)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


BINEURON_IMPORT_ERROR = None
try:
    from BiNeuron import BiNeuron
    from BiNeuron.data.constants_for_functions import (
        HTTP_PROTOCOL, HTTPS_PROTOCOL, TYPES_POWER,
        PREFERENCES_IN_AI_LIST, DETERMINANT_MODE_LIST,
    )
    from BiNeuron.data.variants_industrial_scenarios import ALL_MAIN_PROMPTS
except Exception as e:
    BINEURON_IMPORT_ERROR = f"{type(e).__name__}: {e}"
    HTTP_PROTOCOL, HTTPS_PROTOCOL = "http", "https"
    TYPES_POWER = ["easy", "middle", "hard", "very_hard"]
    PREFERENCES_IN_AI_LIST = ["deepseek", "qwen", "llama"]
    DETERMINANT_MODE_LIST = ["lite", "full", "auto"]
    ALL_MAIN_PROMPTS = {"default": "You are a helpful assistant."}


def _wrap_init_with_kwargs_filter(cls, logger):
    orig_init = cls.__init__
    try:
        sig = inspect.signature(orig_init)
    except (TypeError, ValueError):
        return
    params = sig.parameters
    has_var_kw = any(p.kind == inspect.Parameter.VAR_KEYWORD
                     for p in params.values())
    if has_var_kw:
        return
    allowed = set(params.keys())

    def _patched_init(self, *args, **kwargs):
        dropped = [k for k in list(kwargs) if k not in allowed]
        for k in dropped:
            kwargs.pop(k, None)
        if dropped:
            logger.info(
                f"[compat] {cls.__name__}: dropped unsupported kwargs -> {dropped}"
            )
        return orig_init(self, *args, **kwargs)

    _patched_init.__wrapped__ = orig_init
    cls.__init__ = _patched_init
    print(f"[compat] {cls.__name__} patched")


def _apply_bineuron_compat_patches():
    logger = logging.getLogger(__name__)
    try:
        from BiNeuron.additional_functions.defining_programming_language import (
            DefiningProgrammingLanguage,
        )
    except Exception as e:
        print(f"[compat] DefiningProgrammingLanguage not found: {e}")
    else:
        _wrap_init_with_kwargs_filter(DefiningProgrammingLanguage, logger)

    for mod_name, cls_name in (
        ("BiNeuron.additional_functions.text_translation", "TranslatorText"),
    ):
        try:
            mod = __import__(mod_name, fromlist=[cls_name])
            cls = getattr(mod, cls_name)
            _wrap_init_with_kwargs_filter(cls, logger)
        except Exception:
            pass


_apply_bineuron_compat_patches()


app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["MAX_CONTENT_LENGTH"] = 512 * 1024 * 1024


class TaskManager:
    def __init__(self, max_tasks: int = 200):
        self._tasks = {}
        self._order = []
        self._lock = threading.Lock()
        self._max = max_tasks

    def create(self) -> str:
        tid = uuid.uuid4().hex
        with self._lock:
            self._tasks[tid] = {
                "status": "running",
                "logs": [],
                "answer": None,
                "error": None,
                "created_at": datetime.now().isoformat(),
            }
            self._order.append(tid)
            while len(self._order) > self._max:
                self._tasks.pop(self._order.pop(0), None)
        return tid

    def log(self, tid: str, msg: str):
        with self._lock:
            t = self._tasks.get(tid)
            if t is not None:
                t["logs"].append(msg)
                if len(t["logs"]) > 4000:
                    t["logs"] = t["logs"][-4000:]

    def finish(self, tid: str, answer: str):
        with self._lock:
            t = self._tasks.get(tid)
            if t is not None:
                t["status"] = "done"
                t["answer"] = answer

    def fail(self, tid: str, error: str):
        with self._lock:
            t = self._tasks.get(tid)
            if t is not None:
                t["status"] = "error"
                t["error"] = error

    def get(self, tid: str, since: int = 0):
        with self._lock:
            t = self._tasks.get(tid)
            if t is None:
                return None
            return {
                "status": t["status"],
                "answer": t["answer"],
                "error": t["error"],
                "logs": t["logs"][since:],
                "log_count": len(t["logs"]),
            }


task_manager = TaskManager()
_task_lock = threading.Lock()


class TaskLogHandler(logging.Handler):
    def __init__(self, tm: TaskManager, tid: str):
        super().__init__()
        self.tm = tm
        self.tid = tid

    def emit(self, record):
        try:
            self.tm.log(self.tid, self.format(record))
        except Exception:
            pass


class _StdStreamCapture:
    def __init__(self, tm: TaskManager, tid: str, original):
        self.tm = tm
        self.tid = tid
        self.original = original
        self.buffer = ""

    def write(self, s):
        if self.original is not None:
            try:
                self.original.write(s)
                self.original.flush()
            except Exception:
                pass
        if not s:
            return
        self.buffer += s
        while True:
            idx_n = self.buffer.find("\n")
            idx_r = self.buffer.find("\r")
            positions = [i for i in (idx_n, idx_r) if i >= 0]
            if not positions:
                break
            idx = min(positions)
            line = self.buffer[:idx]
            self.buffer = self.buffer[idx + 1:]
            if line.strip():
                self.tm.log(self.tid, line)

    def flush(self):
        if self.original is not None:
            try:
                self.original.flush()
            except Exception:
                pass
        if self.buffer.strip():
            self.tm.log(self.tid, self.buffer)
            self.buffer = ""

    def isatty(self):
        return True

    def fileno(self):
        if self.original is not None:
            try:
                return self.original.fileno()
            except Exception:
                pass
        raise OSError("fileno not available")


def _to_int(v, default=None):
    if v in (None, ""):
        return default
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return default


def _to_float(v, default=0.1):
    if v in (None, ""):
        return default
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def _to_bool(v):
    if isinstance(v, bool):
        return v
    if v is None:
        return False
    return str(v).strip().lower() in ("1", "true", "yes", "on")


def _to_list(v):
    if not v:
        return None
    if isinstance(v, list):
        items = [str(x).strip() for x in v if str(x).strip()]
        return items or None
    items = [line.strip() for line in str(v).splitlines() if line.strip()]
    return items or None


def parse_settings_for_bineuron(data: dict) -> dict:
    return {
        "preferences_in_ai": data.get("preferences_in_ai") or PREFERENCES_IN_AI_LIST[0],
        "filter_for_swearing": _to_bool(data.get("filter_for_swearing")),
        "models_dir": (data.get("models_dir") or "./models").strip(),
        "with_ai_orchestrator": _to_bool(data.get("with_ai_orchestrator", True)),
        "verbose": _to_bool(data.get("verbose")),
        "n_ctx": _to_int(data.get("n_ctx")),
        "n_gpu_layers": _to_int(data.get("n_gpu_layers"), 0),
        "echo": _to_bool(data.get("echo")),
        "max_tokens": _to_int(data.get("max_tokens"), 4096),
        "your_token_for_hf": data.get("your_token_for_hf") or None,
        "subdomain": data.get("subdomain") or "",
        "country": data.get("country") or None,
        "protocol": data.get("protocol") or HTTP_PROTOCOL,
        "max_timeout": _to_int(data.get("max_timeout"), 30),
        "is_working": _to_bool(data.get("is_working")),
        "type_computer": (data.get("type_computer")
                          if data.get("type_computer") not in (None, "", "auto")
                          else None),
        "auto_proxies": _to_bool(data.get("auto_proxies")),
        "writing_response_to_file": _to_bool(data.get("writing_response_to_file")),
        "your_proxies_dict": _to_list(data.get("your_proxies_dict")),
        "determinant_mode": data.get("determinant_mode") or "auto",
        "accurate_translation": _to_bool(data.get("accurate_translation")),
        "your_key_for_deepl": data.get("your_key_for_deepl") or "",
        "proprietary_algorithms": _to_bool(data.get("proprietary_algorithms")),
        "repo_id": data.get("repo_id") or None,
        "filename": data.get("filename") or None,
        "min_timeout_for_checking_availability":
            _to_int(data.get("min_timeout_for_checking_availability"), 5),
        "max_timeout_for_checking_availability":
            _to_int(data.get("max_timeout_for_checking_availability"), 15),
        "request_language": data.get("request_language") or "en",
        "main_prompt_mode": data.get("main_prompt_mode") or "default",
        "main_prompt": data.get("main_prompt") or None,
        "temperature": _to_float(data.get("temperature"), 0.1),
        "retries": _to_int(data.get("retries"), 3),
        "github_proxies": _to_bool(data.get("github_proxies")),
        "url_lst": _to_list(data.get("url_lst")),
        "proxy_retries": _to_int(data.get("proxy_retries"), 3),
        "main_retries": _to_int(data.get("main_retries"), 3),
        "lang_lst": _to_list(data.get("lang_lst")),
        "use_gpu_for_ocr": _to_bool(data.get("use_gpu_for_ocr")),
        "virtual_storage": _to_bool(data.get("virtual_storage")),
        "virtual_storage_path": data.get("virtual_storage_path") or None,
        "with_ocr": _to_bool(data.get("with_ocr")),
        "cloud_version": _to_bool(data.get("cloud_version")),
        "with_deepseek": _to_bool(data.get("with_deepseek", True)),
        "model_size": data.get("model_size") or "tiny",
        "crop_mode": _to_bool(data.get("crop_mode")),
        "base_url": data.get("base_url")
                    or "https://api.siliconflow.cn/v1/chat/completions",
        "api_key_for_deepseek_ocr": data.get("api_key_for_deepseek_ocr") or None,
        "timeout_for_deepseek_ocr": _to_int(data.get("timeout_for_deepseek_ocr")),
        "max_rate_limit_retries": _to_int(data.get("max_rate_limit_retries"), 3),
        "prefer_mirror": _to_bool(data.get("prefer_mirror", True)),
        "editing_files": _to_bool(data.get("editing_files")),
    }


def default_settings() -> dict:
    return {
        "preferences_in_ai": PREFERENCES_IN_AI_LIST[0] if PREFERENCES_IN_AI_LIST else "deepseek",
        "filter_for_swearing": False,
        "models_dir": "./models",
        "with_ai_orchestrator": True,
        "verbose": False,
        "n_ctx": 0,
        "n_gpu_layers": 0,
        "echo": False,
        "max_tokens": 4096,
        "your_token_for_hf": "",
        "subdomain": "",
        "country": "",
        "protocol": HTTP_PROTOCOL,
        "max_timeout": 30,
        "is_working": False,
        "type_computer": "auto",
        "auto_proxies": False,
        "writing_response_to_file": False,
        "your_proxies_dict": "",
        "determinant_mode": DETERMINANT_MODE_LIST[0] if DETERMINANT_MODE_LIST else "auto",
        "accurate_translation": False,
        "your_key_for_deepl": "",
        "proprietary_algorithms": False,
        "repo_id": "",
        "filename": "",
        "min_timeout_for_checking_availability": 5,
        "max_timeout_for_checking_availability": 15,
        "request_language": "en",
        "main_prompt_mode": (list(ALL_MAIN_PROMPTS.keys())[0]
                             if ALL_MAIN_PROMPTS else "default"),
        "main_prompt": "",
        "temperature": 0.1,
        "retries": 3,
        "github_proxies": False,
        "url_lst": "",
        "proxy_retries": 3,
        "main_retries": 3,
        "lang_lst": "",
        "use_gpu_for_ocr": False,
        "virtual_storage": False,
        "virtual_storage_path": "",
        "with_ocr": False,
        "cloud_version": False,
        "with_deepseek": True,
        "model_size": "tiny",
        "crop_mode": False,
        "base_url": "https://api.siliconflow.cn/v1/chat/completions",
        "api_key_for_deepseek_ocr": "",
        "timeout_for_deepseek_ocr": 30,
        "max_rate_limit_retries": 3,
        "prefer_mirror": True,
        "editing_files": False,
    }


def load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"Failed to save {path}: {e}")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/meta")
def api_meta():
    return jsonify({
        "protocols": [HTTP_PROTOCOL, HTTPS_PROTOCOL],
        "types_power": TYPES_POWER,
        "preferences_in_ai": PREFERENCES_IN_AI_LIST,
        "determinant_modes": DETERMINANT_MODE_LIST,
        "main_prompt_modes": list(ALL_MAIN_PROMPTS.keys()),
        "model_sizes": ["tiny", "small", "base", "large", "gundam"],
        "import_error": BINEURON_IMPORT_ERROR,
    })


@app.route("/api/settings", methods=["GET"])
def api_get_settings():
    data = load_json(SETTINGS_FILE, None)
    return jsonify(data if data is not None else default_settings())


@app.route("/api/settings", methods=["POST"])
def api_save_settings():
    save_json(SETTINGS_FILE, request.get_json(silent=True) or {})
    return jsonify({"ok": True})


@app.route("/api/settings/reset", methods=["POST"])
def api_reset_settings():
    data = default_settings()
    save_json(SETTINGS_FILE, data)
    return jsonify({"ok": True, "settings": data})


@app.route("/api/chats", methods=["GET"])
def api_list_chats():
    return jsonify(load_json(CHATS_FILE, {}))


@app.route("/api/chats", methods=["POST"])
def api_create_chat():
    chats = load_json(CHATS_FILE, {})
    new_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
    chats[new_id] = {
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "messages": [],
    }
    save_json(CHATS_FILE, chats)
    return jsonify({"id": new_id, "chat": chats[new_id]})


@app.route("/api/chats/<chat_id>", methods=["GET"])
def api_get_chat(chat_id):
    chats = load_json(CHATS_FILE, {})
    if chat_id not in chats:
        abort(404)
    return jsonify(chats[chat_id])


@app.route("/api/chats/<chat_id>", methods=["DELETE"])
def api_delete_chat(chat_id):
    chats = load_json(CHATS_FILE, {})
    chats.pop(chat_id, None)
    save_json(CHATS_FILE, chats)
    return jsonify({"ok": True})


@app.route("/api/chats/<chat_id>/messages", methods=["POST"])
def api_append_message(chat_id):
    body = request.get_json(silent=True) or {}
    role = body.get("role")
    if role not in ("user", "assistant", "system"):
        abort(400)
    chats = load_json(CHATS_FILE, {})
    chats.setdefault(chat_id, {
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "messages": [],
    })
    chats[chat_id]["messages"].append({
        "role": role,
        "content": body.get("content", ""),
        "timestamp": datetime.now().strftime("%H:%M"),
    })
    save_json(CHATS_FILE, chats)
    return jsonify({"ok": True})


def _run_bi_neuron_task(tid, params, request_text, additional_files):
    with _task_lock:
        handler = TaskLogHandler(task_manager, tid)
        handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s"))

        root = logging.getLogger()
        root.addHandler(handler)
        old_level = root.level
        root.setLevel(logging.INFO)

        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = _StdStreamCapture(task_manager, tid, old_stdout)
        sys.stderr = _StdStreamCapture(task_manager, tid, old_stderr)

        try:
            if BINEURON_IMPORT_ERROR is not None:
                raise RuntimeError(
                    f"BiNeuron could not be imported: {BINEURON_IMPORT_ERROR}")

            task_manager.log(tid, "[web] Creating BiNeuron instance...")
            bi = BiNeuron(request=request_text,
                          additional_files=additional_files,
                          **params)
            task_manager.log(tid, "[web] Running final_ai_request()...")
            answer = bi.final_ai_request()
            task_manager.finish(tid, answer or "")
        except Exception as e:
            err = f"{type(e).__name__}: {e}\n{traceback.format_exc()}"
            task_manager.log(tid, "[web] ERROR: " + err)
            task_manager.fail(tid, err)
        finally:
            try:
                sys.stdout.flush()
                sys.stderr.flush()
            except Exception:
                pass
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            root.removeHandler(handler)
            root.setLevel(old_level)


@app.route("/api/chat", methods=["POST"])
def api_chat():
    body = request.get_json(silent=True) or {}
    user_text = (body.get("request") or "").strip()
    if not user_text:
        return jsonify({"error": "empty request"}), 400

    params = parse_settings_for_bineuron(body.get("settings") or {})

    uploaded = body.get("attached_files") or []
    additional_files = None
    if isinstance(uploaded, list) and uploaded:
        existing = [p for p in uploaded
                    if isinstance(p, str) and os.path.isfile(p)]
        if existing:
            additional_files = existing

    tid = task_manager.create()
    threading.Thread(
        target=_run_bi_neuron_task,
        args=(tid, params, user_text, additional_files),
        daemon=True,
    ).start()
    return jsonify({"task_id": tid})


@app.route("/api/chat/task/<tid>", methods=["GET"])
def api_chat_task(tid):
    since = _to_int(request.args.get("since"), 0)
    t = task_manager.get(tid, since=since)
    if t is None:
        abort(404)
    return jsonify(t)


@app.route("/api/upload", methods=["POST"])
def api_upload():
    files = request.files.getlist("files")
    if not files:
        return jsonify({"ok": True, "paths": []})

    session_dir = os.path.join(
        UPLOAD_DIR, datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    os.makedirs(session_dir, exist_ok=True)

    saved = []
    for f in files:
        if not f.filename:
            continue
        dest = os.path.join(session_dir, os.path.basename(f.filename))
        f.save(dest)
        saved.append(dest)

    return jsonify({"ok": True, "paths": saved})


@app.route("/api/models", methods=["GET"])
def api_list_models():
    models_dir = request.args.get("dir") or "./models"
    if not os.path.isdir(models_dir):
        return jsonify({"ok": False, "error": "not a directory", "models": []})
    gguf = []
    for root, _dirs, files in os.walk(models_dir):
        for name in files:
            if name.lower().endswith(".gguf"):
                gguf.append(os.path.relpath(os.path.join(root, name), models_dir))
    return jsonify({"ok": True, "models": sorted(gguf)})


@app.route("/api/storage/tree", methods=["POST"])
def api_storage_tree():
    body = request.get_json(silent=True) or {}
    path = body.get("path") or ""
    if not path or not os.path.isdir(path):
        return jsonify({"ok": False, "error": "invalid path", "tree": None})

    def build(p):
        try:
            entries = sorted(os.listdir(p))
        except PermissionError:
            return []
        out = []
        for name in entries:
            full = os.path.join(p, name)
            if os.path.isdir(full):
                out.append({"name": name, "path": full,
                            "type": "dir", "children": build(full)})
            else:
                out.append({"name": name, "path": full, "type": "file"})
        return out

    return jsonify({"ok": True, "tree": {
        "name": os.path.basename(path) or path,
        "path": path, "type": "dir", "children": build(path),
    }})


@app.route("/api/storage/open", methods=["POST"])
def api_storage_open():
    path = (request.get_json(silent=True) or {}).get("path") or ""
    if not os.path.isfile(path):
        return jsonify({"ok": False, "error": "not a file"})
    try:
        if os.name == "nt":
            os.startfile(path)
        elif sys.platform == "darwin":
            import subprocess
            subprocess.Popen(["open", path])
        else:
            import subprocess
            subprocess.Popen(["xdg-open", path])
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    print("=" * 60)
    print("BiNeuron Web UI  ->  http://127.0.0.1:5000")
    if BINEURON_IMPORT_ERROR:
        print(f"BiNeuron import failed: {BINEURON_IMPORT_ERROR}")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)