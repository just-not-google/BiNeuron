from tkinter import filedialog, messagebox
import threading
import queue
import logging
import traceback
import json
import os
from datetime import datetime
import customtkinter as ctk
from CTkSpinbox import CTkSpinbox

from AlexRadar import AlexRadar
from AlexRadar.data.constants_for_functions import (
    HTTP_PROTOCOL, HTTPS_PROTOCOL, TYPES_POWER,
    PREFERENCES_IN_AI_LIST, DETERMINANT_MODE_LIST
)
from AlexRadar.data.variants_industrial_scenarios import ALL_MAIN_PROMPTS
from AlexRadar.data.natural_languages import NATURAL_LANGUAGES

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

COLOR_BG = ("#f0f0f0", "#1a1a1a")
COLOR_FRAME = ("#e8e8e8", "#252525")
COLOR_FRAME_DARK = ("#dcdcdc", "#2e2e2e")
COLOR_ENTRY = ("#ffffff", "#2d2d2d")
COLOR_TEXTBOX = ("#fafafa", "#1f1f1f")
COLOR_BUTTON = ("#c0c0c0", "#3a3a3a")
COLOR_BUTTON_HOVER = ("#a8a8a8", "#505050")
COLOR_BORDER = ("#aaaaaa", "#444444")
COLOR_SELECT = ("#888888", "#666666")
COLOR_SWITCH = ("#999999", "#555555")

FRAME_CORNER = 10
LABEL_FONT = ("Segoe UI", 13)
TITLE_FONT = ("Segoe UI", 18, "bold")
SECTION_FONT = ("Segoe UI", 15, "bold")
SPINBOX_WIDTH = 80

class AlexRadarGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AlexRadar")
        self.root.geometry("1500x900")
        self.alex_instance = None
        self.is_busy = False
        self.message_queue = queue.Queue()
        self.attached_files = []
        self.chats_file = "chats.json"
        root.grid_columnconfigure(0, weight=1, uniform="main")
        root.grid_columnconfigure(1, weight=3, uniform="main")
        root.grid_columnconfigure(2, weight=1, uniform="main")
        root.grid_rowconfigure(0, weight=1)
        self.create_settings_panel()
        self.create_chat_panel()
        self.create_history_panel()
        self.setup_logging()
        self.load_chats_from_file()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.poll_queue()

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

    def save_chats_to_file(self):
        try:
            with open(self.chats_file, "w", encoding="utf-8") as f:
                json.dump(self.chats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"Failed to save chats: {e}")

    def on_closing(self):
        self.save_chats_to_file()
        self.root.destroy()

    def create_settings_panel(self):
        settings_frame = ctk.CTkScrollableFrame(root, width=420, corner_radius=FRAME_CORNER, fg_color="transparent")
        settings_frame.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        settings_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(settings_frame, text="Settings", font=TITLE_FONT, text_color=("black", "white")).grid(row=0, column=0, pady=(10, 15))
        interface_frame = ctk.CTkFrame(settings_frame, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME)
        interface_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        interface_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(interface_frame, text="Interface", font=SECTION_FONT, text_color=("black", "white")).grid(row=0, column=0, pady=(8, 5), padx=10, sticky="w")
        interface_subframe = ctk.CTkFrame(interface_frame, fg_color="transparent", corner_radius=0)
        interface_subframe.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        interface_subframe.grid_columnconfigure(0, weight=0, minsize=140)
        interface_subframe.grid_columnconfigure(1, weight=1)
        row = 0
        ctk.CTkLabel(interface_subframe, text="Theme", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.theme_option_menu = ctk.CTkOptionMenu(interface_subframe, values=["dark", "light", "system"],
                                                   command=lambda choice: ctk.set_appearance_mode(choice),
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
        network_frame = ctk.CTkFrame(settings_frame, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME)
        network_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
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
        self.max_timeout_spinbox = CTkSpinbox(network_subframe, min_value=0, max_value=2000, width=SPINBOX_WIDTH, corner_radius=8,
                                              fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                              button_color=COLOR_BUTTON, button_hover_color=COLOR_BUTTON_HOVER,
                                              text_color=("black", "white"))
        self.max_timeout_spinbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
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
        self.min_timeout_for_checking_availability_spinbox = CTkSpinbox(network_subframe, min_value=0, max_value=60, width=SPINBOX_WIDTH, corner_radius=8,
                                                                        fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                                                        button_color=COLOR_BUTTON, button_hover_color=COLOR_BUTTON_HOVER,
                                                                        text_color=("black", "white"))
        self.min_timeout_for_checking_availability_spinbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        row += 1
        ctk.CTkLabel(network_subframe, text="Max Timeout For Check", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.max_timeout_for_checking_availability_spinbox = CTkSpinbox(network_subframe, min_value=0, max_value=60, width=SPINBOX_WIDTH, corner_radius=8,
                                                                        fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                                                        button_color=COLOR_BUTTON, button_hover_color=COLOR_BUTTON_HOVER,
                                                                        text_color=("black", "white"))
        self.max_timeout_for_checking_availability_spinbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        row += 1
        ctk.CTkLabel(network_subframe, text="Retries", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.retries_spinbox = CTkSpinbox(network_subframe, min_value=0, max_value=10, width=SPINBOX_WIDTH, corner_radius=8,
                                          fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                          button_color=COLOR_BUTTON, button_hover_color=COLOR_BUTTON_HOVER,
                                          text_color=("black", "white"))
        self.retries_spinbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
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
        self.proxy_retries_spinbox = CTkSpinbox(network_subframe, min_value=0, max_value=10, width=SPINBOX_WIDTH, corner_radius=8,
                                                fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                                button_color=COLOR_BUTTON, button_hover_color=COLOR_BUTTON_HOVER,
                                                text_color=("black", "white"))
        self.proxy_retries_spinbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        row += 1
        ctk.CTkLabel(network_subframe, text="Main Retries", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.main_retries_spinbox = CTkSpinbox(network_subframe, min_value=0, max_value=10, width=SPINBOX_WIDTH, corner_radius=8,
                                               fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                               button_color=COLOR_BUTTON, button_hover_color=COLOR_BUTTON_HOVER,
                                               text_color=("black", "white"))
        self.main_retries_spinbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        model_frame = ctk.CTkFrame(settings_frame, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME)
        model_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
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
        self.n_ctx_spinbox = CTkSpinbox(model_subframe, min_value=0, max_value=8192, width=SPINBOX_WIDTH, corner_radius=8,
                                        fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                        button_color=COLOR_BUTTON, button_hover_color=COLOR_BUTTON_HOVER,
                                        text_color=("black", "white"))
        self.n_ctx_spinbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        row += 1
        ctk.CTkLabel(model_subframe, text="N GPU Layers", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.n_gpu_layers_spinbox = CTkSpinbox(model_subframe, min_value=0, max_value=100, width=SPINBOX_WIDTH, corner_radius=8,
                                               fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                               button_color=COLOR_BUTTON, button_hover_color=COLOR_BUTTON_HOVER,
                                               text_color=("black", "white"))
        self.n_gpu_layers_spinbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        row += 1
        ctk.CTkLabel(model_subframe, text="Max Tokens", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.max_tokens_spinbox = CTkSpinbox(model_subframe, min_value=0, max_value=8192, width=SPINBOX_WIDTH, corner_radius=8,
                                             fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                             button_color=COLOR_BUTTON, button_hover_color=COLOR_BUTTON_HOVER,
                                             text_color=("black", "white"))
        self.max_tokens_spinbox.set(4096)
        self.max_tokens_spinbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
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
        self.temperature_entry = ctk.CTkEntry(model_subframe, corner_radius=8, fg_color=COLOR_ENTRY,
                                              border_color=COLOR_BORDER, text_color=("black", "white"))
        self.temperature_entry.insert(0, "0.1")
        self.temperature_entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(8,0))
        translator_frame = ctk.CTkFrame(settings_frame, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME)
        translator_frame.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
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
        ocr_frame = ctk.CTkFrame(settings_frame, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME)
        ocr_frame.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
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
        self.timeout_for_deepseek_ocr_spinbox = CTkSpinbox(ocr_subframe, min_value=0, max_value=300, width=SPINBOX_WIDTH, corner_radius=8,
                                                           fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                                           button_color=COLOR_BUTTON, button_hover_color=COLOR_BUTTON_HOVER,
                                                           text_color=("black", "white"))
        self.timeout_for_deepseek_ocr_spinbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        row += 1
        ctk.CTkLabel(ocr_subframe, text="Max Rate Limit Retries", font=LABEL_FONT, text_color=("black", "white")).grid(row=row, column=0, sticky="w", pady=4)
        self.max_rate_limit_retries_spinbox = CTkSpinbox(ocr_subframe, min_value=0, max_value=10, width=SPINBOX_WIDTH, corner_radius=8,
                                                         fg_color=COLOR_ENTRY, border_color=COLOR_BORDER,
                                                         button_color=COLOR_BUTTON, button_hover_color=COLOR_BUTTON_HOVER,
                                                         text_color=("black", "white"))
        self.max_rate_limit_retries_spinbox.grid(row=row, column=1, sticky="w", pady=4, padx=(8,0))
        other_frame = ctk.CTkFrame(settings_frame, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME)
        other_frame.grid(row=6, column=0, sticky="ew", padx=5, pady=5)
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

    def create_chat_panel(self):
        chat_frame = ctk.CTkFrame(root, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME_DARK)
        chat_frame.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)
        chat_frame.grid_rowconfigure(1, weight=1)
        chat_frame.grid_rowconfigure(2, weight=0)
        chat_frame.grid_rowconfigure(3, weight=0)
        chat_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(chat_frame, text="Chat With AI", font=TITLE_FONT, text_color=("black", "white")).grid(row=0, column=0, pady=(10, 5))
        self.messages_frame = ctk.CTkScrollableFrame(chat_frame, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME)
        self.messages_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.messages_frame.grid_columnconfigure(0, weight=1)
        attached_frame = ctk.CTkFrame(chat_frame, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME)
        attached_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        attached_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(attached_frame, text="Attached files", font=LABEL_FONT, text_color=("black", "white")).grid(row=0, column=0, sticky="w", padx=10, pady=(5,0))
        self.attached_textbox = ctk.CTkTextbox(attached_frame, height=80, corner_radius=8,
                                               fg_color=COLOR_TEXTBOX, border_color=COLOR_BORDER,
                                               text_color=("black", "white"))
        self.attached_textbox.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.attached_textbox.configure(state="disabled")
        request_frame = ctk.CTkFrame(chat_frame, fg_color="transparent")
        request_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
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
        history_frame = ctk.CTkFrame(root, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME_DARK)
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
        download_chats_button.grid(row=0, column=3, padx=(2,0), sticky="w")
        self.storage_controls = ctk.CTkFrame(self.history_subframe, fg_color="transparent")
        self.storage_controls.grid(row=0, column=0, sticky="ew")
        self.storage_controls.grid_columnconfigure(0, weight=1)
        self.storage_controls.grid_columnconfigure(1, weight=0)
        self.storage_controls.grid_columnconfigure(2, weight=0)
        self.storage_controls.grid_columnconfigure(3, weight=0)
        self.storage_controls.grid_remove()
        self.storage_path_entry = ctk.CTkEntry(self.storage_controls, corner_radius=8, placeholder_text="Storage path...",
                                               fg_color=COLOR_ENTRY, border_color=COLOR_BORDER, text_color=("black", "white"))
        self.storage_path_entry.grid(row=0, column=0, sticky="ew", padx=(0,5))
        add_storage_button = ctk.CTkButton(self.storage_controls, text="Add", width=60, height=30, corner_radius=8,
                                           fg_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER,
                                           text_color=("black", "white"), command=self.add_storage_path)
        add_storage_button.grid(row=0, column=1, padx=2, sticky="w")
        delete_storage_button = ctk.CTkButton(self.storage_controls, text="Delete", width=60, height=30, corner_radius=8,
                                              fg_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER,
                                              text_color=("black", "white"), command=self.delete_storage_path)
        delete_storage_button.grid(row=0, column=2, padx=2, sticky="w")
        replace_storage_button = ctk.CTkButton(self.storage_controls, text="Replace", width=60, height=30, corner_radius=8,
                                               fg_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER,
                                               text_color=("black", "white"), command=self.replace_storage_path)
        replace_storage_button.grid(row=0, column=3, padx=(2,0), sticky="w")
        self.history_field_frame = ctk.CTkScrollableFrame(history_frame, corner_radius=FRAME_CORNER, fg_color=COLOR_FRAME)
        self.history_field_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
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

    def switch_mode(self):
        if self.mode_switch.get() == 1:
            self.history_controls.grid_remove()
            self.storage_controls.grid()
            self.history_title.configure(text="Virtual Storage")
            for widget in self.history_field_frame.winfo_children():
                widget.destroy()
        else:
            self.storage_controls.grid_remove()
            self.history_controls.grid()
            self.history_title.configure(text="History")
            self.update_history_list()

    def update_history_list(self):
        for widget in self.history_field_frame.winfo_children():
            widget.destroy()
        for chat_id, chat_data in self.chats.items():
            messages = chat_data.get("messages", [])
            first_msg = messages[0]["content"][:30] if messages else "Empty chat"
            created_at = chat_data.get("created_at", "Unknown date")
            btn_text = f"{created_at} - {first_msg}"
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
            first_msg = messages[0]["content"][:30] if messages else "Empty chat"
            created_at = chat_data.get("created_at", "Unknown date")
            if query in f"{created_at} {first_msg}".lower():
                btn = ctk.CTkButton(self.history_field_frame, text=f"{created_at} - {first_msg}",
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

    def delete_current_chat(self):
        if self.current_chat_id is not None and self.current_chat_id in self.chats:
            del self.chats[self.current_chat_id]
            self.current_chat_id = None
            self.clear_messages()
            self.save_chats_to_file()
            self.update_history_list()

    def load_chat(self, chat_id):
        self.current_chat_id = chat_id
        self.clear_messages()
        for msg in self.chats[chat_id]["messages"]:
            self.display_message(msg["role"], msg["content"])

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

    def clear_messages(self):
        for widget in self.messages_frame.winfo_children():
            widget.destroy()

    def display_message(self, role, content):
        bubble = ctk.CTkFrame(self.messages_frame, corner_radius=10,
                              fg_color=("#ffffff", "#3a3a3a") if role == "user" else ("#e0e0e0", "#2a2a2a"))
        bubble.pack(fill="x", padx=10, pady=5, anchor="e" if role == "user" else "w")
        label = ctk.CTkLabel(bubble, text=content, wraplength=600, justify="left",
                             text_color=("black", "white"))
        label.pack(padx=10, pady=5)

    def add_storage_path(self):
        path = self.storage_path_entry.get()
        if path:
            print(f"Add storage path: {path}")

    def delete_storage_path(self):
        print("Delete storage path")

    def replace_storage_path(self):
        print("Replace storage path")

    def download_logs(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt")])
        if file_path:
            content = self.logs_textbox.get("1.0", "end-1c")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

    def clear_logs(self):
        self.logs_textbox.delete("1.0", "end")

    def upload_files(self):
        files = filedialog.askopenfilenames()
        if files:
            self.attached_files = list(files)
            self.attached_textbox.configure(state="normal")
            self.attached_textbox.delete("1.0", "end")
            self.attached_textbox.insert("1.0", "\n".join(self.attached_files))
            self.attached_textbox.configure(state="disabled")

    def collect_parameters(self):
        def parse_textbox_list(widget):
            text = widget.get("1.0", "end-1c").strip()
            if not text:
                return []
            return [line.strip() for line in text.splitlines() if line.strip()]

        params = {
            "request": self.request_entry.get().strip(),
            "preferences_in_ai": self.preferences_in_ai_option_menu.get(),
            "filter_for_swearing": bool(self.filter_for_swearing_checkbox.get()),
            "additional_files": self.attached_files if self.attached_files else None,
            "models_dir": self.models_dir_entry.get().strip() or "./models",
            "with_ai_orchestrator": bool(self.with_ai_orchestrator_checkbox.get()),
            "verbose": bool(self.verbose_checkbox.get()),
            "n_ctx": int(self.n_ctx_spinbox.get()) if self.n_ctx_spinbox.get() else None,
            "n_gpu_layers": int(self.n_gpu_layers_spinbox.get()),
            "echo": bool(self.echo_checkbox.get()),
            "max_tokens": int(self.max_tokens_spinbox.get()),
            "your_token_for_hf": self.your_token_for_hf_entry.get().strip() or None,
            "subdomain": self.subdomain_entry.get().strip() or "",
            "country": self.country_entry.get().strip() or None,
            "protocol": self.protocol_option_menu.get(),
            "max_timeout": int(self.max_timeout_spinbox.get()),
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
            "min_timeout_for_checking_availability": int(self.min_timeout_for_checking_availability_spinbox.get()),
            "max_timeout_for_checking_availability": int(self.max_timeout_for_checking_availability_spinbox.get()),
            "request_language": self.request_language_entry.get().strip() or "en",
            "main_prompt_mode": self.main_prompt_mode_option_menu.get(),
            "main_prompt": self.main_prompt_textbox.get("1.0", "end-1c").strip() or None,
            "temperature": float(self.temperature_entry.get()) if self.temperature_entry.get() else 0.1,
            "retries": int(self.retries_spinbox.get()),
            "github_proxies": bool(self.github_proxies_checkbox.get()),
            "url_lst": parse_textbox_list(self.url_lst_textbox) or None,
            "proxy_retries": int(self.proxy_retries_spinbox.get()),
            "main_retries": int(self.main_retries_spinbox.get()),
            "lang_lst": parse_textbox_list(self.lang_lst_textbox) or None,
            "use_gpu_for_ocr": bool(self.use_gpu_for_ocr_checkbox.get()),
            "virtual_storage": bool(self.mode_switch.get()),
            "virtual_storage_path": self.storage_path_entry.get().strip() if self.mode_switch.get() else None,
            "with_ocr": bool(self.with_ocr_checkbox.get()),
            "cloud_version": bool(self.cloud_version_checkbox.get()),
            "with_deepseek": bool(self.with_deepseek_checkbox.get()),
            "model_size": self.model_size_option_menu.get(),
            "crop_mode": bool(self.crop_mode_checkbox.get()),
            "base_url": self.base_url_entry.get().strip(),
            "api_key_for_deepseek_ocr": self.api_key_for_deepseek_ocr_entry.get().strip() or None,
            "timeout_for_deepseek_ocr": int(self.timeout_for_deepseek_ocr_spinbox.get()) if self.timeout_for_deepseek_ocr_spinbox.get() else None,
            "max_rate_limit_retries": int(self.max_rate_limit_retries_spinbox.get()),
            "prefer_mirror": bool(self.prefer_mirror_checkbox.get())
        }
        return params

    def send_message(self):
        if self.is_busy:
            messagebox.showinfo("Info", "AI is busy. Please wait.")
            return
        user_text = self.request_entry.get().strip()
        if not user_text:
            return
        self.request_entry.delete(0, "end")
        self.display_message("user", user_text)
        if self.current_chat_id is not None:
            if self.current_chat_id not in self.chats:
                self.chats[self.current_chat_id] = {
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "messages": []
                }
            self.chats[self.current_chat_id]["messages"].append({"role": "user", "content": user_text})
            self.save_chats_to_file()
            self.update_history_list()
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
                    self.display_message("assistant", data)
                    if self.current_chat_id is not None:
                        if self.current_chat_id in self.chats:
                            self.chats[self.current_chat_id]["messages"].append({"role": "assistant", "content": data})
                            self.save_chats_to_file()
                            self.update_history_list()
                elif msg_type == "error":
                    messagebox.showerror("Error", data)
                elif msg_type == "done":
                    self.is_busy = False
        except queue.Empty:
            pass
        self.root.after(100, self.poll_queue)


if __name__ == "__main__":
    root = ctk.CTk()
    app = AlexRadarGUI(root)
    root.mainloop()