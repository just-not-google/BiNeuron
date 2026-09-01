import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import queue
import logging
import traceback
import json
import os
import sys
from datetime import datetime
from BiNeuron import BiNeuron
from BiNeuron.data.constants_for_functions import (HTTP_PROTOCOL, HTTPS_PROTOCOL,
                                                   TYPES_POWER, PREFERENCES_IN_AI_LIST,
                                                   DETERMINANT_MODE_LIST)
from BiNeuron.data.variants_industrial_scenarios import ALL_MAIN_PROMPTS
from BiNeuron.data.natural_languages import NATURAL_LANGUAGES
from BiNeuron.data.translated_ui import TRANSLATED_UI
from BiNeuron.data.fonts_and_colors import *


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class NumericEntry(ttk.Entry):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        vcmd = (self.register(self._validate), "%P")
        self.config(validate="key", validatecommand=vcmd)

    def _validate(self, new_value):
        if new_value == "":
            return True
        try:
            float(new_value)
            return True
        except ValueError:
            return False

    def get_float(self, default=0.0):
        try:
            return float(self.get())
        except ValueError:
            return default

    def get_int(self, default=0):
        try:
            return int(self.get())
        except ValueError:
            return default


class SpinEntry(ttk.Frame):
    def __init__(self, master, step=1, default=0, **kwargs):
        super().__init__(master)
        self.step = step
        self.entry = NumericEntry(self, **kwargs)
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 2))
        self.entry.insert(0, str(default))
        self.btn_up = ttk.Button(self, text="▲", width=2, command=self.increment)
        self.btn_up.grid(row=0, column=1, padx=1, sticky="e")
        self.btn_down = ttk.Button(self, text="▼", width=2, command=self.decrement)
        self.btn_down.grid(row=0, column=2, padx=1, sticky="e")
        self.grid_columnconfigure(0, weight=1)

    def increment(self):
        try:
            val = float(self.entry.get())
        except ValueError:
            val = 0.0
        val += self.step
        self._set_value(val)

    def decrement(self):
        try:
            val = float(self.entry.get())
        except ValueError:
            val = 0.0
        val -= self.step
        self._set_value(val)

    def _set_value(self, val):
        if isinstance(self.step, int) or self.step == int(self.step):
            self.entry.delete(0, "end")
            self.entry.insert(0, str(int(val)))
        else:
            precision = len(str(self.step).split('.')[1]) if '.' in str(self.step) else 1
            self.entry.delete(0, "end")
            self.entry.insert(0, f"{val:.{precision}f}")

    def get(self):
        return self.entry.get()

    def get_int(self, default=0):
        return self.entry.get_int(default)

    def get_float(self, default=0.0):
        return self.entry.get_float(default)

    def delete(self, first, last=None):
        self.entry.delete(first, last)

    def insert(self, index, string):
        self.entry.insert(index, string)


class ScrollableFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas = tk.Canvas(self, bg=BG_FRAME, highlightthickness=0, borderwidth=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style="TFrame")
        self.scrollable_frame.bind("<Configure>",
                                   lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas.find_withtag("all")[0], width=event.width)

    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def get_frame(self):
        return self.scrollable_frame


class BiNeuronGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BiNeuron")
        self.root.geometry("1500x900")
        self.root.minsize(1500, 900)
        self.root.iconbitmap(resource_path("img_files/logo.ico"))
        self.root.configure(bg=BG_MAIN)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self._setup_styles()
        self.alex_instance = None
        self.is_busy = False
        self.is_scanning = False
        self.message_queue = queue.Queue()
        self.attached_files = []
        self.virtual_files = []
        self.virtual_tree_data = {}
        self.chats_file = "chats.json"
        self.storage_path_file = "storage_path.json"
        self.settings_file = "settings.json"
        self.storage_path = self.load_storage_path()
        self.translations = TRANSLATED_UI
        self.widgets_to_translate = []
        self.select_language()
        self.root.grid_columnconfigure(0, weight=1, uniform="main", minsize=320)
        self.root.grid_columnconfigure(1, weight=4, uniform="main")
        self.root.grid_columnconfigure(2, weight=1, uniform="main", minsize=200)
        self.root.grid_rowconfigure(0, weight=1)
        self.create_settings_panel()
        self.create_chat_panel()
        self.create_history_panel()
        self.setup_logging()
        self.load_chats_from_file()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.poll_queue()
        self.welcome_label = None
        self.show_welcome_placeholder()
        self.check_pending_message()
        self.load_settings()
        self.apply_language()

    def _setup_styles(self):
        self.style.configure(".",
                             background=BG_MAIN,
                             foreground=FG_TEXT,
                             font=FONT_MAIN)
        self.style.configure("TFrame",
                             background=BG_MAIN)
        self.style.configure("TLabel",
                             background=BG_MAIN,
                             foreground=FG_TEXT,
                             font=FONT_MAIN)
        self.style.configure("TButton",
                             background=BG_FRAME,
                             foreground=FG_TEXT,
                             bordercolor=BORDER,
                             lightcolor=BG_FRAME,
                             darkcolor=BG_FRAME,
                             focusthickness=0,
                             focuscolor=BG_FRAME,
                             padding=5)
        self.style.map("TButton",
                       background=[("active", ACCENT_HOVER), ("pressed", ACCENT)],
                       foreground=[("active", "white"), ("pressed", "white")])
        self.style.configure("TEntry",
                             fieldbackground=BG_ENTRY,
                             foreground=FG_TEXT,
                             bordercolor=BORDER,
                             lightcolor=BORDER,
                             darkcolor=BORDER,
                             insertcolor=FG_TEXT,
                             padding=3)
        self.style.configure("TCheckbutton",
                             background=BG_MAIN,
                             foreground=FG_TEXT,
                             focusthickness=0,
                             focuscolor=BG_MAIN)
        self.style.map("TCheckbutton",
                       background=[("active", BG_MAIN)],
                       foreground=[("active", FG_TEXT)])
        self.style.configure("TCombobox",
                             fieldbackground=BG_ENTRY,
                             background=BG_ENTRY,
                             foreground=FG_TEXT,
                             arrowcolor=FG_TEXT,
                             bordercolor=BORDER,
                             lightcolor=BORDER,
                             darkcolor=BORDER,
                             padding=3)
        self.style.map("TCombobox",
                       fieldbackground=[("readonly", BG_ENTRY)],
                       selectbackground=[("readonly", BG_ENTRY)],
                       selectforeground=[("readonly", FG_TEXT)])
        self.style.configure("Treeview",
                             background=TREE_BG,
                             foreground=TREE_FG,
                             fieldbackground=TREE_BG,
                             borderwidth=0,
                             font=FONT_MAIN)
        self.style.map("Treeview",
                       background=[("selected", TREE_SELECT_BG)],
                       foreground=[("selected", TREE_SELECT_FG)])
        self.style.configure("Treeview.Heading",
                             background=BG_FRAME,
                             foreground=FG_TEXT,
                             relief="flat",
                             font=FONT_BOLD)
        self.style.map("Treeview.Heading",
                       background=[("active", BG_FRAME)],
                       foreground=[("active", FG_TEXT)])
        self.style.configure("Vertical.TScrollbar",
                             background=BG_FRAME,
                             troughcolor=BG_MAIN,
                             bordercolor=BG_MAIN,
                             arrowcolor=FG_TEXT)
        self.style.configure("Horizontal.TScrollbar",
                             background=BG_FRAME,
                             troughcolor=BG_MAIN,
                             bordercolor=BG_MAIN,
                             arrowcolor=FG_TEXT)

    def select_language(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("BiNeuron")
        dialog.geometry("300x100")
        dialog.resizable(False, False)
        dialog.configure(bg=BG_MAIN)
        dialog.transient(self.root)
        dialog.iconbitmap(resource_path("img_files/logo.ico"))
        dialog.grab_set()
        dialog.update_idletasks()
        x = self.root.winfo_screenwidth() // 2 - 150
        y = self.root.winfo_screenheight() // 2 - 75
        dialog.geometry(f"+{x}+{y}")

        if isinstance(NATURAL_LANGUAGES, dict):
            lang_names = list(NATURAL_LANGUAGES.keys())
        else:
            lang_names = list(NATURAL_LANGUAGES) \
                if NATURAL_LANGUAGES else ["English", "Russian"]

        combo = ttk.Combobox(dialog, values=lang_names, state="readonly")
        combo.pack(pady=10)

        if lang_names:
            combo.current(0)

        def on_ok():
            selected = combo.get()
            if selected:
                self.current_lang = self._get_lang_code(selected)
            else:
                self.current_lang = "en"
            dialog.destroy()

        ok_btn = ttk.Button(dialog, text="OK", command=on_ok)
        ok_btn.pack(pady=10)
        self.root.wait_window(dialog)

    def _get_lang_code(self, lang_name):
        if hasattr(NATURAL_LANGUAGES, 'get'):
            code = NATURAL_LANGUAGES.get(lang_name)
            if code:
                return code

        mapping = {"English": "en", "Russian": "ru"}
        return mapping.get(lang_name, "en")

    def translate(self, key, **kwargs):
        lang_dict = self.translations.get(self.current_lang, self.translations["en"])
        text = lang_dict.get(key, key)

        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                pass
        return text

    def apply_language(self):
        for widget, key, attr in self.widgets_to_translate:
            try:
                if attr == "text":
                    widget.config(text=self.translate(key))
                elif attr == "title":
                    widget.title(self.translate(key))
            except Exception:
                pass
        self.root.title(self.translate("title"))

        if hasattr(self, 'history_title'):
            if self.virtual_storage_var.get():
                self.history_title.config(text=self.translate("history_title_virtual"))
            else:
                self.history_title.config(text=self.translate("history_title"))

        if hasattr(self, 'attached_frame'):
            self.attached_frame.config(text=self.translate("attached_files_label"))

        if hasattr(self, 'resume_button'):
            self.resume_button.config(text=self.translate("resume_button_text"))

        if self.welcome_label is not None:
            self.welcome_label.config(text=self.translate("welcome_text"))

        self.update_attached_text()

    def setup_logging(self):
        class ChatHandler(logging.Handler):
            def __init__(self, gui):
                super().__init__()
                self.gui = gui

            def emit(self, record):
                msg = self.format(record)
                self.gui.root.after(0, self.gui.display_log_message, msg)

        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        handler = ChatHandler(self)
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.INFO)

        logger = logging.getLogger("BiNeuron")
        logger.setLevel(logging.INFO)
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    def display_log_message(self, text, save=True):
        if self.welcome_label is not None:
            self.hide_welcome_placeholder()
        was_at_bottom = self._is_scrolled_to_bottom()
        frame = tk.Frame(self.messages_frame, bg=BG_FRAME, bd=0)
        frame.pack(fill="x", padx=10, pady=2)

        label = tk.Label(frame,
                         text=f"[LOG] {text}",
                         fg=FG_TEXT,
                         bg=BG_FRAME,
                         font=FONT_SMALL,
                         wraplength=600,
                         justify="left",
                         anchor="w")
        label.pack(side="left", padx=10, pady=2, fill="x", expand=True)

        self.messages_frame.update_idletasks()
        if was_at_bottom:
            self.messages_canvas.yview_moveto(1.0)

        if save:
            self._save_log_to_chat(text)

    def _save_log_to_chat(self, text):
        if (hasattr(self, 'current_chat_id')
                and self.current_chat_id is not None
                and self.current_chat_id in self.chats):
            timestamp = datetime.now().strftime("%H:%M")
            log_entry = {"role": "system", "content": text, "timestamp": timestamp}
            self.chats[self.current_chat_id]["messages"].append(log_entry)
            self.save_chats_to_file()
            self.update_history_list()

    def load_storage_path(self):
        if os.path.exists(self.storage_path_file):
            try:
                with open(self.storage_path_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return ""
        return ""

    def save_storage_path(self):
        try:
            with open(self.storage_path_file, "w", encoding="utf-8") as f:
                json.dump(self.storage_path, f, ensure_ascii=False, indent=2)
        except:
            pass

    def get_all_settings(self):
        return {
            "theme": "dark",
            "country": self.country_entry.get(),
            "protocol": self.protocol_combobox.get(),
            "max_timeout": self.max_timeout_entry.get(),
            "is_working": "1" if self.is_working_var.get() else "0",
            "auto_proxies": "1" if self.auto_proxies_var.get() else "0",
            "your_proxies_dict": self.your_proxies_dict_text.get("1.0", "end-1c"),
            "min_timeout_for_checking_availability": self.min_timeout_entry.get(),
            "max_timeout_for_checking_availability": self.max_timeout_entry.get(),
            "retries": self.retries_entry.get(),
            "github_proxies": "1" if self.github_proxies_var.get() else "0",
            "url_lst": self.url_lst_text.get("1.0", "end-1c"),
            "proxy_retries": self.proxy_retries_entry.get(),
            "main_retries": self.main_retries_entry.get(),
            "preferences_in_ai": self.preferences_combobox.get(),
            "models_dir": self.models_dir_entry.get(),
            "with_ai_orchestrator": "1" if self.with_ai_orchestrator_var.get() else "0",
            "n_ctx": self.n_ctx_entry.get(),
            "n_gpu_layers": self.n_gpu_layers_entry.get(),
            "max_tokens": self.max_tokens_entry.get(),
            "your_token_for_hf": self.token_hf_entry.get(),
            "subdomain": self.subdomain_entry.get(),
            "repo_id": self.repo_id_entry.get(),
            "filename": self.filename_entry.get(),
            "prefer_mirror": "1" if self.prefer_mirror_var.get() else "0",
            "main_prompt_mode": self.main_prompt_mode_combobox.get(),
            "main_prompt": self.main_prompt_text.get("1.0", "end-1c"),
            "temperature": self.temperature_entry.get(),
            "determinant_mode": self.determinant_mode_combobox.get(),
            "accurate_translation": "1" if self.accurate_translation_var.get() else "0",
            "your_key_for_deepl": self.deepl_key_entry.get(),
            "request_language": self.request_language_entry.get(),
            "lang_lst": self.lang_lst_text.get("1.0", "end-1c"),
            "use_gpu_for_ocr": "1" if self.use_gpu_ocr_var.get() else "0",
            "with_ocr": "1" if self.with_ocr_var.get() else "0",
            "cloud_version": "1" if self.cloud_version_var.get() else "0",
            "with_deepseek": "1" if self.with_deepseek_var.get() else "0",
            "model_size": self.model_size_combobox.get(),
            "crop_mode": "1" if self.crop_mode_var.get() else "0",
            "base_url": self.base_url_entry.get(),
            "api_key_for_deepseek_ocr": self.deepseek_api_entry.get(),
            "timeout_for_deepseek_ocr": self.deepseek_timeout_entry.get(),
            "max_rate_limit_retries": self.max_rate_limit_retries_entry.get(),
            "filter_for_swearing": "1" if self.filter_swearing_var.get() else "0",
            "verbose": "1" if self.verbose_var.get() else "0",
            "echo": "1" if self.echo_var.get() else "0",
            "type_computer": self.type_computer_combobox.get(),
            "proprietary_algorithms": "1" if self.proprietary_algorithms_var.get() else "0",
            "writing_response_to_file": "1" if self.writing_response_var.get() else "0",
            "editing_files": "1" if self.editing_files_var.get() else "0",
            "virtual_storage": "1" if self.virtual_storage_var.get() else "0",
            "storage_path": self.storage_path,
        }

    def set_all_settings(self, settings):
        def set_entry(entry, value):
            entry.delete(0, "end")
            entry.insert(0, str(value))

        if "country" in settings:
            set_entry(self.country_entry, settings["country"])
        if "protocol" in settings:
            self.protocol_combobox.set(settings["protocol"])
        if "max_timeout" in settings:
            set_entry(self.max_timeout_entry.entry, settings["max_timeout"])
        if "is_working" in settings:
            self.is_working_var.set(settings["is_working"] == "1")
        if "auto_proxies" in settings:
            self.auto_proxies_var.set(settings["auto_proxies"] == "1")
        if "your_proxies_dict" in settings:
            self.your_proxies_dict_text.delete("1.0", "end")
            self.your_proxies_dict_text.insert("1.0", settings["your_proxies_dict"])
        if "min_timeout_for_checking_availability" in settings:
            set_entry(self.min_timeout_entry.entry, settings["min_timeout_for_checking_availability"])
        if "max_timeout_for_checking_availability" in settings:
            set_entry(self.max_timeout_entry.entry, settings["max_timeout_for_checking_availability"])
        if "retries" in settings:
            set_entry(self.retries_entry.entry, settings["retries"])
        if "github_proxies" in settings:
            self.github_proxies_var.set(settings["github_proxies"] == "1")
        if "url_lst" in settings:
            self.url_lst_text.delete("1.0", "end")
            self.url_lst_text.insert("1.0", settings["url_lst"])
        if "proxy_retries" in settings:
            set_entry(self.proxy_retries_entry.entry, settings["proxy_retries"])
        if "main_retries" in settings:
            set_entry(self.main_retries_entry.entry, settings["main_retries"])
        if "preferences_in_ai" in settings:
            self.preferences_combobox.set(settings["preferences_in_ai"])
        if "models_dir" in settings:
            set_entry(self.models_dir_entry, settings["models_dir"])
        if "with_ai_orchestrator" in settings:
            self.with_ai_orchestrator_var.set(settings["with_ai_orchestrator"] == "1")
        if "n_ctx" in settings:
            set_entry(self.n_ctx_entry.entry, settings["n_ctx"])
        if "n_gpu_layers" in settings:
            set_entry(self.n_gpu_layers_entry.entry, settings["n_gpu_layers"])
        if "max_tokens" in settings:
            set_entry(self.max_tokens_entry.entry, settings["max_tokens"])
        if "your_token_for_hf" in settings:
            set_entry(self.token_hf_entry, settings["your_token_for_hf"])
        if "subdomain" in settings:
            set_entry(self.subdomain_entry, settings["subdomain"])
        if "repo_id" in settings:
            set_entry(self.repo_id_entry, settings["repo_id"])
        if "filename" in settings:
            set_entry(self.filename_entry, settings["filename"])
        if "prefer_mirror" in settings:
            self.prefer_mirror_var.set(settings["prefer_mirror"] == "1")
        if "main_prompt_mode" in settings:
            self.main_prompt_mode_combobox.set(settings["main_prompt_mode"])
        if "main_prompt" in settings:
            self.main_prompt_text.delete("1.0", "end")
            self.main_prompt_text.insert("1.0", settings["main_prompt"])
        if "temperature" in settings:
            set_entry(self.temperature_entry.entry, settings["temperature"])
        if "determinant_mode" in settings:
            self.determinant_mode_combobox.set(settings["determinant_mode"])
        if "accurate_translation" in settings:
            self.accurate_translation_var.set(settings["accurate_translation"] == "1")
        if "your_key_for_deepl" in settings:
            set_entry(self.deepl_key_entry, settings["your_key_for_deepl"])
        if "request_language" in settings:
            set_entry(self.request_language_entry, settings["request_language"])
        if "lang_lst" in settings:
            self.lang_lst_text.delete("1.0", "end")
            self.lang_lst_text.insert("1.0", settings["lang_lst"])
        if "use_gpu_for_ocr" in settings:
            self.use_gpu_ocr_var.set(settings["use_gpu_for_ocr"] == "1")
        if "with_ocr" in settings:
            self.with_ocr_var.set(settings["with_ocr"] == "1")
        if "cloud_version" in settings:
            self.cloud_version_var.set(settings["cloud_version"] == "1")
        if "with_deepseek" in settings:
            self.with_deepseek_var.set(settings["with_deepseek"] == "1")
        if "model_size" in settings:
            self.model_size_combobox.set(settings["model_size"])
        if "crop_mode" in settings:
            self.crop_mode_var.set(settings["crop_mode"] == "1")
        if "base_url" in settings:
            set_entry(self.base_url_entry, settings["base_url"])
        if "api_key_for_deepseek_ocr" in settings:
            set_entry(self.deepseek_api_entry, settings["api_key_for_deepseek_ocr"])
        if "timeout_for_deepseek_ocr" in settings:
            set_entry(self.deepseek_timeout_entry.entry, settings["timeout_for_deepseek_ocr"])
        if "max_rate_limit_retries" in settings:
            set_entry(self.max_rate_limit_retries_entry.entry, settings["max_rate_limit_retries"])
        if "filter_for_swearing" in settings:
            self.filter_swearing_var.set(settings["filter_for_swearing"] == "1")
        if "verbose" in settings:
            self.verbose_var.set(settings["verbose"] == "1")
        if "echo" in settings:
            self.echo_var.set(settings["echo"] == "1")
        if "type_computer" in settings:
            self.type_computer_combobox.set(settings["type_computer"])
        if "proprietary_algorithms" in settings:
            self.proprietary_algorithms_var.set(settings["proprietary_algorithms"] == "1")
        if "writing_response_to_file" in settings:
            self.writing_response_var.set(settings["writing_response_to_file"] == "1")
        if "editing_files" in settings:
            self.editing_files_var.set(settings["editing_files"] == "1")
        if "virtual_storage" in settings:
            self.virtual_storage_var.set(settings["virtual_storage"] == "1")
        if "storage_path" in settings:
            self.storage_path = settings["storage_path"]
            if hasattr(self, "storage_path_entry"):
                self.storage_path_entry.delete(0, "end")
                self.storage_path_entry.insert(0, self.storage_path)
            self.save_storage_path()
            if self.virtual_storage_var.get():
                self.build_tree()

        self.update_attached_text()
        self.apply_language()

    def set_default_settings(self):
        default = {
            "theme": "dark",
            "country": "",
            "protocol": HTTP_PROTOCOL,
            "max_timeout": "30",
            "is_working": "0",
            "auto_proxies": "0",
            "your_proxies_dict": "",
            "min_timeout_for_checking_availability": "5",
            "max_timeout_for_checking_availability": "15",
            "retries": "3",
            "github_proxies": "0",
            "url_lst": "",
            "proxy_retries": "3",
            "main_retries": "3",
            "preferences_in_ai": PREFERENCES_IN_AI_LIST[0],
            "models_dir": "./models",
            "with_ai_orchestrator": "1",
            "n_ctx": "0",
            "n_gpu_layers": "0",
            "max_tokens": "4096",
            "your_token_for_hf": "",
            "subdomain": "",
            "repo_id": "",
            "filename": "",
            "prefer_mirror": "1",
            "main_prompt_mode": list(ALL_MAIN_PROMPTS.keys())[0],
            "main_prompt": "",
            "temperature": "0.1",
            "determinant_mode": DETERMINANT_MODE_LIST[0],
            "accurate_translation": "0",
            "your_key_for_deepl": "",
            "request_language": "en",
            "lang_lst": "",
            "use_gpu_for_ocr": "0",
            "with_ocr": "0",
            "cloud_version": "0",
            "with_deepseek": "1",
            "model_size": "tiny",
            "crop_mode": "0",
            "base_url": "https://api.siliconflow.cn/v1/chat/completions",
            "api_key_for_deepseek_ocr": "",
            "timeout_for_deepseek_ocr": "30",
            "max_rate_limit_retries": "3",
            "filter_for_swearing": "0",
            "verbose": "0",
            "echo": "0",
            "type_computer": "auto",
            "proprietary_algorithms": "0",
            "writing_response_to_file": "0",
            "editing_files": "0",
            "virtual_storage": "0",
            "storage_path": "",
        }
        self.set_all_settings(default)

    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                self.set_all_settings(settings)
            except Exception as e:
                logging.error(f"Failed to load settings: {e}")
                self.set_default_settings()
        else:
            self.set_default_settings()

    def save_settings(self):
        settings = self.get_all_settings()
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"Failed to save settings: {e}")

    def reset_settings(self):
        self.set_default_settings()
        self.save_settings()
        messagebox.showinfo(self.translate("success_info"), self.translate("settings_reset"))

    def load_chats_from_file(self):
        if os.path.exists(self.chats_file):
            try:
                with open(self.chats_file, "r", encoding="utf-8") as f:
                    self.chats = json.load(f)

                if not isinstance(self.chats, dict):
                    self.chats = {}

            except Exception as e:
                logging.error(f"Failed to load chats: {e}")
                self.chats = {}
        else:
            self.chats = {}

        if not self.chats:
            self.add_new_chat()

        first_id = next(iter(self.chats.keys()), None)

        if first_id:
            self.current_chat_id = first_id
            self.load_chat(first_id)
        else:
            self.current_chat_id = None

        self.update_history_list()

    def save_chats_to_file(self):
        try:
            with open(self.chats_file, "w", encoding="utf-8") as f:
                json.dump(self.chats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"Failed to save chats: {e}")

    def on_closing(self):
        self.save_chats_to_file()
        self.save_storage_path()
        self.save_settings()
        self.root.destroy()

    def create_settings_panel(self):
        settings_outer = tk.Frame(self.root, bg=BG_MAIN)
        settings_outer.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        settings_outer.grid_rowconfigure(1, weight=1)
        settings_outer.grid_columnconfigure(0, weight=1)
        title_label = ttk.Label(settings_outer,
                                text=self.translate("settings_title"),
                                font=FONT_TITLE)
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.widgets_to_translate.append((title_label, "settings_title", "text"))
        settings_scroll = ScrollableFrame(settings_outer)
        settings_scroll.grid(row=1, column=0, sticky="nsew")
        settings_frame = settings_scroll.get_frame()
        settings_frame.grid_columnconfigure(0, weight=1)
        btn_frame = ttk.Frame(settings_frame)
        btn_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=(0, 10))
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)
        reset_btn = ttk.Button(btn_frame,
                               text=self.translate("reset_btn"),
                               width=10,
                               command=self.reset_settings)
        reset_btn.grid(row=0, column=0, sticky="ew", padx=2)
        self.widgets_to_translate.append((reset_btn, "reset_btn", "text"))
        export_btn = ttk.Button(btn_frame,
                                text=self.translate("export_all_btn"),
                                width=10,
                                command=self.export_all_chats)
        export_btn.grid(row=0, column=1, sticky="ew", padx=2)
        self.widgets_to_translate.append((export_btn, "export_all_btn", "text"))
        delete_btn = ttk.Button(btn_frame,
                                text=self.translate("delete_all_btn"),
                                width=10,
                                command=self.delete_all_chats)
        delete_btn.grid(row=0, column=2, sticky="ew", padx=2)
        self.widgets_to_translate.append((delete_btn, "delete_all_btn", "text"))
        network_frame = ttk.LabelFrame(settings_frame,
                                       text=self.translate("network_frame"),
                                       padding=5)
        network_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        network_frame.grid_columnconfigure(0, weight=0, minsize=160)
        network_frame.grid_columnconfigure(1, weight=1)
        self.widgets_to_translate.append((network_frame, "network_frame", "text"))
        row = 0
        country_label = ttk.Label(network_frame, text=self.translate("country_label"))
        country_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((country_label, "country_label", "text"))
        self.country_entry = ttk.Entry(network_frame)
        self.country_entry.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        protocol_label = ttk.Label(network_frame, text=self.translate("protocol_label"))
        protocol_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((protocol_label, "protocol_label", "text"))
        self.protocol_combobox = ttk.Combobox(network_frame,
                                              values=[HTTP_PROTOCOL, HTTPS_PROTOCOL],
                                              state="readonly")
        self.protocol_combobox.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        max_timeout_label = ttk.Label(network_frame, text=self.translate("max_timeout_label"))
        max_timeout_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((max_timeout_label, "max_timeout_label", "text"))
        self.max_timeout_entry = SpinEntry(network_frame, step=1, default=30)
        self.max_timeout_entry.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        is_working_label = ttk.Label(network_frame, text=self.translate("is_working_label"))
        is_working_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((is_working_label, "is_working_label", "text"))
        self.is_working_var = tk.BooleanVar(value=False)
        (ttk.Checkbutton(network_frame, variable=self.is_working_var).
         grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0)))
        row += 1
        auto_proxies_label = ttk.Label(network_frame, text=self.translate("auto_proxies_label"))
        auto_proxies_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((auto_proxies_label, "auto_proxies_label", "text"))
        self.auto_proxies_var = tk.BooleanVar(value=False)
        (ttk.Checkbutton(network_frame, variable=self.auto_proxies_var).
         grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0)))
        row += 1
        your_proxies_label = ttk.Label(network_frame, text=self.translate("your_proxies_label"))
        your_proxies_label.grid(row=row, column=0, sticky="nw", pady=2)
        self.widgets_to_translate.append((your_proxies_label, "your_proxies_label", "text"))
        self.your_proxies_dict_text = tk.Text(network_frame,
                                              height=3,
                                              bg=BG_ENTRY,
                                              fg=FG_TEXT,
                                              insertbackground=FG_TEXT,
                                              relief="flat",
                                              borderwidth=1,
                                              highlightthickness=1,
                                              highlightbackground=BORDER,
                                              highlightcolor=BORDER,
                                              wrap="word")
        self.your_proxies_dict_text.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        min_timeout_check_label = ttk.Label(network_frame,
                                            text=self.translate("min_timeout_check_label"))
        min_timeout_check_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((min_timeout_check_label,
                                          "min_timeout_check_label", "text"))
        self.min_timeout_entry = SpinEntry(network_frame, step=1, default=5)
        self.min_timeout_entry.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        max_timeout_check_label = ttk.Label(network_frame,
                                            text=self.translate("max_timeout_check_label"))
        max_timeout_check_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((max_timeout_check_label,
                                          "max_timeout_check_label", "text"))
        self.max_timeout_entry = SpinEntry(network_frame, step=1, default=15)
        self.max_timeout_entry.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        retries_label = ttk.Label(network_frame, text=self.translate("retries_label"))
        retries_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((retries_label, "retries_label", "text"))
        self.retries_entry = SpinEntry(network_frame, step=1, default=3)
        self.retries_entry.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        github_proxies_label = ttk.Label(network_frame,
                                         text=self.translate("github_proxies_label"))
        github_proxies_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((github_proxies_label,
                                          "github_proxies_label", "text"))
        self.github_proxies_var = tk.BooleanVar(value=False)
        (ttk.Checkbutton(network_frame, variable=self.github_proxies_var).
         grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0)))
        row += 1
        url_list_label = ttk.Label(network_frame, text=self.translate("url_list_label"))
        url_list_label.grid(row=row, column=0, sticky="nw", pady=2)
        self.widgets_to_translate.append((url_list_label, "url_list_label", "text"))
        self.url_lst_text = tk.Text(network_frame,
                                    height=3,
                                    bg=BG_ENTRY,
                                    fg=FG_TEXT,
                                    insertbackground=FG_TEXT,
                                    relief="flat",
                                    borderwidth=1,
                                    highlightthickness=1,
                                    highlightbackground=BORDER,
                                    highlightcolor=BORDER,
                                    wrap="word")
        self.url_lst_text.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        proxy_retries_label = ttk.Label(network_frame, text=self.translate("proxy_retries_label"))
        proxy_retries_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((proxy_retries_label, "proxy_retries_label", "text"))
        self.proxy_retries_entry = SpinEntry(network_frame, step=1, default=3)
        self.proxy_retries_entry.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        main_retries_label = ttk.Label(network_frame, text=self.translate("main_retries_label"))
        main_retries_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((main_retries_label, "main_retries_label", "text"))
        self.main_retries_entry = SpinEntry(network_frame, step=1, default=3)
        self.main_retries_entry.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        model_frame = ttk.LabelFrame(settings_frame, text=self.translate("model_frame"), padding=5)
        model_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        model_frame.grid_columnconfigure(0, weight=0, minsize=160)
        model_frame.grid_columnconfigure(1, weight=1)
        self.widgets_to_translate.append((model_frame, "model_frame", "text"))
        row = 0
        preferences_label = ttk.Label(model_frame, text=self.translate("preferences_in_ai_label"))
        preferences_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((preferences_label, "preferences_in_ai_label", "text"))
        self.preferences_combobox = ttk.Combobox(model_frame,
                                                 values=PREFERENCES_IN_AI_LIST,
                                                 state="readonly")
        self.preferences_combobox.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        models_dir_label = ttk.Label(model_frame, text=self.translate("models_dir_label"))
        models_dir_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((models_dir_label, "models_dir_label", "text"))
        self.models_dir_entry = ttk.Entry(model_frame)
        self.models_dir_entry.insert(0, "./models")
        self.models_dir_entry.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        with_ai_orchestrator_label = ttk.Label(model_frame,
                                               text=self.translate("with_ai_orchestrator_label"))
        with_ai_orchestrator_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((with_ai_orchestrator_label,
                                          "with_ai_orchestrator_label", "text"))
        self.with_ai_orchestrator_var = tk.BooleanVar(value=True)
        (ttk.Checkbutton(model_frame, variable=self.with_ai_orchestrator_var).
         grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0)))
        row += 1
        n_ctx_label = ttk.Label(model_frame, text=self.translate("n_ctx_label"))
        n_ctx_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((n_ctx_label, "n_ctx_label", "text"))
        self.n_ctx_entry = SpinEntry(model_frame, step=1, default=0)
        self.n_ctx_entry.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        n_gpu_layers_label = ttk.Label(model_frame, text=self.translate("n_gpu_layers_label"))
        n_gpu_layers_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((n_gpu_layers_label, "n_gpu_layers_label", "text"))
        self.n_gpu_layers_entry = SpinEntry(model_frame, step=1, default=0)
        self.n_gpu_layers_entry.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        max_tokens_label = ttk.Label(model_frame, text=self.translate("max_tokens_label"))
        max_tokens_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((max_tokens_label, "max_tokens_label", "text"))
        self.max_tokens_entry = SpinEntry(model_frame, step=1, default=4096)
        self.max_tokens_entry.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        token_hf_label = ttk.Label(model_frame, text=self.translate("token_hf_label"))
        token_hf_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((token_hf_label, "token_hf_label", "text"))
        self.token_hf_entry = ttk.Entry(model_frame)
        self.token_hf_entry.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        subdomain_label = ttk.Label(model_frame, text=self.translate("subdomain_label"))
        subdomain_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((subdomain_label, "subdomain_label", "text"))
        self.subdomain_entry = ttk.Entry(model_frame)
        self.subdomain_entry.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        repo_id_label = ttk.Label(model_frame, text=self.translate("repo_id_label"))
        repo_id_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((repo_id_label, "repo_id_label", "text"))
        self.repo_id_entry = ttk.Entry(model_frame)
        self.repo_id_entry.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        filename_label = ttk.Label(model_frame, text=self.translate("filename_label"))
        filename_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((filename_label, "filename_label", "text"))
        self.filename_entry = ttk.Entry(model_frame)
        self.filename_entry.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        prefer_mirror_label = ttk.Label(model_frame, text=self.translate("prefer_mirror_label"))
        prefer_mirror_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((prefer_mirror_label, "prefer_mirror_label", "text"))
        self.prefer_mirror_var = tk.BooleanVar(value=True)
        (ttk.Checkbutton(model_frame, variable=self.prefer_mirror_var).
         grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0)))
        row += 1
        main_prompt_mode_label = ttk.Label(model_frame, text=self.translate("main_prompt_mode_label"))
        main_prompt_mode_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((main_prompt_mode_label, "main_prompt_mode_label", "text"))
        self.main_prompt_mode_combobox = ttk.Combobox(model_frame,
                                                      values=list(ALL_MAIN_PROMPTS.keys()),
                                                      state="readonly")
        self.main_prompt_mode_combobox.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        main_prompt_label = ttk.Label(model_frame, text=self.translate("main_prompt_label"))
        main_prompt_label.grid(row=row, column=0, sticky="nw", pady=2)
        self.widgets_to_translate.append((main_prompt_label, "main_prompt_label", "text"))
        self.main_prompt_text = tk.Text(model_frame,
                                        height=3,
                                        bg=BG_ENTRY,
                                        fg=FG_TEXT,
                                        insertbackground=FG_TEXT,
                                        relief="flat",
                                        borderwidth=1,
                                        highlightthickness=1,
                                        highlightbackground=BORDER,
                                        highlightcolor=BORDER,
                                        wrap="word")
        self.main_prompt_text.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        temperature_label = ttk.Label(model_frame, text=self.translate("temperature_label"))
        temperature_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((temperature_label, "temperature_label", "text"))
        self.temperature_entry = SpinEntry(model_frame, step=0.1, default=0.1)
        self.temperature_entry.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        translator_frame = ttk.LabelFrame(settings_frame,
                                          text=self.translate("translator_frame"),
                                          padding=5)
        translator_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        translator_frame.grid_columnconfigure(0, weight=0, minsize=160)
        translator_frame.grid_columnconfigure(1, weight=1)
        self.widgets_to_translate.append((translator_frame, "translator_frame", "text"))
        row = 0
        determinant_mode_label = ttk.Label(translator_frame,
                                           text=self.translate("determinant_mode_label"))
        determinant_mode_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((determinant_mode_label, "determinant_mode_label", "text"))
        self.determinant_mode_combobox = ttk.Combobox(translator_frame,
                                                      values=DETERMINANT_MODE_LIST,
                                                      state="readonly")
        self.determinant_mode_combobox.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        accurate_translation_label = ttk.Label(translator_frame,
                                               text=self.translate("accurate_translation_label"))
        accurate_translation_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((accurate_translation_label, "accurate_translation_label", "text"))
        self.accurate_translation_var = tk.BooleanVar(value=False)
        (ttk.Checkbutton(translator_frame, variable=self.accurate_translation_var).
         grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0)))
        row += 1
        deepl_key_label = ttk.Label(translator_frame, text=self.translate("deepl_key_label"))
        deepl_key_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((deepl_key_label, "deepl_key_label", "text"))
        self.deepl_key_entry = ttk.Entry(translator_frame)
        self.deepl_key_entry.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        request_language_label = ttk.Label(translator_frame,
                                           text=self.translate("request_language_label"))
        request_language_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((request_language_label,
                                          "request_language_label", "text"))
        self.request_language_entry = ttk.Entry(translator_frame)
        self.request_language_entry.insert(0, "en")
        self.request_language_entry.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        ocr_frame = ttk.LabelFrame(settings_frame, text=self.translate("ocr_frame"), padding=5)
        ocr_frame.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        ocr_frame.grid_columnconfigure(0, weight=0, minsize=160)
        ocr_frame.grid_columnconfigure(1, weight=1)
        self.widgets_to_translate.append((ocr_frame, "ocr_frame", "text"))
        row = 0
        languages_list_label = ttk.Label(ocr_frame, text=self.translate("languages_list_label"))
        languages_list_label.grid(row=row, column=0, sticky="nw", pady=2)
        self.widgets_to_translate.append((languages_list_label, "languages_list_label", "text"))
        self.lang_lst_text = tk.Text(ocr_frame,
                                     height=3,
                                     bg=BG_ENTRY,
                                     fg=FG_TEXT,
                                     insertbackground=FG_TEXT,
                                     relief="flat",
                                     borderwidth=1,
                                     highlightthickness=1,
                                     highlightbackground=BORDER,
                                     highlightcolor=BORDER,
                                     wrap="word")
        self.lang_lst_text.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        use_gpu_label = ttk.Label(ocr_frame, text=self.translate("use_gpu_label"))
        use_gpu_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((use_gpu_label, "use_gpu_label", "text"))
        self.use_gpu_ocr_var = tk.BooleanVar(value=False)
        (ttk.Checkbutton(ocr_frame, variable=self.use_gpu_ocr_var).
         grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0)))
        row += 1
        with_ocr_label = ttk.Label(ocr_frame, text=self.translate("with_ocr_label"))
        with_ocr_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((with_ocr_label, "with_ocr_label", "text"))
        self.with_ocr_var = tk.BooleanVar(value=False)
        (ttk.Checkbutton(ocr_frame, variable=self.with_ocr_var).
         grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0)))
        row += 1
        cloud_version_label = ttk.Label(ocr_frame, text=self.translate("cloud_version_label"))
        cloud_version_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((cloud_version_label, "cloud_version_label", "text"))
        self.cloud_version_var = tk.BooleanVar(value=False)
        (ttk.Checkbutton(ocr_frame, variable=self.cloud_version_var).
         grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0)))
        row += 1
        with_deepseek_label = ttk.Label(ocr_frame, text=self.translate("with_deepseek_label"))
        with_deepseek_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((with_deepseek_label, "with_deepseek_label", "text"))
        self.with_deepseek_var = tk.BooleanVar(value=True)
        (ttk.Checkbutton(ocr_frame, variable=self.with_deepseek_var).
         grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0)))
        row += 1
        model_size_label = ttk.Label(ocr_frame, text=self.translate("model_size_label"))
        model_size_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((model_size_label, "model_size_label", "text"))
        self.model_size_combobox = ttk.Combobox(ocr_frame,
                                                values=["tiny", "small", "base", "large", "gundam"],
                                                state="readonly")
        self.model_size_combobox.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        crop_mode_label = ttk.Label(ocr_frame, text=self.translate("crop_mode_label"))
        crop_mode_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((crop_mode_label, "crop_mode_label", "text"))
        self.crop_mode_var = tk.BooleanVar(value=False)
        (ttk.Checkbutton(ocr_frame, variable=self.crop_mode_var).
         grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0)))
        row += 1
        base_url_label = ttk.Label(ocr_frame, text=self.translate("base_url_label"))
        base_url_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((base_url_label, "base_url_label", "text"))
        self.base_url_entry = ttk.Entry(ocr_frame)
        self.base_url_entry.insert(0, "https://api.siliconflow.cn/v1/chat/completions")
        self.base_url_entry.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        api_key_deepseek_label = ttk.Label(ocr_frame, text=self.translate("api_key_deepseek_label"))
        api_key_deepseek_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((api_key_deepseek_label, "api_key_deepseek_label", "text"))
        self.deepseek_api_entry = ttk.Entry(ocr_frame)
        self.deepseek_api_entry.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        timeout_deepseek_label = ttk.Label(ocr_frame, text=self.translate("timeout_deepseek_label"))
        timeout_deepseek_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((timeout_deepseek_label, "timeout_deepseek_label", "text"))
        self.deepseek_timeout_entry = SpinEntry(ocr_frame, step=1, default=30)
        self.deepseek_timeout_entry.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        max_rate_limit_retries_label = ttk.Label(ocr_frame,
                                                 text=self.translate("max_rate_limit_retries_label"))
        max_rate_limit_retries_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((max_rate_limit_retries_label,
                                          "max_rate_limit_retries_label", "text"))
        self.max_rate_limit_retries_entry = SpinEntry(ocr_frame, step=1, default=3)
        self.max_rate_limit_retries_entry.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        other_frame = ttk.LabelFrame(settings_frame,
                                     text=self.translate("other_frame"), padding=5)
        other_frame.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
        other_frame.grid_columnconfigure(0, weight=0, minsize=160)
        other_frame.grid_columnconfigure(1, weight=1)
        self.widgets_to_translate.append((other_frame, "other_frame", "text"))
        row = 0
        filter_swearing_label = ttk.Label(other_frame,
                                          text=self.translate("filter_swearing_label"))
        filter_swearing_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((filter_swearing_label, "filter_swearing_label", "text"))
        self.filter_swearing_var = tk.BooleanVar(value=False)
        (ttk.Checkbutton(other_frame, variable=self.filter_swearing_var).
         grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0)))
        row += 1
        verbose_label = ttk.Label(other_frame, text=self.translate("verbose_label"))
        verbose_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((verbose_label, "verbose_label", "text"))
        self.verbose_var = tk.BooleanVar(value=False)
        (ttk.Checkbutton(other_frame, variable=self.verbose_var).
         grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0)))
        row += 1
        echo_label = ttk.Label(other_frame, text=self.translate("echo_label"))
        echo_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((echo_label, "echo_label", "text"))
        self.echo_var = tk.BooleanVar(value=False)
        (ttk.Checkbutton(other_frame, variable=self.echo_var).
         grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0)))
        row += 1
        type_computer_label = ttk.Label(other_frame, text=self.translate("type_computer_label"))
        type_computer_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((type_computer_label, "type_computer_label", "text"))
        self.type_computer_combobox = ttk.Combobox(other_frame, values=["auto"] +
                                                                       TYPES_POWER, state="readonly")
        self.type_computer_combobox.grid(row=row, column=1, sticky="ew", pady=2, padx=(5, 0))
        row += 1
        proprietary_algorithms_label = ttk.Label(other_frame,
                                                 text=self.translate("proprietary_algorithms_label"))
        proprietary_algorithms_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((proprietary_algorithms_label,
                                          "proprietary_algorithms_label", "text"))
        self.proprietary_algorithms_var = tk.BooleanVar(value=False)
        (ttk.Checkbutton(other_frame, variable=self.proprietary_algorithms_var).
         grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0)))
        row += 1
        writing_response_label = ttk.Label(other_frame, text=self.translate("writing_response_label"))
        writing_response_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((writing_response_label, "writing_response_label", "text"))
        self.writing_response_var = tk.BooleanVar(value=False)
        (ttk.Checkbutton(other_frame, variable=self.writing_response_var).
         grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0)))
        row += 1
        editing_files_label = ttk.Label(other_frame, text=self.translate("editing_files_label"))
        editing_files_label.grid(row=row, column=0, sticky="w", pady=2)
        self.widgets_to_translate.append((editing_files_label, "editing_files_label", "text"))
        self.editing_files_var = tk.BooleanVar(value=False)
        (ttk.Checkbutton(other_frame, variable=self.editing_files_var).
         grid(row=row, column=1, sticky="w", pady=2, padx=(5, 0)))
        row += 1

    def create_chat_panel(self):
        chat_frame = tk.Frame(self.root, bg=BG_MAIN)
        chat_frame.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)
        chat_frame.grid_rowconfigure(1, weight=1)
        chat_frame.grid_columnconfigure(0, weight=1)
        chat_title = ttk.Label(chat_frame,
                               text=self.translate("chat_title"),
                               font=FONT_TITLE)
        chat_title.grid(row=0, column=0, pady=(10, 5))
        self.widgets_to_translate.append((chat_title, "chat_title", "text"))
        self.resume_button = ttk.Button(chat_frame,
                                        text=self.translate("resume_button_text"),
                                        command=self.resume_request)
        self.resume_button.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 5))
        self.resume_button.grid_remove()
        self.widgets_to_translate.append((self.resume_button, "resume_button_text", "text"))
        messages_container = tk.Frame(chat_frame, bg=BG_FRAME)
        messages_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        messages_container.grid_rowconfigure(0, weight=1)
        messages_container.grid_columnconfigure(0, weight=1)
        self.messages_canvas = tk.Canvas(messages_container, bg=BG_FRAME, highlightthickness=0)
        self.messages_scrollbar = ttk.Scrollbar(messages_container,
                                                orient="vertical",
                                                command=self.messages_canvas.yview)
        self.messages_frame = tk.Frame(self.messages_canvas, bg=BG_FRAME)
        self.messages_frame.bind("<Configure>", lambda e: self.messages_canvas.
                                 configure(scrollregion=self.messages_canvas.bbox("all")))
        self.messages_canvas.create_window((0, 0), window=self.messages_frame, anchor="nw")
        self.messages_canvas.configure(yscrollcommand=self.messages_scrollbar.set)
        self.messages_canvas.pack(side="left", fill="both", expand=True)
        self.messages_scrollbar.pack(side="right", fill="y")
        self.messages_canvas.bind("<Enter>", self._bind_mousewheel_messages)
        self.messages_canvas.bind("<Leave>", self._unbind_mousewheel_messages)
        self.messages_canvas.bind("<Configure>", self._on_messages_canvas_configure)
        self.attached_frame = ttk.LabelFrame(chat_frame,
                                             text=self.translate("attached_files_label"),
                                             padding=5)
        self.attached_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        self.attached_frame.grid_columnconfigure(0, weight=1)
        self.widgets_to_translate.append((self.attached_frame, "attached_files_label", "text"))
        self.attached_textbox = tk.Text(self.attached_frame,
                                        height=3,
                                        bg=BG_ENTRY,
                                        fg=FG_TEXT,
                                        insertbackground=FG_TEXT,
                                        relief="flat",
                                        borderwidth=1,
                                        highlightthickness=1,
                                        highlightbackground=BORDER,
                                        highlightcolor=BORDER,
                                        state="disabled",
                                        wrap="word")
        self.attached_textbox.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        input_frame = ttk.Frame(chat_frame)
        input_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=5)
        input_frame.grid_columnconfigure(0, weight=1)
        self.request_entry = ttk.Entry(input_frame)
        self.request_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.request_entry.bind("<Return>", lambda event: self.send_message())
        upload_btn = ttk.Button(input_frame,
                                text=self.translate("upload_btn"),
                                command=self.upload_files)
        upload_btn.grid(row=0, column=1, padx=2)
        self.widgets_to_translate.append((upload_btn, "upload_btn", "text"))
        send_btn = ttk.Button(input_frame,
                              text=self.translate("send_btn"),
                              command=self.send_message)
        send_btn.grid(row=0, column=2, padx=2)
        self.widgets_to_translate.append((send_btn, "send_btn", "text"))
        copy_btn = ttk.Button(input_frame,
                              text=self.translate("copy_chat_btn"),
                              command=self.copy_chat)
        copy_btn.grid(row=0, column=3, padx=2)
        self.widgets_to_translate.append((copy_btn, "copy_chat_btn", "text"))

    def _on_messages_canvas_configure(self, event):
        self.messages_canvas.itemconfig(self.messages_canvas.find_withtag("all")[0], width=event.width)

    def _bind_mousewheel_messages(self, event):
        self.messages_canvas.bind_all("<MouseWheel>", self._on_mousewheel_messages)

    def _unbind_mousewheel_messages(self, event):
        self.messages_canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel_messages(self, event):
        self.messages_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _is_scrolled_to_bottom(self):
        if not hasattr(self, 'messages_canvas'):
            return True
        top, bottom = self.messages_canvas.yview()
        return bottom >= 0.99

    def create_history_panel(self):
        history_outer = tk.Frame(self.root, bg=BG_MAIN)
        history_outer.grid(row=0, column=2, sticky="nsew", padx=8, pady=8)
        history_outer.grid_rowconfigure(2, weight=1)
        history_outer.grid_columnconfigure(0, weight=1)
        title_frame = ttk.Frame(history_outer)
        title_frame.grid(row=0, column=0, sticky="ew", pady=(10, 5), padx=5)
        title_frame.grid_columnconfigure(0, weight=1)
        self.history_title = ttk.Label(title_frame,
                                       text=self.translate("history_title"),
                                       font=FONT_TITLE)
        self.history_title.grid(row=0, column=0, sticky="w")
        self.widgets_to_translate.append((self.history_title, "history_title", "text"))
        self.virtual_storage_var = tk.BooleanVar(value=False)
        vs_check = ttk.Checkbutton(title_frame,
                                   text=self.translate("virtual_storage_switch"),
                                   variable=self.virtual_storage_var,
                                   command=self.switch_mode)
        vs_check.grid(row=0, column=1, sticky="e", padx=10)
        self.widgets_to_translate.append((vs_check, "virtual_storage_switch", "text"))
        self.history_controls = ttk.Frame(history_outer)
        self.history_controls.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.history_controls.grid_columnconfigure(0, weight=1)
        self.history_controls.grid_columnconfigure(1, weight=1)
        self.history_controls.grid_columnconfigure(2, weight=1)
        self.find_story_entry = ttk.Entry(self.history_controls)
        self.find_story_entry.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 5))
        self.find_story_entry.bind("<KeyRelease>", lambda e: self.filter_history())
        add_btn = ttk.Button(self.history_controls,
                             text=self.translate("add_btn"),
                             width=6,
                             command=self.add_new_chat)
        add_btn.grid(row=1, column=0, sticky="ew", padx=2)
        self.widgets_to_translate.append((add_btn, "add_btn", "text"))
        delete_btn = ttk.Button(self.history_controls,
                                text=self.translate("delete_btn"),
                                width=6,
                                command=self.delete_current_chat)
        delete_btn.grid(row=1, column=1, sticky="ew", padx=2)
        self.widgets_to_translate.append((delete_btn, "delete_btn", "text"))
        download_btn = ttk.Button(self.history_controls,
                                  text=self.translate("download_btn"),
                                  width=6,
                                  command=self.download_chat)
        download_btn.grid(row=1, column=2, sticky="ew", padx=2)
        self.widgets_to_translate.append((download_btn, "download_btn", "text"))
        self.storage_controls = ttk.Frame(history_outer)
        self.storage_controls.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.storage_controls.grid_columnconfigure(0, weight=1)
        self.storage_controls.grid_columnconfigure(1, weight=1)
        self.storage_path_entry = ttk.Entry(self.storage_controls)
        self.storage_path_entry.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        browse_btn = ttk.Button(self.storage_controls,
                                text=self.translate("browse_btn"),
                                width=6,
                                command=self.browse_storage)
        browse_btn.grid(row=1, column=0, sticky="ew", padx=2)
        self.widgets_to_translate.append((browse_btn, "browse_btn", "text"))
        refresh_btn = ttk.Button(self.storage_controls,
                                 text=self.translate("refresh_btn"),
                                 width=6,
                                 command=self.refresh_storage)
        refresh_btn.grid(row=1, column=1, sticky="ew", padx=2)
        self.widgets_to_translate.append((refresh_btn, "refresh_btn", "text"))
        self.storage_controls.grid_remove()
        self.history_normal_frame = ScrollableFrame(history_outer)
        self.history_normal_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.history_tree_frame = tk.Frame(history_outer, bg=BG_FRAME)
        self.history_tree_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.history_tree_frame.grid_remove()
        self.current_chat_id = None
        self.chats = {}
        self.update_history_list()
        self.tree = None

    def show_welcome_placeholder(self):
        self.hide_welcome_placeholder()

        if not self.messages_frame.winfo_children():
            self.welcome_label = tk.Label(self.messages_frame, text=self.translate("welcome_text"),
                                         font=("Segoe UI", 12), fg=FG_DARK, bg=BG_FRAME,
                                         justify="center")
            self.welcome_label.pack(expand=True, fill="both")

    def hide_welcome_placeholder(self):
        if self.welcome_label is not None:
            self.welcome_label.destroy()
            self.welcome_label = None

    def clear_messages(self):
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
        self.welcome_label = None

    def update_attached_text(self):
        self.attached_textbox.config(state="normal")
        self.attached_textbox.delete("1.0", "end")

        if self.virtual_storage_var.get():
            self.attached_textbox.insert("1.0", self.translate("all_files_in_virtual_storage"))
        else:
            if self.attached_files:
                self.attached_textbox.insert("1.0", "\n".join(self.attached_files))

        self.attached_textbox.config(state="disabled")

    def switch_mode(self):
        if self.virtual_storage_var.get():
            self.history_controls.grid_remove()
            self.storage_controls.grid()
            self.history_title.config(text=self.translate("history_title_virtual"))
            self.history_normal_frame.grid_remove()
            self.history_tree_frame.grid()
            self.build_tree()
        else:
            self.storage_controls.grid_remove()
            self.history_controls.grid()
            self.history_title.config(text=self.translate("history_title"))
            self.history_tree_frame.grid_remove()
            self.history_normal_frame.grid()
            self.update_history_list()
        self.update_attached_text()

    def build_tree(self):
        if self.is_scanning:
            return
        self.is_scanning = True
        def worker():
            try:
                self.root.after(0, self._build_tree_ui)
            finally:
                self.is_scanning = False
        threading.Thread(target=worker, daemon=True).start()

    def _build_tree_ui(self):
        for widget in self.history_tree_frame.winfo_children():
            widget.destroy()

        if not self.storage_path or not os.path.isdir(self.storage_path):
            ttk.Label(self.history_tree_frame, text=self.translate("no_storage_path")).pack(pady=10)
            return

        tree_container = tk.Frame(self.history_tree_frame, bg=BG_FRAME)
        tree_container.pack(fill="both", expand=True)
        scrollbar = ttk.Scrollbar(tree_container, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        self.tree = ttk.Treeview(tree_container,
                                 yscrollcommand=scrollbar.set,
                                 selectmode="browse")
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
        self.virtual_tree_data = {}
        root_node = self.tree.insert("", "end",
                                     text=os.path.basename(self.storage_path),
                                     open=True)
        self.virtual_tree_data[root_node] = self.storage_path
        self._populate_tree(root_node, self.storage_path)
        self.tree.bind("<Double-1>", self.on_tree_double_click)

    def _populate_tree(self, parent, path):
        try:
            items = os.listdir(path)
        except PermissionError:
            return
        for item in items:
            full = os.path.join(path, item)

            if os.path.isdir(full):
                node = self.tree.insert(parent, "end", text=item, open=True)
                self.virtual_tree_data[node] = full
                self._populate_tree(node, full)
            else:
                node = self.tree.insert(parent, "end", text=item)
                self.virtual_tree_data[node] = full

    def on_tree_double_click(self, event):
        item = self.tree.selection()[0] if self.tree.selection() else None
        if item and item in self.virtual_tree_data:
            path = self.virtual_tree_data[item]

            if os.path.isfile(path):
                try:
                    if os.name == 'nt':
                        os.startfile(path)
                    else:
                        os.system(f'xdg-open "{path}"')
                except Exception as e:
                    logging.error(f"Failed to open file: {e}")

    def browse_storage(self):
        path = filedialog.askdirectory(title="Select Virtual Storage Folder")

        if path:
            self.storage_path = path
            self.storage_path_entry.delete(0, "end")
            self.storage_path_entry.insert(0, path)
            self.save_storage_path()
            self.build_tree()

    def refresh_storage(self):
        self.storage_path = self.storage_path_entry.get().strip()
        self.save_storage_path()
        self.build_tree()

    def update_history_list(self):
        for widget in self.history_normal_frame.get_frame().winfo_children():
            widget.destroy()
        for chat_id, chat_data in self.chats.items():
            messages = chat_data.get("messages", [])
            first_user_msg = next((m["content"] for m in messages if m.get("role") == "user"), "")
            title = first_user_msg[:30] + ("..." if len(first_user_msg) > 30 else "") \
                if first_user_msg else "Empty chat"
            created_at = chat_data.get("created_at", "Unknown date")
            btn_text = f"{created_at} - {title}"
            btn = tk.Button(self.history_normal_frame.get_frame(), text=btn_text,
                            command=lambda cid=chat_id: self.load_chat(cid),
                            anchor='w', justify='left', bg=BG_FRAME, fg=FG_TEXT,
                            relief='flat', activebackground=ACCENT_HOVER, activeforeground='white',
                            font=FONT_MAIN, padx=5, pady=2)
            btn.pack(fill="x", padx=5, pady=2)
        (self.history_normal_frame.canvas.
         configure(scrollregion=self.history_normal_frame.canvas.bbox("all")))
        self.history_normal_frame.canvas.yview_moveto(0.0)

    def filter_history(self):
        query = self.find_story_entry.get().lower()
        for widget in self.history_normal_frame.get_frame().winfo_children():
            widget.destroy()
        for chat_id, chat_data in self.chats.items():
            messages = chat_data.get("messages", [])
            first_user_msg = next((m["content"] for m in messages if m.get("role") == "user"), "")
            title = first_user_msg[:30] + ("..." if len(first_user_msg) > 30 else "") \
                if first_user_msg else "Empty chat"
            created_at = chat_data.get("created_at", "Unknown date")

            if query in f"{created_at} {title}".lower():
                btn = tk.Button(self.history_normal_frame.get_frame(), text=f"{created_at} - {title}",
                                command=lambda cid=chat_id: self.load_chat(cid),
                                anchor='w', justify='left', bg=BG_FRAME, fg=FG_TEXT,
                                relief='flat',
                                activebackground=ACCENT_HOVER,
                                activeforeground='white',
                                font=FONT_MAIN, padx=5, pady=2)
                btn.pack(fill="x", padx=5, pady=2)
        (self.history_normal_frame.canvas.
         configure(scrollregion=self.history_normal_frame.canvas.bbox("all")))
        self.history_normal_frame.canvas.yview_moveto(0.0)

    def add_new_chat(self):
        new_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.chats[new_id] = {
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "messages": []
        }
        self.current_chat_id = new_id
        self.save_chats_to_file()
        self.update_history_list()
        self.clear_messages()
        self.show_welcome_placeholder()
        self.resume_button.grid_remove()

    def delete_current_chat(self):
        if self.current_chat_id is not None and self.current_chat_id in self.chats:
            del self.chats[self.current_chat_id]
            self.current_chat_id = None
            self.clear_messages()
            self.show_welcome_placeholder()
            self.save_chats_to_file()
            self.update_history_list()
            self.resume_button.grid_remove()

    def load_chat(self, chat_id):
        self.current_chat_id = chat_id
        self.clear_messages()
        messages = self.chats[chat_id].get("messages", [])

        if not messages:
            self.show_welcome_placeholder()
        else:
            for msg in messages:
                role = msg.get("role")
                if role in ("user", "assistant"):
                    self.display_message(role, msg["content"], msg.get("timestamp", ""))
                elif role == "system":
                    self.display_log_message(msg["content"], save=False)
        self.check_pending_message()
        self.messages_canvas.yview_moveto(1.0)

    def display_message(self, role, content, timestamp=None):
        if role not in ("user", "assistant"):
            return

        if timestamp is None:
            timestamp = datetime.now().strftime("%H:%M")
        self.hide_welcome_placeholder()

        if role == "user":
            bg = "#3a3a3a"
        else:
            bg = "#2d2d2d"

        was_at_bottom = self._is_scrolled_to_bottom()

        bubble = tk.Frame(self.messages_frame, bg=bg, bd=0)
        bubble.pack(fill="x", padx=10, pady=5, anchor="e" if role == "user" else "w")
        canvas_width = self.messages_canvas.winfo_width()
        wrap_length = max(200, canvas_width - 50)
        label = tk.Label(bubble,
                         text=content,
                         wraplength=wrap_length,
                         justify="left",
                         fg=FG_TEXT, bg=bg, font=FONT_MAIN)
        label.pack(padx=10, pady=(10, 5), anchor="w")
        bottom = tk.Frame(bubble, bg=bg)
        bottom.pack(fill="x", padx=10, pady=(0, 5))
        time_label = tk.Label(bottom,
                              text=timestamp,
                              font=FONT_SMALL,
                              fg=FG_DARK,
                              bg=bg)
        time_label.pack(side="left")

        if was_at_bottom:
            self.messages_canvas.yview_moveto(1.0)

    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()

    def copy_chat(self):
        if self.current_chat_id is None or self.current_chat_id not in self.chats:
            return
        messages = self.chats[self.current_chat_id].get("messages", [])

        if not messages:
            return

        lines = []
        for msg in messages:
            role = msg.get("role")
            content = msg.get("content", "")

            if role == "system":
                prefix = "LOG"
            else:
                prefix = role.capitalize()

            lines.append(f"{prefix}: {content}")
        text = "\n".join(lines)
        self.copy_to_clipboard(text)
        messagebox.showinfo(self.translate("success_info"),
                            self.translate("chat_saved"))

    def send_message(self):
        if self.is_busy:
            messagebox.showinfo(self.translate("success_info"),
                                self.translate("info_ai_busy"))
            return
        user_text = self.request_entry.get().strip()

        if not user_text:
            return

        if self.current_chat_id is None:
            self.add_new_chat()

        self.hide_welcome_placeholder()
        self.request_entry.delete(0, "end")
        now = datetime.now().strftime("%H:%M")
        self.display_message("user", user_text, now)

        if self.current_chat_id is not None:
            if self.current_chat_id not in self.chats:
                self.chats[self.current_chat_id] = {
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "messages": []
                }
            (self.chats[self.current_chat_id]["messages"].
             append({"role": "user", "content": user_text, "timestamp": now}))
            self.save_chats_to_file()
            self.update_history_list()

        self.resume_button.grid_remove()
        self.is_busy = True
        thread = threading.Thread(target=self.process_request, args=(user_text,))
        thread.daemon = True
        thread.start()

    def collect_parameters(self):
        def parse_textbox_list(widget):
            text = widget.get("1.0", "end-1c").strip()

            if not text:
                return []
            return [line.strip() for line in text.splitlines() if line.strip()]

        virtual_storage = self.virtual_storage_var.get()
        virtual_storage_path = self.storage_path if virtual_storage else None
        additional = []

        if virtual_storage and self.storage_path and os.path.isdir(self.storage_path):
            for root, dirs, files in os.walk(self.storage_path):
                for f in files:
                    additional.append(os.path.join(root, f))
        elif self.attached_files:
            additional = self.attached_files.copy()

        params = {
            "request": self.request_entry.get().strip(),
            "preferences_in_ai": self.preferences_combobox.get(),
            "filter_for_swearing": self.filter_swearing_var.get(),
            "additional_files": additional if additional else None,
            "models_dir": self.models_dir_entry.get().strip() or "./models",
            "with_ai_orchestrator": self.with_ai_orchestrator_var.get(),
            "verbose": self.verbose_var.get(),
            "n_ctx": self.n_ctx_entry.get_int(default=0) or None,
            "n_gpu_layers": self.n_gpu_layers_entry.get_int(default=0),
            "echo": self.echo_var.get(),
            "max_tokens": self.max_tokens_entry.get_int(default=4096),
            "your_token_for_hf": self.token_hf_entry.get().strip() or None,
            "subdomain": self.subdomain_entry.get().strip() or "",
            "country": self.country_entry.get().strip() or None,
            "protocol": self.protocol_combobox.get(),
            "max_timeout": self.max_timeout_entry.get_int(default=30),
            "is_working": self.is_working_var.get(),
            "type_computer": self.type_computer_combobox.get()
            if self.type_computer_combobox.get() != "auto" else None,
            "auto_proxies": self.auto_proxies_var.get(),
            "writing_response_to_file": self.writing_response_var.get(),
            "editing_files": self.editing_files_var.get(),
            "your_proxies_dict": parse_textbox_list(self.your_proxies_dict_text) or None,
            "determinant_mode": self.determinant_mode_combobox.get(),
            "accurate_translation": self.accurate_translation_var.get(),
            "your_key_for_deepl": self.deepl_key_entry.get().strip() or "",
            "proprietary_algorithms": self.proprietary_algorithms_var.get(),
            "repo_id": self.repo_id_entry.get().strip() or None,
            "filename": self.filename_entry.get().strip() or None,
            "min_timeout_for_checking_availability": self.min_timeout_entry.get_int(default=5),
            "max_timeout_for_checking_availability": self.max_timeout_entry.get_int(default=15),
            "request_language": self.request_language_entry.get().strip() or "en",
            "main_prompt_mode": self.main_prompt_mode_combobox.get(),
            "main_prompt": self.main_prompt_text.get("1.0", "end-1c").strip() or None,
            "temperature": self.temperature_entry.get_float(default=0.1),
            "retries": self.retries_entry.get_int(default=3),
            "github_proxies": self.github_proxies_var.get(),
            "url_lst": parse_textbox_list(self.url_lst_text) or None,
            "proxy_retries": self.proxy_retries_entry.get_int(default=3),
            "main_retries": self.main_retries_entry.get_int(default=3),
            "lang_lst": parse_textbox_list(self.lang_lst_text) or None,
            "use_gpu_for_ocr": self.use_gpu_ocr_var.get(),
            "virtual_storage": virtual_storage,
            "virtual_storage_path": virtual_storage_path,
            "with_ocr": self.with_ocr_var.get(),
            "cloud_version": self.cloud_version_var.get(),
            "with_deepseek": self.with_deepseek_var.get(),
            "model_size": self.model_size_combobox.get(),
            "crop_mode": self.crop_mode_var.get(),
            "base_url": self.base_url_entry.get().strip(),
            "api_key_for_deepseek_ocr": self.deepseek_api_entry.get().strip() or None,
            "timeout_for_deepseek_ocr": self.deepseek_timeout_entry.get_int(default=30) or None,
            "max_rate_limit_retries": self.max_rate_limit_retries_entry.get_int(default=3),
            "prefer_mirror": self.prefer_mirror_var.get()
        }
        return params

    def process_request(self, user_text):
        try:
            params = self.collect_parameters()
            params["request"] = user_text
            alex = BiNeuron(**params)
            answer = alex.final_ai_request()
            self.message_queue.put(("response", answer))
        except Exception as e:
            error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
            self.message_queue.put(("error", error_msg))
        finally:
            self.message_queue.put(("done", None))

    def poll_queue(self):
        try:
            while True:
                msg_type, data = self.message_queue.get_nowait()

                if msg_type == "response":
                    now = datetime.now().strftime("%H:%M")
                    self.display_message("assistant", data, now)

                    if self.current_chat_id is not None:
                        if self.current_chat_id in self.chats:
                            (self.chats[self.current_chat_id]["messages"].
                             append({"role": "assistant", "content": data, "timestamp": now}))
                            self.save_chats_to_file()
                            self.update_history_list()
                            self.resume_button.grid_remove()
                elif msg_type == "error":
                    messagebox.showerror(self.translate("error_occurred"), data)
                elif msg_type == "done":
                    self.is_busy = False

        except queue.Empty:
            pass
        self.root.after(100, self.poll_queue)

    def check_pending_message(self):
        self.resume_button.grid_remove()

        if self.current_chat_id is None or self.current_chat_id not in self.chats:
            return
        messages = self.chats[self.current_chat_id].get("messages", [])

        if not messages:
            return

        last_user_idx = -1
        for i, msg in enumerate(messages):
            if msg.get("role") == "user":
                last_user_idx = i

        if last_user_idx == -1:
            return

        if last_user_idx == len(messages) - 1:
            self.resume_button.grid()
            self.resume_button.config(text=self.translate("resume_button_text"))
        else:
            self.resume_button.grid_remove()

    def resume_request(self):
        if self.is_busy:
            return

        if self.current_chat_id is None:
            return

        messages = self.chats[self.current_chat_id].get("messages", [])
        last_user_msg = None
        for msg in reversed(messages):
            if msg.get("role") == "user":
                last_user_msg = msg["content"]
                break

        if last_user_msg is None:
            return

        if messages and messages[-1].get("role") == "assistant":
            messages.pop()
            self.save_chats_to_file()
            self.load_chat(self.current_chat_id)

        self.resume_button.grid_remove()
        self.is_busy = True
        thread = threading.Thread(target=self.process_request, args=(last_user_msg,))
        thread.daemon = True
        thread.start()

    def export_all_chats(self):
        if not self.chats:
            messagebox.showinfo(self.translate("success_info"), self.translate("no_chats"))
            return

        folder = filedialog.askdirectory(title="Select folder to export all chats")

        if not folder:
            return

        count = 0
        for chat_id, chat_data in self.chats.items():
            messages = chat_data.get("messages", [])

            if not messages:
                continue

            first_user = next((m["content"] for m in messages if m.get("role") == "user"), "empty")
            safe_title = "".join(c for c in first_user[:30] if c.isalnum() or c in (' ', '_')).strip()

            if not safe_title:
                safe_title = "chat"

            timestamp = chat_data.get("created_at", "unknown").replace(":", "-").replace(" ", "_")
            filename = f"{timestamp}_{safe_title}.txt"
            filepath = os.path.join(folder, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                for msg in messages:
                    f.write(f"{msg['role'].capitalize()}: {msg['content']}\n")
            count += 1
        messagebox.showinfo(self.translate("export_success"),
                            self.translate("export_all_success",
                                           count=count, folder=folder))

    def delete_all_chats(self):
        if not self.chats:
            return

        if not messagebox.askyesno(self.translate("delete_all_title"),
                                   self.translate("delete_all_confirm")):
            return

        self.chats.clear()
        self.add_new_chat()
        self.save_chats_to_file()
        self.update_history_list()
        self.resume_button.grid_remove()

    def download_chat(self):
        if self.current_chat_id is None:
            messagebox.showwarning(self.translate("warning_info"),
                                   self.translate("no_chat_selected"))
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                for msg in self.chats[self.current_chat_id]["messages"]:
                    f.write(f"{msg['role'].capitalize()}: {msg['content']}\n")
            messagebox.showinfo(self.translate("success_info"), self.translate("chat_saved"))

    def upload_files(self):
        if self.virtual_storage_var.get():
            messagebox.showinfo(self.translate("success_info"),
                                self.translate("info_virtual_storage_active"))
            return

        files = filedialog.askopenfilenames()

        if files:
            self.attached_files = list(files)
            self.update_attached_text()


if __name__ == "__main__":
    root = tk.Tk()
    app = BiNeuronGUI(root)
    root.mainloop()