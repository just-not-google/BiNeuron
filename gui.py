from tkinter import filedialog, messagebox, ttk
import threading
import queue
import logging
import traceback
import json
import os
from datetime import datetime
import customtkinter as ctk
from AlexRadar import AlexRadar
from AlexRadar.data.constants_for_functions import (HTTP_PROTOCOL, HTTPS_PROTOCOL,
                                                    TYPES_POWER,PREFERENCES_IN_AI_LIST,
                                                    DETERMINANT_MODE_LIST)
from AlexRadar.data.variants_industrial_scenarios import ALL_MAIN_PROMPTS
from AlexRadar.data.natural_languages import NATURAL_LANGUAGES

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

COLOR_BG = ("#f0f0f0", "#1a1a1a")
COLOR_FRAME = ("#e8e8e8", "#252525")
COLOR_FRAME_DARK = ("#dcdcdc", "#2e2e2e")
COLOR_ENTRY = ("#ffffff", "#2d2d2d")
COLOR_TEXTBOX = ("#fafafa", "#1f1f1f")
COLOR_BUTTON = ("#d0d0d0", "#3a3a3a")
COLOR_BUTTON_HOVER = ("#b0b0b0", "#505050")
COLOR_BORDER = ("#aaaaaa", "#444444")
COLOR_SELECT = ("#888888", "#666666")
COLOR_SWITCH = ("#999999", "#555555")

FRAME_CORNER = 10
LABEL_FONT = ("Segoe UI", 13)
TITLE_FONT = ("Segoe UI", 18, "bold")
SECTION_FONT = ("Segoe UI", 15, "bold")
SMALL_FONT = ("Segoe UI", 10)

def validate_number(char, current_value):
    if char == "":
        return True
    if char.isdigit() or char == ".":
        if char == "." and "." in current_value:
            return False
        return True
    return False

class NumericEntry(ctk.CTkEntry):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        vcmd = (self.register(self._validate), "%P", "%s")
        self.configure(validate="key", validatecommand=vcmd)

    def _validate(self, new_value, old_value):
        if new_value == "":
            return True
        if new_value.replace(".", "", 1).isdigit():
            if new_value.count(".") > 1:
                return False
            return True
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

class SpinEntry(ctk.CTkFrame):
    def __init__(self, master, step=1, default=0, **kwargs):
        super().__init__(master, fg_color="transparent")
        self.step = step
        self.entry = NumericEntry(self, **kwargs)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.entry.insert(0, str(default))

        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(side="left")
        self.btn_up = ctk.CTkButton(
            self.btn_frame, text="▲", width=25, height=20,
            command=self.increment,
            fg_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER,
            text_color=("black", "white"), corner_radius=4
        )
        self.btn_up.pack(side="top", pady=1)
        self.btn_down = ctk.CTkButton(
            self.btn_frame, text="▼", width=25, height=20,
            command=self.decrement,
            fg_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER,
            text_color=("black", "white"), corner_radius=4
        )
        self.btn_down.pack(side="top", pady=1)

    def increment(self):
        try:
            val = float(self.entry.get())
        except:
            val = 0.0
        val += self.step
        self._set_value(val)

    def decrement(self):
        try:
            val = float(self.entry.get())
        except:
            val = 0.0
        val -= self.step
        self._set_value(val)

    def _set_value(self, val):
        if self.step == int(self.step):
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

class AlexRadarGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AlexRadar")
        self.root.geometry("1500x900")
        self.root.minsize(1200, 700)

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

        self.root.grid_columnconfigure(0, weight=1, uniform="main")
        self.root.grid_columnconfigure(1, weight=3, uniform="main")
        self.root.grid_columnconfigure(2, weight=1, uniform="main")
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

        self.tree_style_configured = False
        self.setup_tree_style()

        self.load_settings()

    def setup_logging(self):
        class TextHandler(logging.Handler):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget
            def emit(self, record):
                msg = self.format(record)
                self.text_widget.after(0, self.text_widget.insert, "end", msg + "\n")
                self.text_widget.after(0, self.text_widget.see, "end")
        logger = logging.getLogger("AlexRadar")
        logger.setLevel(logging.INFO)
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        handler = TextHandler(self.logs_textbox)
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(handler)

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
            "theme": self.theme_option_menu.get(),
            "language": self.language_option_menu.get(),
            "country": self.country_entry.get(),
            "protocol": self.protocol_option_menu.get(),
            "max_timeout": self.max_timeout_entry.get(),
            "is_working": str(self.is_working_checkbox.get()),
            "auto_proxies": str(self.auto_proxies_checkbox.get()),
            "your_proxies_dict": self.your_proxies_dict_textbox.get("1.0", "end-1c"),
            "min_timeout_for_checking_availability": self.min_timeout_for_checking_availability_entry.get(),
            "max_timeout_for_checking_availability": self.max_timeout_for_checking_availability_entry.get(),
            "retries": self.retries_entry.get(),
            "github_proxies": str(self.github_proxies_checkbox.get()),
            "url_lst": self.url_lst_textbox.get("1.0", "end-1c"),
            "proxy_retries": self.proxy_retries_entry.get(),
            "main_retries": self.main_retries_entry.get(),
            "preferences_in_ai": self.preferences_in_ai_option_menu.get(),
            "models_dir": self.models_dir_entry.get(),
            "with_ai_orchestrator": str(self.with_ai_orchestrator_checkbox.get()),
            "n_ctx": self.n_ctx_entry.get(),
            "n_gpu_layers": self.n_gpu_layers_entry.get(),
            "max_tokens": self.max_tokens_entry.get(),
            "your_token_for_hf": self.your_token_for_hf_entry.get(),
            "subdomain": self.subdomain_entry.get(),
            "repo_id": self.repo_id_entry.get(),
            "filename": self.filename_entry.get(),
            "prefer_mirror": str(self.prefer_mirror_checkbox.get()),
            "main_prompt_mode": self.main_prompt_mode_option_menu.get(),
            "main_prompt": self.main_prompt_textbox.get("1.0", "end-1c"),
            "temperature": self.temperature_entry.get(),
            "determinant_mode": self.determinant_mode_option_menu.get(),
            "accurate_translation": str(self.accurate_translation_checkbox.get()),
            "your_key_for_deepl": self.your_key_for_deepl_entry.get(),
            "request_language": self.request_language_entry.get(),
            "lang_lst": self.lang_lst_textbox.get("1.0", "end-1c"),
            "use_gpu_for_ocr": str(self.use_gpu_for_ocr_checkbox.get()),
            "with_ocr": str(self.with_ocr_checkbox.get()),
            "cloud_version": str(self.cloud_version_checkbox.get()),
            "with_deepseek": str(self.with_deepseek_checkbox.get()),
            "model_size": self.model_size_option_menu.get(),
            "crop_mode": str(self.crop_mode_checkbox.get()),
            "base_url": self.base_url_entry.get(),
            "api_key_for_deepseek_ocr": self.api_key_for_deepseek_ocr_entry.get(),
            "timeout_for_deepseek_ocr": self.timeout_for_deepseek_ocr_entry.get(),
            "max_rate_limit_retries": self.max_rate_limit_retries_entry.get(),
            "filter_for_swearing": str(self.filter_for_swearing_checkbox.get()),
            "verbose": str(self.verbose_checkbox.get()),
            "echo": str(self.echo_checkbox.get()),
            "type_computer": self.type_computer_option_menu.get(),
            "proprietary_algorithms": str(self.proprietary_algorithms_checkbox.get()),
            "writing_response_to_file": str(self.writing_response_to_file_checkbox.get()),
            "virtual_storage": str(self.mode_switch.get()),
            "storage_path": self.storage_path,
        }

    def set_all_settings(self, settings):
        if "theme" in settings:
            self.theme_option_menu.set(settings["theme"])
            ctk.set_appearance_mode(settings["theme"])
            self.update_tree_style()
        if "language" in settings:
            self.language_option_menu.set(settings["language"])
        if "country" in settings:
            self.country_entry.delete(0, "end")
            self.country_entry.insert(0, settings["country"])
        if "protocol" in settings:
            self.protocol_option_menu.set(settings["protocol"])
        if "max_timeout" in settings:
            self.max_timeout_entry.delete(0, "end")
            self.max_timeout_entry.insert(0, settings["max_timeout"])
        if "is_working" in settings:
            if settings["is_working"] == "1":
                self.is_working_checkbox.select()
            else:
                self.is_working_checkbox.deselect()
        if "auto_proxies" in settings:
            if settings["auto_proxies"] == "1":
                self.auto_proxies_checkbox.select()
            else:
                self.auto_proxies_checkbox.deselect()
        if "your_proxies_dict" in settings:
            self.your_proxies_dict_textbox.delete("1.0", "end")
            self.your_proxies_dict_textbox.insert("1.0", settings["your_proxies_dict"])
        if "min_timeout_for_checking_availability" in settings:
            self.min_timeout_for_checking_availability_entry.delete(0, "end")
            self.min_timeout_for_checking_availability_entry.insert(0, settings["min_timeout_for_checking_availability"])
        if "max_timeout_for_checking_availability" in settings:
            self.max_timeout_for_checking_availability_entry.delete(0, "end")
            self.max_timeout_for_checking_availability_entry.insert(0, settings["max_timeout_for_checking_availability"])
        if "retries" in settings:
            self.retries_entry.delete(0, "end")
            self.retries_entry.insert(0, settings["retries"])
        if "github_proxies" in settings:
            if settings["github_proxies"] == "1":
                self.github_proxies_checkbox.select()
            else:
                self.github_proxies_checkbox.deselect()
        if "url_lst" in settings:
            self.url_lst_textbox.delete("1.0", "end")
            self.url_lst_textbox.insert("1.0", settings["url_lst"])
        if "proxy_retries" in settings:
            self.proxy_retries_entry.delete(0, "end")
            self.proxy_retries_entry.insert(0, settings["proxy_retries"])
        if "main_retries" in settings:
            self.main_retries_entry.delete(0, "end")
            self.main_retries_entry.insert(0, settings["main_retries"])
        if "preferences_in_ai" in settings:
            self.preferences_in_ai_option_menu.set(settings["preferences_in_ai"])
        if "models_dir" in settings:
            self.models_dir_entry.delete(0, "end")
            self.models_dir_entry.insert(0, settings["models_dir"])
        if "with_ai_orchestrator" in settings:
            if settings["with_ai_orchestrator"] == "1":
                self.with_ai_orchestrator_checkbox.select()
            else:
                self.with_ai_orchestrator_checkbox.deselect()
        if "n_ctx" in settings:
            self.n_ctx_entry.delete(0, "end")
            self.n_ctx_entry.insert(0, settings["n_ctx"])
        if "n_gpu_layers" in settings:
            self.n_gpu_layers_entry.delete(0, "end")
            self.n_gpu_layers_entry.insert(0, settings["n_gpu_layers"])
        if "max_tokens" in settings:
            self.max_tokens_entry.delete(0, "end")
            self.max_tokens_entry.insert(0, settings["max_tokens"])
        if "your_token_for_hf" in settings:
            self.your_token_for_hf_entry.delete(0, "end")
            self.your_token_for_hf_entry.insert(0, settings["your_token_for_hf"])
        if "subdomain" in settings:
            self.subdomain_entry.delete(0, "end")
            self.subdomain_entry.insert(0, settings["subdomain"])
        if "repo_id" in settings:
            self.repo_id_entry.delete(0, "end")
            self.repo_id_entry.insert(0, settings["repo_id"])
        if "filename" in settings:
            self.filename_entry.delete(0, "end")
            self.filename_entry.insert(0, settings["filename"])
        if "prefer_mirror" in settings:
            if settings["prefer_mirror"] == "1":
                self.prefer_mirror_checkbox.select()
            else:
                self.prefer_mirror_checkbox.deselect()
        if "main_prompt_mode" in settings:
            self.main_prompt_mode_option_menu.set(settings["main_prompt_mode"])
        if "main_prompt" in settings:
            self.main_prompt_textbox.delete("1.0", "end")
            self.main_prompt_textbox.insert("1.0", settings["main_prompt"])
        if "temperature" in settings:
            self.temperature_entry.delete(0, "end")
            self.temperature_entry.insert(0, settings["temperature"])
        if "determinant_mode" in settings:
            self.determinant_mode_option_menu.set(settings["determinant_mode"])
        if "accurate_translation" in settings:
            if settings["accurate_translation"] == "1":
                self.accurate_translation_checkbox.select()
            else:
                self.accurate_translation_checkbox.deselect()
        if "your_key_for_deepl" in settings:
            self.your_key_for_deepl_entry.delete(0, "end")
            self.your_key_for_deepl_entry.insert(0, settings["your_key_for_deepl"])
        if "request_language" in settings:
            self.request_language_entry.delete(0, "end")
            self.request_language_entry.insert(0, settings["request_language"])
        if "lang_lst" in settings:
            self.lang_lst_textbox.delete("1.0", "end")
            self.lang_lst_textbox.insert("1.0", settings["lang_lst"])
        if "use_gpu_for_ocr" in settings:
            if settings["use_gpu_for_ocr"] == "1":
                self.use_gpu_for_ocr_checkbox.select()
            else:
                self.use_gpu_for_ocr_checkbox.deselect()
        if "with_ocr" in settings:
            if settings["with_ocr"] == "1":
                self.with_ocr_checkbox.select()
            else:
                self.with_ocr_checkbox.deselect()
        if "cloud_version" in settings:
            if settings["cloud_version"] == "1":
                self.cloud_version_checkbox.select()
            else:
                self.cloud_version_checkbox.deselect()
        if "with_deepseek" in settings:
            if settings["with_deepseek"] == "1":
                self.with_deepseek_checkbox.select()
            else:
                self.with_deepseek_checkbox.deselect()
        if "model_size" in settings:
            self.model_size_option_menu.set(settings["model_size"])
        if "crop_mode" in settings:
            if settings["crop_mode"] == "1":
                self.crop_mode_checkbox.select()
            else:
                self.crop_mode_checkbox.deselect()
        if "base_url" in settings:
            self.base_url_entry.delete(0, "end")
            self.base_url_entry.insert(0, settings["base_url"])
        if "api_key_for_deepseek_ocr" in settings:
            self.api_key_for_deepseek_ocr_entry.delete(0, "end")
            self.api_key_for_deepseek_ocr_entry.insert(0, settings["api_key_for_deepseek_ocr"])
        if "timeout_for_deepseek_ocr" in settings:
            self.timeout_for_deepseek_ocr_entry.delete(0, "end")
            self.timeout_for_deepseek_ocr_entry.insert(0, settings["timeout_for_deepseek_ocr"])
        if "max_rate_limit_retries" in settings:
            self.max_rate_limit_retries_entry.delete(0, "end")
            self.max_rate_limit_retries_entry.insert(0, settings["max_rate_limit_retries"])
        if "filter_for_swearing" in settings:
            if settings["filter_for_swearing"] == "1":
                self.filter_for_swearing_checkbox.select()
            else:
                self.filter_for_swearing_checkbox.deselect()
        if "verbose" in settings:
            if settings["verbose"] == "1":
                self.verbose_checkbox.select()
            else:
                self.verbose_checkbox.deselect()
        if "echo" in settings:
            if settings["echo"] == "1":
                self.echo_checkbox.select()
            else:
                self.echo_checkbox.deselect()
        if "type_computer" in settings:
            self.type_computer_option_menu.set(settings["type_computer"])
        if "proprietary_algorithms" in settings:
            if settings["proprietary_algorithms"] == "1":
                self.proprietary_algorithms_checkbox.select()
            else:
                self.proprietary_algorithms_checkbox.deselect()
        if "writing_response_to_file" in settings:
            if settings["writing_response_to_file"] == "1":
                self.writing_response_to_file_checkbox.select()
            else:
                self.writing_response_to_file_checkbox.deselect()
        if "virtual_storage" in settings:
            if settings["virtual_storage"] == "1":
                self.mode_switch.select()
            else:
                self.mode_switch.deselect()
            self.switch_mode()
        if "storage_path" in settings:
            self.storage_path = settings["storage_path"]
            self.storage_path_entry.delete(0, "end")
            self.storage_path_entry.insert(0, self.storage_path)
            self.save_storage_path()
            if self.mode_switch.get() == 1:
                self.build_tree()

        self.update_attached_text()

    def set_default_settings(self):
        default = {
            "theme": "dark",
            "language": list(NATURAL_LANGUAGES.keys())[0],
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
        messagebox.showinfo("Settings", "Settings have been reset to default.")

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

    def show_welcome_placeholder(self):
        self.hide_welcome_placeholder()
        if not self.messages_frame.winfo_children():
            self.welcome_label = ctk.CTkLabel(
                self.messages_frame,
                text="Welcome to AlexRadar! How can I help?\n"
                     "(The GUI was created using the CLI version of the app)",
                font=("Segoe UI", 16),
                text_color=("gray60", "gray60"),
                justify="center"
            )
            self.welcome_label.pack(expand=True, fill="both")

    def hide_welcome_placeholder(self):
        if self.welcome_label is not None:
            self.welcome_label.destroy()
            self.welcome_label = None

    def clear_messages(self):
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
        self.welcome_label = None

    def setup_tree_style(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.update_tree_style()

    def update_tree_style(self):
        mode = ctk.get_appearance_mode()
        if mode == "Dark":
            bg = "#252525"
            fg = "white"
            sel_bg = "#3a3a3a"
            sel_fg = "white"
            arrow_color = "#666666"
        else:
            bg = "#e8e8e8"
            fg = "black"
            sel_bg = "#d0d0d0"
            sel_fg = "black"
            arrow_color = "#888888"

        self.style.configure("Treeview",
                             background=bg,
                             foreground=fg,
                             fieldbackground=bg,
                             borderwidth=0,
                             highlightthickness=0,
                             font=("Segoe UI", 11))
        self.style.configure("Treeview.Item", background=bg, foreground=fg)
        self.style.map("Treeview",
                       background=[("selected", sel_bg)],
                       foreground=[("selected", sel_fg)])
        self.style.configure("Treeview.Heading",
                             background=bg,
                             foreground=fg,
                             borderwidth=0,
                             relief="flat",
                             font=("Segoe UI", 11, "bold"))
        self.style.map("Treeview.Heading",
                       background=[("active", sel_bg)],
                       foreground=[("active", fg)])
        self.style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
        self.tree_style_configured = True

    def create_settings_panel(self):
        settings_frame = ctk.CTkScrollableFrame(self.root, width=420, corner_radius=FRAME_CORNER, fg_color="transparent")
        settings_frame.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        settings_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(settings_frame, text="Settings", font=TITLE_FONT, text_color=("black", "white")).grid(row=0, column=0, pady=(10, 5))

        reset_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        reset_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 10))
        reset_frame.grid_columnconfigure(0, weight=1)
        reset_frame.grid_columnconfigure(1, weight=1)
        reset_frame.grid_columnconfigure(2, weight=1)

        reset_btn = ctk.CTkButton(reset_frame, text="Reset", corner_radius=8,
                                  fg_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER,
                                  text_color=("black", "white"), command=self.reset_settings)
        reset_btn.grid(row=0, column=0, sticky="ew", padx=2)

        export_all_btn = ctk.CTkButton(reset_frame, text="Export All", corner_radius=8,
                                       fg_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER,
                                       text_color=("black", "white"), command=self.export_all_chats)
        export_all_btn.grid(row=0, column=1, sticky="ew", padx=2)

        delete_all_btn = ctk.CTkButton(reset_frame, text="Delete All", corner_radius=8,
                                       fg_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER,
                                       text_color=("black", "white"), command=self.delete_all_chats)
        delete_all_btn.grid(row=0, column=2, sticky="ew", padx=2)

        interface_frame = ctk.CTkFrame(settings_frame, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME)
        interface_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        interface_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(interface_frame, text="Interface", font=SECTION_FONT, text_color=("black", "white")).grid(row=0, column=0, pady=(8, 5), padx=10, sticky="w")
        interface_subframe = ctk.CTkFrame(interface_frame, fg_color="transparent", corner_radius=0)
        interface_subframe.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        interface_subframe.grid_columnconfigure(0, weight=0, minsize=140)
        interface_subframe.grid_columnconfigure(1, weight=1)

        row = 0
        ctk.CTkLabel(interface_subframe, text="Theme", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.theme_option_menu = ctk.CTkOptionMenu(interface_subframe, values=["dark", "light", "system"],
                                                   command=self.change_theme,
                                                   corner_radius=8, fg_color=COLOR_BUTTON,
                                                   button_color=COLOR_BUTTON, button_hover_color=COLOR_BUTTON_HOVER,
                                                   dropdown_fg_color=COLOR_FRAME_DARK,
                                                   dropdown_hover_color=COLOR_BUTTON_HOVER,
                                                   text_color=("black", "white"))
        self.theme_option_menu.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(interface_subframe, text="Language", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.language_option_menu = ctk.CTkOptionMenu(interface_subframe, values=list(NATURAL_LANGUAGES.keys()), corner_radius=8,
                                                      fg_color=COLOR_BUTTON, button_color=COLOR_BUTTON,
                                                      button_hover_color=COLOR_BUTTON_HOVER,
                                                      dropdown_fg_color=COLOR_FRAME_DARK,
                                                      dropdown_hover_color=COLOR_BUTTON_HOVER,
                                                      text_color=("black", "white"))
        self.language_option_menu.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        network_frame = ctk.CTkFrame(settings_frame, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME)
        network_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        network_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(network_frame, text="Network", font=SECTION_FONT, text_color=("black", "white")).grid(row=0, column=0, pady=(8, 5), padx=10, sticky="w")
        network_subframe = ctk.CTkFrame(network_frame, fg_color="transparent", corner_radius=0)
        network_subframe.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        network_subframe.grid_columnconfigure(0, weight=0, minsize=140)
        network_subframe.grid_columnconfigure(1, weight=1)

        row = 0
        ctk.CTkLabel(network_subframe, text="Country", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.country_entry = ctk.CTkEntry(network_subframe, corner_radius=8, fg_color=COLOR_ENTRY,
                                          border_color=COLOR_BORDER, text_color=("black", "white"))
        self.country_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(network_subframe, text="Protocol", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.protocol_option_menu = ctk.CTkOptionMenu(network_subframe, values=[HTTP_PROTOCOL, HTTPS_PROTOCOL], corner_radius=8,
                                                      fg_color=COLOR_BUTTON, button_color=COLOR_BUTTON,
                                                      button_hover_color=COLOR_BUTTON_HOVER,
                                                      dropdown_fg_color=COLOR_FRAME_DARK,
                                                      dropdown_hover_color=COLOR_BUTTON_HOVER,
                                                      text_color=("black", "white"))
        self.protocol_option_menu.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(network_subframe, text="Max Timeout", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.max_timeout_entry = SpinEntry(network_subframe, step=1, default=30, corner_radius=8,
                                           fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                           text_color=("black", "white"))
        self.max_timeout_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(network_subframe, text="Is Working", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.is_working_checkbox = ctk.CTkCheckBox(network_subframe, text="", corner_radius=6,
                                                   fg_color=COLOR_SWITCH, hover_color=COLOR_BUTTON_HOVER,
                                                   border_color=COLOR_BORDER, checkmark_color=("black", "white"))
        self.is_working_checkbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(network_subframe, text="Auto Proxies", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.auto_proxies_checkbox = ctk.CTkCheckBox(network_subframe, text="", corner_radius=6,
                                                     fg_color=COLOR_SWITCH, hover_color=COLOR_BUTTON_HOVER,
                                                     border_color=COLOR_BORDER, checkmark_color=("black", "white"))
        self.auto_proxies_checkbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(network_subframe, text="Your Proxies", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="nw", pady=4)
        self.your_proxies_dict_textbox = ctk.CTkTextbox(network_subframe, height=60, corner_radius=8,
                                                        fg_color=COLOR_TEXTBOX, border_color=COLOR_BORDER,
                                                        text_color=("black", "white"))
        self.your_proxies_dict_textbox.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(network_subframe, text="Min Timeout For Check", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.min_timeout_for_checking_availability_entry = SpinEntry(network_subframe, step=1, default=5, corner_radius=8,
                                                                     fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                                                     text_color=("black", "white"))
        self.min_timeout_for_checking_availability_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(network_subframe, text="Max Timeout For Check", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.max_timeout_for_checking_availability_entry = SpinEntry(network_subframe, step=1, default=15, corner_radius=8,
                                                                     fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                                                     text_color=("black", "white"))
        self.max_timeout_for_checking_availability_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(network_subframe, text="Retries", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.retries_entry = SpinEntry(network_subframe, step=1, default=3, corner_radius=8,
                                       fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                       text_color=("black", "white"))
        self.retries_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(network_subframe, text="GitHub Proxies", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.github_proxies_checkbox = ctk.CTkCheckBox(network_subframe, text="", corner_radius=6,
                                                       fg_color=COLOR_SWITCH, hover_color=COLOR_BUTTON_HOVER,
                                                       border_color=COLOR_BORDER, checkmark_color=("black", "white"))
        self.github_proxies_checkbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(network_subframe, text="URL List", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="nw", pady=4)
        self.url_lst_textbox = ctk.CTkTextbox(network_subframe, height=60, corner_radius=8,
                                              fg_color=COLOR_TEXTBOX, border_color=COLOR_BORDER,
                                              text_color=("black", "white"))
        self.url_lst_textbox.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(network_subframe, text="Proxy Retries", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.proxy_retries_entry = SpinEntry(network_subframe, step=1, default=3, corner_radius=8,
                                             fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                             text_color=("black", "white"))
        self.proxy_retries_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(network_subframe, text="Main Retries", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.main_retries_entry = SpinEntry(network_subframe, step=1, default=3, corner_radius=8,
                                            fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                            text_color=("black", "white"))
        self.main_retries_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        model_frame = ctk.CTkFrame(settings_frame, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME)
        model_frame.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        model_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(model_frame, text="Model", font=SECTION_FONT, text_color=("black", "white")).grid(row=0, column=0, pady=(8, 5), padx=10, sticky="w")
        model_subframe = ctk.CTkFrame(model_frame, fg_color="transparent", corner_radius=0)
        model_subframe.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        model_subframe.grid_columnconfigure(0, weight=0, minsize=140)
        model_subframe.grid_columnconfigure(1, weight=1)

        row = 0
        ctk.CTkLabel(model_subframe, text="Preferences In AI", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.preferences_in_ai_option_menu = ctk.CTkOptionMenu(model_subframe, values=PREFERENCES_IN_AI_LIST, corner_radius=8,
                                                               fg_color=COLOR_BUTTON, button_color=COLOR_BUTTON,
                                                               button_hover_color=COLOR_BUTTON_HOVER,
                                                               dropdown_fg_color=COLOR_FRAME_DARK,
                                                               dropdown_hover_color=COLOR_BUTTON_HOVER,
                                                               text_color=("black", "white"))
        self.preferences_in_ai_option_menu.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(model_subframe, text="Models Dir", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.models_dir_entry = ctk.CTkEntry(model_subframe, corner_radius=8, fg_color=COLOR_ENTRY,
                                             border_color=COLOR_BORDER, text_color=("black", "white"))
        self.models_dir_entry.insert(0, "./models")
        self.models_dir_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(model_subframe, text="With AI Orchestrator", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.with_ai_orchestrator_checkbox = ctk.CTkCheckBox(model_subframe, text="", corner_radius=6,
                                                             fg_color=COLOR_SWITCH, hover_color=COLOR_BUTTON_HOVER,
                                                             border_color=COLOR_BORDER, checkmark_color=("black", "white"))
        self.with_ai_orchestrator_checkbox.select()
        self.with_ai_orchestrator_checkbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(model_subframe, text="N CTX", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.n_ctx_entry = SpinEntry(model_subframe, step=1, default=0, corner_radius=8,
                                     fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                     text_color=("black", "white"))
        self.n_ctx_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(model_subframe, text="N GPU Layers", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.n_gpu_layers_entry = SpinEntry(model_subframe, step=1, default=0, corner_radius=8,
                                            fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                            text_color=("black", "white"))
        self.n_gpu_layers_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(model_subframe, text="Max Tokens", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.max_tokens_entry = SpinEntry(model_subframe, step=1, default=4096, corner_radius=8,
                                          fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                          text_color=("black", "white"))
        self.max_tokens_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(model_subframe, text="Token Hugging Face", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.your_token_for_hf_entry = ctk.CTkEntry(model_subframe, corner_radius=8, fg_color=COLOR_ENTRY,
                                                    border_color=COLOR_BORDER, text_color=("black", "white"))
        self.your_token_for_hf_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(model_subframe, text="Subdomain", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.subdomain_entry = ctk.CTkEntry(model_subframe, corner_radius=8, fg_color=COLOR_ENTRY,
                                            border_color=COLOR_BORDER, text_color=("black", "white"))
        self.subdomain_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(model_subframe, text="Repo ID", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.repo_id_entry = ctk.CTkEntry(model_subframe, corner_radius=8, fg_color=COLOR_ENTRY,
                                          border_color=COLOR_BORDER, text_color=("black", "white"))
        self.repo_id_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(model_subframe, text="Filename", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.filename_entry = ctk.CTkEntry(model_subframe, corner_radius=8, fg_color=COLOR_ENTRY,
                                           border_color=COLOR_BORDER, text_color=("black", "white"))
        self.filename_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(model_subframe, text="Prefer Mirror", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.prefer_mirror_checkbox = ctk.CTkCheckBox(model_subframe, text="", corner_radius=6,
                                                      fg_color=COLOR_SWITCH, hover_color=COLOR_BUTTON_HOVER,
                                                      border_color=COLOR_BORDER, checkmark_color=("black", "white"))
        self.prefer_mirror_checkbox.select()
        self.prefer_mirror_checkbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(model_subframe, text="Main Prompt Mode", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.main_prompt_mode_option_menu = ctk.CTkOptionMenu(model_subframe, values=list(ALL_MAIN_PROMPTS.keys()), corner_radius=8,
                                                              fg_color=COLOR_BUTTON, button_color=COLOR_BUTTON,
                                                              button_hover_color=COLOR_BUTTON_HOVER,
                                                              dropdown_fg_color=COLOR_FRAME_DARK,
                                                              dropdown_hover_color=COLOR_BUTTON_HOVER,
                                                              text_color=("black", "white"))
        self.main_prompt_mode_option_menu.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(model_subframe, text="Main Prompt", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="nw", pady=4)
        self.main_prompt_textbox = ctk.CTkTextbox(model_subframe, height=60, corner_radius=8,
                                                  fg_color=COLOR_TEXTBOX, border_color=COLOR_BORDER,
                                                  text_color=("black", "white"))
        self.main_prompt_textbox.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(model_subframe, text="Temperature", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.temperature_entry = SpinEntry(model_subframe, step=0.1, default=0.1, corner_radius=8,
                                           fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                           text_color=("black", "white"))
        self.temperature_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        translator_frame = ctk.CTkFrame(settings_frame, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME)
        translator_frame.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
        translator_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(translator_frame, text="Translator", font=SECTION_FONT, text_color=("black", "white")).grid(row=0, column=0, pady=(8, 5), padx=10, sticky="w")
        translator_subframe = ctk.CTkFrame(translator_frame, fg_color="transparent", corner_radius=0)
        translator_subframe.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        translator_subframe.grid_columnconfigure(0, weight=0, minsize=140)
        translator_subframe.grid_columnconfigure(1, weight=1)

        row = 0
        ctk.CTkLabel(translator_subframe, text="Determinant Mode", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.determinant_mode_option_menu = ctk.CTkOptionMenu(translator_subframe, values=DETERMINANT_MODE_LIST, corner_radius=8,
                                                              fg_color=COLOR_BUTTON, button_color=COLOR_BUTTON,
                                                              button_hover_color=COLOR_BUTTON_HOVER,
                                                              dropdown_fg_color=COLOR_FRAME_DARK,
                                                              dropdown_hover_color=COLOR_BUTTON_HOVER,
                                                              text_color=("black", "white"))
        self.determinant_mode_option_menu.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(translator_subframe, text="Accurate Translation", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.accurate_translation_checkbox = ctk.CTkCheckBox(translator_subframe, text="", corner_radius=6,
                                                             fg_color=COLOR_SWITCH, hover_color=COLOR_BUTTON_HOVER,
                                                             border_color=COLOR_BORDER, checkmark_color=("black", "white"))
        self.accurate_translation_checkbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(translator_subframe, text="API KEY DeepL", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.your_key_for_deepl_entry = ctk.CTkEntry(translator_subframe, corner_radius=8, fg_color=COLOR_ENTRY,
                                                     border_color=COLOR_BORDER, text_color=("black", "white"))
        self.your_key_for_deepl_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(translator_subframe, text="Request Language", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.request_language_entry = ctk.CTkEntry(translator_subframe, corner_radius=8, fg_color=COLOR_ENTRY,
                                                   border_color=COLOR_BORDER, text_color=("black", "white"))
        self.request_language_entry.insert(0, "en")
        self.request_language_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ocr_frame = ctk.CTkFrame(settings_frame, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME)
        ocr_frame.grid(row=6, column=0, sticky="ew", padx=5, pady=5)
        ocr_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(ocr_frame, text="OCR", font=SECTION_FONT, text_color=("black", "white")).grid(row=0, column=0, pady=(8, 5), padx=10, sticky="w")
        ocr_subframe = ctk.CTkFrame(ocr_frame, fg_color="transparent", corner_radius=0)
        ocr_subframe.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        ocr_subframe.grid_columnconfigure(0, weight=0, minsize=140)
        ocr_subframe.grid_columnconfigure(1, weight=1)

        row = 0
        ctk.CTkLabel(ocr_subframe, text="Languages List", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="nw", pady=4)
        self.lang_lst_textbox = ctk.CTkTextbox(ocr_subframe, height=60, corner_radius=8,
                                               fg_color=COLOR_TEXTBOX, border_color=COLOR_BORDER,
                                               text_color=("black", "white"))
        self.lang_lst_textbox.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(ocr_subframe, text="Use GPU", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.use_gpu_for_ocr_checkbox = ctk.CTkCheckBox(ocr_subframe, text="", corner_radius=6,
                                                        fg_color=COLOR_SWITCH, hover_color=COLOR_BUTTON_HOVER,
                                                        border_color=COLOR_BORDER, checkmark_color=("black", "white"))
        self.use_gpu_for_ocr_checkbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(ocr_subframe, text="With OCR", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.with_ocr_checkbox = ctk.CTkCheckBox(ocr_subframe, text="", corner_radius=6,
                                                 fg_color=COLOR_SWITCH, hover_color=COLOR_BUTTON_HOVER,
                                                 border_color=COLOR_BORDER, checkmark_color=("black", "white"))
        self.with_ocr_checkbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(ocr_subframe, text="Cloud Version", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.cloud_version_checkbox = ctk.CTkCheckBox(ocr_subframe, text="", corner_radius=6,
                                                      fg_color=COLOR_SWITCH, hover_color=COLOR_BUTTON_HOVER,
                                                      border_color=COLOR_BORDER, checkmark_color=("black", "white"))
        self.cloud_version_checkbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(ocr_subframe, text="With DeepSeek", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.with_deepseek_checkbox = ctk.CTkCheckBox(ocr_subframe, text="", corner_radius=6,
                                                      fg_color=COLOR_SWITCH, hover_color=COLOR_BUTTON_HOVER,
                                                      border_color=COLOR_BORDER, checkmark_color=("black", "white"))
        self.with_deepseek_checkbox.select()
        self.with_deepseek_checkbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(ocr_subframe, text="Model Size", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.model_size_option_menu = ctk.CTkOptionMenu(ocr_subframe, values=["tiny", "small", "base", "large", "gundam"], corner_radius=8,
                                                        fg_color=COLOR_BUTTON, button_color=COLOR_BUTTON,
                                                        button_hover_color=COLOR_BUTTON_HOVER,
                                                        dropdown_fg_color=COLOR_FRAME_DARK,
                                                        dropdown_hover_color=COLOR_BUTTON_HOVER,
                                                        text_color=("black", "white"))
        self.model_size_option_menu.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(ocr_subframe, text="Crop Mode", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.crop_mode_checkbox = ctk.CTkCheckBox(ocr_subframe, text="", corner_radius=6,
                                                  fg_color=COLOR_SWITCH, hover_color=COLOR_BUTTON_HOVER,
                                                  border_color=COLOR_BORDER, checkmark_color=("black", "white"))
        self.crop_mode_checkbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(ocr_subframe, text="Base URL", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.base_url_entry = ctk.CTkEntry(ocr_subframe, corner_radius=8, fg_color=COLOR_ENTRY,
                                           border_color=COLOR_BORDER, text_color=("black", "white"))
        self.base_url_entry.insert(0, "https://api.siliconflow.cn/v1/chat/completions")
        self.base_url_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(ocr_subframe, text="API Key DeepSeek OCR", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.api_key_for_deepseek_ocr_entry = ctk.CTkEntry(ocr_subframe, corner_radius=8, fg_color=COLOR_ENTRY,
                                                           border_color=COLOR_BORDER, text_color=("black", "white"))
        self.api_key_for_deepseek_ocr_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(ocr_subframe, text="Timeout DeepSeek OCR", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.timeout_for_deepseek_ocr_entry = SpinEntry(ocr_subframe, step=1, default=30, corner_radius=8,
                                                        fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                                        text_color=("black", "white"))
        self.timeout_for_deepseek_ocr_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(ocr_subframe, text="Max Rate Limit Retries", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.max_rate_limit_retries_entry = SpinEntry(ocr_subframe, step=1, default=3, corner_radius=8,
                                                      fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                                      text_color=("black", "white"))
        self.max_rate_limit_retries_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        other_frame = ctk.CTkFrame(settings_frame, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME)
        other_frame.grid(row=7, column=0, sticky="ew", padx=5, pady=5)
        other_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(other_frame, text="Other", font=SECTION_FONT, text_color=("black", "white")).grid(row=0, column=0, pady=(8, 5), padx=10, sticky="w")
        other_subframe = ctk.CTkFrame(other_frame, fg_color="transparent", corner_radius=0)
        other_subframe.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        other_subframe.grid_columnconfigure(0, weight=0, minsize=140)
        other_subframe.grid_columnconfigure(1, weight=1)

        row = 0
        ctk.CTkLabel(other_subframe, text="Filter For Swearing", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.filter_for_swearing_checkbox = ctk.CTkCheckBox(other_subframe, text="", corner_radius=6,
                                                            fg_color=COLOR_SWITCH, hover_color=COLOR_BUTTON_HOVER,
                                                            border_color=COLOR_BORDER, checkmark_color=("black", "white"))
        self.filter_for_swearing_checkbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(other_subframe, text="Verbose", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.verbose_checkbox = ctk.CTkCheckBox(other_subframe, text="", corner_radius=6,
                                                fg_color=COLOR_SWITCH, hover_color=COLOR_BUTTON_HOVER,
                                                border_color=COLOR_BORDER, checkmark_color=("black", "white"))
        self.verbose_checkbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(other_subframe, text="Echo", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.echo_checkbox = ctk.CTkCheckBox(other_subframe, text="", corner_radius=6,
                                             fg_color=COLOR_SWITCH, hover_color=COLOR_BUTTON_HOVER,
                                             border_color=COLOR_BORDER, checkmark_color=("black", "white"))
        self.echo_checkbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(other_subframe, text="Type Computer", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.type_computer_option_menu = ctk.CTkOptionMenu(other_subframe, values=["auto"] + TYPES_POWER, corner_radius=8,
                                                           fg_color=COLOR_BUTTON, button_color=COLOR_BUTTON,
                                                           button_hover_color=COLOR_BUTTON_HOVER,
                                                           dropdown_fg_color=COLOR_FRAME_DARK,
                                                           dropdown_hover_color=COLOR_BUTTON_HOVER,
                                                           text_color=("black", "white"))
        self.type_computer_option_menu.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(other_subframe, text="Proprietary Algorithms", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.proprietary_algorithms_checkbox = ctk.CTkCheckBox(other_subframe, text="", corner_radius=6,
                                                               fg_color=COLOR_SWITCH, hover_color=COLOR_BUTTON_HOVER,
                                                               border_color=COLOR_BORDER, checkmark_color=("black", "white"))
        self.proprietary_algorithms_checkbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        row += 1

        ctk.CTkLabel(other_subframe, text="Writing Response To File", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.writing_response_to_file_checkbox = ctk.CTkCheckBox(other_subframe, text="", corner_radius=6,
                                                                 fg_color=COLOR_SWITCH, hover_color=COLOR_BUTTON_HOVER,
                                                                 border_color=COLOR_BORDER, checkmark_color=("black", "white"))
        self.writing_response_to_file_checkbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        row += 1

    def change_theme(self, theme):
        ctk.set_appearance_mode(theme)
        self.update_tree_style()

    def create_chat_panel(self):
        chat_frame = ctk.CTkFrame(self.root, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME_DARK)
        chat_frame.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)
        chat_frame.grid_rowconfigure(1, weight=1)
        chat_frame.grid_rowconfigure(2, weight=0)
        chat_frame.grid_rowconfigure(3, weight=0)
        chat_frame.grid_rowconfigure(4, weight=0)
        chat_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(chat_frame, text="Chat With AI", font=TITLE_FONT, text_color=("black", "white")).grid(row=0, column=0, pady=(10, 5))

        self.resume_button = ctk.CTkButton(
            chat_frame, text="Resume pending request", corner_radius=8,
            fg_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER,
            text_color=("black", "white"), command=self.resume_request
        )
        self.resume_button.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 5))
        self.resume_button.grid_remove()

        self.messages_frame = ctk.CTkScrollableFrame(chat_frame, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME)
        self.messages_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.messages_frame.grid_columnconfigure(0, weight=1)

        attached_frame = ctk.CTkFrame(chat_frame, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME)
        attached_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        attached_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(attached_frame, text="Attached files", font=LABEL_FONT, text_color=("black", "white")).grid(row=0, column=0, sticky="w", padx=10, pady=(5,0))
        self.attached_textbox = ctk.CTkTextbox(attached_frame, height=80, corner_radius=8,
                                               fg_color=COLOR_TEXTBOX, border_color=COLOR_BORDER,
                                               text_color=("black", "white"))
        self.attached_textbox.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.attached_textbox.configure(state="disabled")

        request_frame = ctk.CTkFrame(chat_frame, fg_color="transparent")
        request_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=5)
        request_frame.grid_columnconfigure(0, weight=1)
        request_frame.grid_columnconfigure(1, weight=0)
        request_frame.grid_columnconfigure(2, weight=0)

        self.request_entry = ctk.CTkEntry(request_frame, corner_radius=8, placeholder_text="Type your message...",
                                          fg_color=COLOR_ENTRY, border_color=COLOR_BORDER, text_color=("black", "white"))
        self.request_entry.grid(row=0, column=0, sticky="ew", padx=(0,8))
        self.request_entry.bind("<Return>", lambda event: self.send_message())

        files_button = ctk.CTkButton(request_frame, text="Upload", corner_radius=8, width=90,
                                     fg_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER,
                                     text_color=("black", "white"), command=self.upload_files)
        files_button.grid(row=0, column=1, padx=4)

        send_button = ctk.CTkButton(request_frame, text="Send", corner_radius=8, width=90,
                                    fg_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER,
                                    text_color=("black", "white"), command=self.send_message)
        send_button.grid(row=0, column=2, padx=(4,0))

    def create_history_panel(self):
        history_frame = ctk.CTkFrame(self.root, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME_DARK)
        history_frame.grid(row=0, column=2, sticky="nsew", padx=8, pady=8)
        history_frame.grid_rowconfigure(0, weight=0)
        history_frame.grid_rowconfigure(1, weight=0)
        history_frame.grid_rowconfigure(2, weight=1)
        history_frame.grid_rowconfigure(3, weight=0)
        history_frame.grid_columnconfigure(0, weight=1)

        history_title_frame = ctk.CTkFrame(history_frame, fg_color="transparent")
        history_title_frame.grid(row=0, column=0, sticky="ew", pady=(10,5), padx=5)
        history_title_frame.grid_columnconfigure(0, weight=1)
        history_title_frame.grid_columnconfigure(1, weight=0)

        self.history_title = ctk.CTkLabel(history_title_frame, text="History", font=TITLE_FONT, text_color=("black", "white"))
        self.history_title.grid(row=0, column=0, sticky="w")

        self.mode_switch = ctk.CTkSwitch(history_title_frame, text="Virtual Storage", font=LABEL_FONT,
                                         command=self.switch_mode,
                                         fg_color=COLOR_SWITCH, progress_color=COLOR_SELECT,
                                         button_color=COLOR_BUTTON, button_hover_color=COLOR_BUTTON_HOVER,
                                         text_color=("black", "white"))
        self.mode_switch.grid(row=0, column=1, sticky="e", padx=10)

        self.history_subframe = ctk.CTkFrame(history_frame, fg_color="transparent")
        self.history_subframe.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.history_subframe.grid_columnconfigure(0, weight=1)

        self.history_controls = ctk.CTkFrame(self.history_subframe, fg_color="transparent")
        self.history_controls.grid(row=0, column=0, sticky="ew")
        self.history_controls.grid_columnconfigure(0, weight=1)
        self.history_controls.grid_columnconfigure(1, weight=0)
        self.history_controls.grid_columnconfigure(2, weight=0)
        self.history_controls.grid_columnconfigure(3, weight=0)

        self.find_story_entry = ctk.CTkEntry(self.history_controls, corner_radius=8, placeholder_text="Search...",
                                             fg_color=COLOR_ENTRY, border_color=COLOR_BORDER, text_color=("black", "white"))
        self.find_story_entry.grid(row=0, column=0, sticky="ew", padx=(0,5))
        self.find_story_entry.bind("<KeyRelease>", lambda e: self.filter_history())

        add_chats_button = ctk.CTkButton(self.history_controls, text="Add", width=60, height=30, corner_radius=8,
                                         fg_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER,
                                         text_color=("black", "white"), command=self.add_new_chat)
        add_chats_button.grid(row=0, column=1, padx=2, sticky="w")

        delete_chats_button = ctk.CTkButton(self.history_controls, text="Delete", width=60, height=30, corner_radius=8,
                                            fg_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER,
                                            text_color=("black", "white"), command=self.delete_current_chat)
        delete_chats_button.grid(row=0, column=2, padx=2, sticky="w")

        download_chats_button = ctk.CTkButton(self.history_controls, text="Download", width=60, height=30, corner_radius=8,
                                              fg_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER,
                                              text_color=("black", "white"), command=self.download_chat)
        download_chats_button.grid(row=0, column=3, padx=2, sticky="w")

        self.storage_controls = ctk.CTkFrame(self.history_subframe, fg_color="transparent")
        self.storage_controls.grid(row=0, column=0, sticky="ew")
        self.storage_controls.grid_columnconfigure(0, weight=1)
        self.storage_controls.grid_columnconfigure(1, weight=0)
        self.storage_controls.grid_columnconfigure(2, weight=0)
        self.storage_controls.grid_remove()

        self.storage_path_entry = ctk.CTkEntry(self.storage_controls, corner_radius=8, placeholder_text="Storage path...",
                                               fg_color=COLOR_ENTRY, border_color=COLOR_BORDER, text_color=("black", "white"))
        self.storage_path_entry.grid(row=0, column=0, sticky="ew", padx=(0,5))
        if self.storage_path:
            self.storage_path_entry.insert(0, self.storage_path)

        browse_storage_button = ctk.CTkButton(self.storage_controls, text="Browse", width=70, height=30, corner_radius=8,
                                              fg_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER,
                                              text_color=("black", "white"), command=self.browse_storage)
        browse_storage_button.grid(row=0, column=1, padx=2, sticky="w")

        refresh_storage_button = ctk.CTkButton(self.storage_controls, text="Refresh", width=70, height=30, corner_radius=8,
                                               fg_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER,
                                               text_color=("black", "white"), command=self.refresh_storage)
        refresh_storage_button.grid(row=0, column=2, padx=2, sticky="w")

        self.history_field_frame = ctk.CTkScrollableFrame(history_frame, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME)
        self.history_field_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.history_field_frame.grid_rowconfigure(0, weight=1)
        self.history_field_frame.grid_columnconfigure(0, weight=1)

        logs_frame = ctk.CTkFrame(history_frame, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME)
        logs_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        logs_frame.grid_columnconfigure(0, weight=1)

        logs_header = ctk.CTkFrame(logs_frame, fg_color="transparent")
        logs_header.grid(row=0, column=0, sticky="ew", padx=5, pady=2)
        logs_header.grid_columnconfigure(0, weight=1)
        logs_header.grid_columnconfigure(1, weight=0)
        logs_header.grid_columnconfigure(2, weight=0)

        ctk.CTkLabel(logs_header, text="Logs", font=LABEL_FONT, text_color=("black", "white")).grid(row=0, column=0, sticky="w")
        download_logs_button = ctk.CTkButton(logs_header, text="Download", width=60, height=25, corner_radius=8,
                                             command=self.download_logs,
                                             fg_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER,
                                             text_color=("black", "white"))
        download_logs_button.grid(row=0, column=1, padx=2, sticky="e")
        clear_logs_button = ctk.CTkButton(logs_header, text="Clear", width=60, height=25, corner_radius=8,
                                          command=self.clear_logs,
                                          fg_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER,
                                          text_color=("black", "white"))
        clear_logs_button.grid(row=0, column=2, padx=(2,0), sticky="e")

        self.logs_textbox = ctk.CTkTextbox(logs_frame, height=150, corner_radius=8,
                                           fg_color=COLOR_TEXTBOX, border_color=COLOR_BORDER,
                                           text_color=("black", "white"))
        self.logs_textbox.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        self.current_chat_id = None
        self.chats = {}
        self.update_history_list()

        self.tree = None

    def export_all_chats(self):
        if not self.chats:
            messagebox.showinfo("Info", "No chats to export.")
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
        messagebox.showinfo("Export", f"Exported {count} chat(s) to {folder}")

    def delete_all_chats(self):
        if not self.chats:
            return
        if not messagebox.askyesno("Delete All", "Are you sure you want to delete ALL chats?"):
            return
        self.chats.clear()
        self.add_new_chat()
        self.save_chats_to_file()
        self.update_history_list()
        self.resume_button.grid_remove()

    def clear_current_chat(self):
        if self.current_chat_id is None or self.current_chat_id not in self.chats:
            messagebox.showwarning("Warning", "No chat selected.")
            return
        if not messagebox.askyesno("Clear Chat", "Are you sure you want to clear all messages in this chat?"):
            return
        self.chats[self.current_chat_id]["messages"] = []
        self.save_chats_to_file()
        self.load_chat(self.current_chat_id)
        self.resume_button.grid_remove()

    def switch_mode(self):
        if self.mode_switch.get() == 1:
            self.history_controls.grid_remove()
            self.storage_controls.grid()
            self.history_title.configure(text="Virtual Storage")
            self.build_tree()
            self.update_attached_text()
        else:
            self.storage_controls.grid_remove()
            self.history_controls.grid()
            self.history_title.configure(text="History")
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
        for widget in self.history_field_frame.winfo_children():
            widget.destroy()
        if not self.storage_path or not os.path.isdir(self.storage_path):
            label = ctk.CTkLabel(self.history_field_frame, text="No storage path selected", font=LABEL_FONT,
                                 text_color=("black", "white"))
            label.pack(pady=10)
            return

        self.tree = ttk.Treeview(self.history_field_frame, selectmode="browse")
        self.tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.history_field_frame.grid_rowconfigure(0, weight=1)
        self.history_field_frame.grid_columnconfigure(0, weight=1)

        self.virtual_tree_data = {}
        root_node = self.tree.insert("", "end", text=os.path.basename(self.storage_path), open=True)
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

    def scan_storage(self):
        if self.mode_switch.get() == 1:
            self.build_tree()

    def browse_storage(self):
        path = filedialog.askdirectory(title="Select Virtual Storage Folder")
        if path:
            self.storage_path = path
            self.storage_path_entry.delete(0, "end")
            self.storage_path_entry.insert(0, path)
            self.save_storage_path()
            self.scan_storage()

    def refresh_storage(self):
        self.storage_path = self.storage_path_entry.get().strip()
        self.save_storage_path()
        self.scan_storage()

    def update_attached_text(self):
        self.attached_textbox.configure(state="normal")
        self.attached_textbox.delete("1.0", "end")
        if self.mode_switch.get() == 1:
            self.attached_textbox.insert("1.0", "All files in virtual storage")
        else:
            if self.attached_files:
                self.attached_textbox.insert("1.0", "\n".join(self.attached_files))
            else:
                self.attached_textbox.insert("1.0", "")
        self.attached_textbox.configure(state="disabled")

    def upload_files(self):
        if self.mode_switch.get() == 1:
            messagebox.showinfo("Info", "Virtual storage is active. Use the virtual storage path.")
            return
        files = filedialog.askopenfilenames()
        if files:
            self.attached_files = list(files)
            self.update_attached_text()

    def collect_parameters(self):
        def parse_textbox_list(widget):
            text = widget.get("1.0", "end-1c").strip()
            if not text:
                return []
            return [line.strip() for line in text.splitlines() if line.strip()]

        virtual_storage = bool(self.mode_switch.get())
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
            "preferences_in_ai": self.preferences_in_ai_option_menu.get(),
            "filter_for_swearing": bool(self.filter_for_swearing_checkbox.get()),
            "additional_files": additional if additional else None,
            "models_dir": self.models_dir_entry.get().strip() or "./models",
            "with_ai_orchestrator": bool(self.with_ai_orchestrator_checkbox.get()),
            "verbose": bool(self.verbose_checkbox.get()),
            "n_ctx": self.n_ctx_entry.get_int(default=0) or None,
            "n_gpu_layers": self.n_gpu_layers_entry.get_int(default=0),
            "echo": bool(self.echo_checkbox.get()),
            "max_tokens": self.max_tokens_entry.get_int(default=4096),
            "your_token_for_hf": self.your_token_for_hf_entry.get().strip() or None,
            "subdomain": self.subdomain_entry.get().strip() or "",
            "country": self.country_entry.get().strip() or None,
            "protocol": self.protocol_option_menu.get(),
            "max_timeout": self.max_timeout_entry.get_int(default=30),
            "is_working": bool(self.is_working_checkbox.get()),
            "type_computer": self.type_computer_option_menu.get() if self.type_computer_option_menu.get() != "auto" else None,
            "auto_proxies": bool(self.auto_proxies_checkbox.get()),
            "writing_response_to_file": bool(self.writing_response_to_file_checkbox.get()),
            "your_proxies_dict": parse_textbox_list(self.your_proxies_dict_textbox) or None,
            "determinant_mode": self.determinant_mode_option_menu.get(),
            "accurate_translation": bool(self.accurate_translation_checkbox.get()),
            "your_key_for_deepl": self.your_key_for_deepl_entry.get().strip() or "",
            "proprietary_algorithms": bool(self.proprietary_algorithms_checkbox.get()),
            "repo_id": self.repo_id_entry.get().strip() or None,
            "filename": self.filename_entry.get().strip() or None,
            "min_timeout_for_checking_availability": self.min_timeout_for_checking_availability_entry.get_int(default=5),
            "max_timeout_for_checking_availability": self.max_timeout_for_checking_availability_entry.get_int(default=15),
            "request_language": self.request_language_entry.get().strip() or "en",
            "main_prompt_mode": self.main_prompt_mode_option_menu.get(),
            "main_prompt": self.main_prompt_textbox.get("1.0", "end-1c").strip() or None,
            "temperature": self.temperature_entry.get_float(default=0.1),
            "retries": self.retries_entry.get_int(default=3),
            "github_proxies": bool(self.github_proxies_checkbox.get()),
            "url_lst": parse_textbox_list(self.url_lst_textbox) or None,
            "proxy_retries": self.proxy_retries_entry.get_int(default=3),
            "main_retries": self.main_retries_entry.get_int(default=3),
            "lang_lst": parse_textbox_list(self.lang_lst_textbox) or None,
            "use_gpu_for_ocr": bool(self.use_gpu_for_ocr_checkbox.get()),
            "virtual_storage": virtual_storage,
            "virtual_storage_path": virtual_storage_path,
            "with_ocr": bool(self.with_ocr_checkbox.get()),
            "cloud_version": bool(self.cloud_version_checkbox.get()),
            "with_deepseek": bool(self.with_deepseek_checkbox.get()),
            "model_size": self.model_size_option_menu.get(),
            "crop_mode": bool(self.crop_mode_checkbox.get()),
            "base_url": self.base_url_entry.get().strip(),
            "api_key_for_deepseek_ocr": self.api_key_for_deepseek_ocr_entry.get().strip() or None,
            "timeout_for_deepseek_ocr": self.timeout_for_deepseek_ocr_entry.get_int(default=30) or None,
            "max_rate_limit_retries": self.max_rate_limit_retries_entry.get_int(default=3),
            "prefer_mirror": bool(self.prefer_mirror_checkbox.get())
        }
        return params

    def update_history_list(self):
        for widget in self.history_field_frame.winfo_children():
            widget.destroy()
        for chat_id, chat_data in self.chats.items():
            messages = chat_data.get("messages", [])
            first_user_msg = None
            for m in messages:
                if m.get("role") == "user":
                    first_user_msg = m["content"]
                    break
            if first_user_msg:
                title = first_user_msg[:30] + ("..." if len(first_user_msg) > 30 else "")
            else:
                title = "Empty chat"
            created_at = chat_data.get("created_at", "Unknown date")
            btn_text = f"{created_at} - {title}"
            btn = ctk.CTkButton(self.history_field_frame, text=btn_text,
                                anchor="w", corner_radius=6, height=30,
                                fg_color="transparent", hover_color=COLOR_BUTTON_HOVER,
                                text_color=("black", "white"),
                                command=lambda cid=chat_id: self.load_chat(cid))
            btn.pack(fill="x", padx=5, pady=2)

    def filter_history(self):
        query = self.find_story_entry.get().lower()
        for widget in self.history_field_frame.winfo_children():
            widget.destroy()
        for chat_id, chat_data in self.chats.items():
            messages = chat_data.get("messages", [])
            first_user_msg = None
            for m in messages:
                if m.get("role") == "user":
                    first_user_msg = m["content"]
                    break
            if first_user_msg:
                title = first_user_msg[:30] + ("..." if len(first_user_msg) > 30 else "")
            else:
                title = "Empty chat"
            created_at = chat_data.get("created_at", "Unknown date")
            if query in f"{created_at} {title}".lower():
                btn = ctk.CTkButton(self.history_field_frame, text=f"{created_at} - {title}",
                                    anchor="w", corner_radius=6, height=30,
                                    fg_color="transparent", hover_color=COLOR_BUTTON_HOVER,
                                    text_color=("black", "white"),
                                    command=lambda cid=chat_id: self.load_chat(cid))
                btn.pack(fill="x", padx=5, pady=2)

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
        self.check_pending_message()

    def display_message(self, role, content, timestamp=None):
        if role not in ("user", "assistant"):
            return
        if timestamp is None:
            timestamp = datetime.now().strftime("%H:%M")
        self.hide_welcome_placeholder()

        bg = ("#e0e0e0", "#2d2d2d") if role == "user" else ("#d0d0d0", "#3a3a3a")
        bubble = ctk.CTkFrame(self.messages_frame, corner_radius=10, fg_color=bg)
        bubble.pack(fill="x", padx=10, pady=5, anchor="e" if role == "user" else "w")

        label = ctk.CTkLabel(bubble, text=content, wraplength=600, justify="left",
                             text_color=("black", "white"))
        label.pack(padx=10, pady=(10, 5), anchor="w")

        bottom_frame = ctk.CTkFrame(bubble, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=10, pady=(0, 5))

        time_label = ctk.CTkLabel(bottom_frame, text=timestamp, font=("Segoe UI", 9),
                                  text_color=("gray40", "gray60"))
        time_label.pack(side="left")

        copy_btn = ctk.CTkButton(bottom_frame, text="Copy", width=50, height=20,
                                 corner_radius=4, fg_color=COLOR_BUTTON,
                                 hover_color=COLOR_BUTTON_HOVER,
                                 text_color=("black", "white"),
                                 command=lambda: self.copy_to_clipboard(content))
        copy_btn.pack(side="right", padx=(5,0))

    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()

    def send_message(self):
        if self.is_busy:
            messagebox.showinfo("Info", "AI is busy. Please wait.")
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
            self.chats[self.current_chat_id]["messages"].append({"role": "user", "content": user_text, "timestamp": now})
            self.save_chats_to_file()
            self.update_history_list()

        self.resume_button.grid_remove()
        self.is_busy = True
        thread = threading.Thread(target=self.process_request, args=(user_text,))
        thread.daemon = True
        thread.start()

    def process_request(self, user_text):
        try:
            params = self.collect_parameters()
            params["request"] = user_text
            alex = AlexRadar(**params)
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
                            self.chats[self.current_chat_id]["messages"].append({"role": "assistant", "content": data, "timestamp": now})
                            self.save_chats_to_file()
                            self.update_history_list()
                            self.resume_button.grid_remove()
                elif msg_type == "error":
                    messagebox.showerror("Error", data)
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
            self.resume_button.configure(text="Resume pending request")
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
        self.process_request(last_user_msg)

    def download_logs(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt")])
        if file_path:
            content = self.logs_textbox.get("1.0", "end-1c")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

    def clear_logs(self):
        self.logs_textbox.delete("1.0", "end")

    def download_chat(self):
        if self.current_chat_id is None:
            messagebox.showwarning("Warning", "No chat selected.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                for msg in self.chats[self.current_chat_id]["messages"]:
                    f.write(f"{msg['role'].capitalize()}: {msg['content']}\n")
            messagebox.showinfo("Success", "Chat saved.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = AlexRadarGUI(root)
    root.mainloop()