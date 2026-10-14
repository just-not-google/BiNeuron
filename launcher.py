# This code was made entirely using DeepSeek Coder.
# Link to the model: https://huggingface.co/collections/deepseek-ai/deepseek-coder


import os
import sys
import socket
import logging
import threading

logging.getLogger("werkzeug").disabled = True
logging.getLogger("werkzeug").propagate = False

class _Null:
    def write(self, *_a, **_k): pass
    def flush(self, *_a, **_k): pass
    def isatty(self, *_a, **_k): return False

sys.stdout = _Null()
sys.stderr = _Null()
try:
    from all_logic_interface.app import app
finally:
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

APP_TITLE    = "BiNeuron"
WIN_W, WIN_H = 1400, 900
MIN_W, MIN_H = WIN_W, WIN_H
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _resolve_icon():
    img_dir = os.path.join(BASE_DIR, "img_files")
    if sys.platform == "win32":
        candidates = ["logo.ico", "logo.png"]
    elif sys.platform == "darwin":
        candidates = ["logo.icns", "logo.png"]
    else:
        candidates = ["logo.png", "logo.ico"]
    for name in candidates:
        path = os.path.join(img_dir, name)
        if os.path.isfile(path):
            return path
    return None

ICON_PATH = _resolve_icon()

def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]

class _ServerThread(threading.Thread):
    def __init__(self, wsgi_app, host: str, port: int):
        super().__init__(daemon=True, name="http-server")
        from werkzeug.serving import make_server
        self._srv = make_server(host, port, wsgi_app, threaded=True)

    def run(self) -> None:
        try:
            self._srv.serve_forever()
        except Exception:
            pass

    def stop(self) -> None:
        try:
            self._srv.shutdown()
        except Exception:
            pass
        try:
            self._srv.server_close()
        except Exception:
            pass

def _set_windows_app_id() -> None:
    if sys.platform != "win32":
        return
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "BiNeuron.App.1"
        )
    except Exception:
        pass

def _set_macos_app_name() -> None:
    if sys.platform != "darwin":
        return
    try:
        import setproctitle
        setproctitle.setproctitle(APP_TITLE)
    except Exception:
        pass

def main() -> None:
    _set_windows_app_id()
    _set_macos_app_name()
    old_out, old_err = sys.stdout, sys.stderr
    sys.stdout = _Null()
    sys.stderr = _Null()
    try:
        port = _find_free_port()
        server = _ServerThread(app, "127.0.0.1", port)
        server.start()
    finally:
        sys.stdout, sys.stderr = old_out, old_err

    import webview
    window = webview.create_window(
        title=APP_TITLE,
        url=f"http://127.0.0.1:{port}",
        width=WIN_W,
        height=WIN_H,
        min_size=(MIN_W, MIN_H),
        text_select=True,
    )
    _closing = threading.Event()

    def _shutdown_and_exit(*_a, **_k):
        if _closing.is_set():
            return
        _closing.set()
        try:
            server.stop()
        finally:
            os._exit(0)

    window.events.closed += _shutdown_and_exit

    start_kwargs = {}
    if ICON_PATH:
        start_kwargs["icon"] = ICON_PATH

    try:
        webview.start(**start_kwargs)
    finally:
        _shutdown_and_exit()


if __name__ == "__main__":
    main()