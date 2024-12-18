# Author: Valley-e
# Date: 2024/12/18  
# Description:

from dotenv import load_dotenv
import os
import customtkinter as ctk
from pptflow.setting import Setting
from utils import setting_dic as sd
from .file_section import FileSection
from .export_section import ExportSection
from .settings_section import SettingsSection
import json
import sys
from utils import mylogger

# Load environment variables
load_dotenv()
# Setup logger
logger = mylogger.get_logger(__name__)
logger.info("Application started")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.setting = Setting()
        self.current_language = self.setting.language
        self.language_modes = get_locales_subdirectories() if len(
            get_locales_subdirectories()) > 0 else sd.language_mode
        self._translations_cache = {}  # Add translation cache
        self.translations = self.get_translation()

        # Configure window
        self.title("PPT FLOW")
        self.center_window()

        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create navigation frame
        self.create_navigation_frame()

        # Create main frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Initialize frames
        self.frames = {}
        frame_classes = {
            "video_generation": FileSection,
            "export_settings": ExportSection
        }

        for name, frame_class in frame_classes.items():
            frame = frame_class(self.main_frame, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Add copyright notice
        self.copyright_frame = ctk.CTkFrame(self, height=30, corner_radius=0)
        self.copyright_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.copyright_label = ctk.CTkLabel(
            self.copyright_frame,
            text="© 2024 ArchWorks. All rights reserved.",
            font=ctk.CTkFont(size=12)
        )
        self.copyright_label.grid(row=0, column=0, padx=20, pady=5)

        # Show default frame
        self.select_frame("video_generation")

    def create_navigation_frame(self):
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.nav_label = ctk.CTkLabel(
            self.navigation_frame,
            text=self.get_text("nav_menu"),
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.nav_label.grid(row=0, column=0, padx=20, pady=20)

        # Navigation buttons
        self.nav_buttons = []
        nav_items = ["video_generation", "export_settings"]

        index = 0
        for i, item in enumerate(nav_items):
            button = ctk.CTkButton(
                self.navigation_frame,
                corner_radius=0,
                height=40,
                border_spacing=10,
                text=self.get_text(item),
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                anchor="center",
                command=lambda x=item: self.select_frame(x)
            )
            button.grid(row=i + 1, column=0, sticky="ew")
            self.nav_buttons.append((button, item))
            index = i

        self.create_language_mode(index+3)
        self.create_theme_mode(index+5)
        self.create_scale_mode(index+7)

    def create_language_mode(self, index):
        # Language selection
        self.language_label = ctk.CTkLabel(self.navigation_frame, text=self.get_text("ui_language"), anchor="w")
        self.language_label.grid(row=index, column=0, padx=20, pady=(10, 0), sticky="s")

        self.language_list = [self.get_text(language) for language in self.language_modes]
        self.language_setting = ctk.CTkComboBox(self.navigation_frame,
                                                values=self.language_list,
                                                command=self.on_language_change)
        self.language_setting.grid(row=index+1, column=0, padx=20, pady=(10, 10))

    def create_theme_mode(self, index):
        # Theme selection
        self.theme_label = ctk.CTkLabel(self.navigation_frame, text=self.get_text("theme"), anchor="w")
        self.theme_label.grid(row=index, column=0, padx=20, pady=(10, 0))

        self.theme = ctk.CTkComboBox(self.navigation_frame, values=[self.get_text("dark"),
                                                                    self.get_text("light"),
                                                                    self.get_text("system")],
                                     command=self.change_appearance_mode_event)
        self.theme.grid(row=index+1, column=0, padx=20, pady=(10, 10))
        self.theme_map = {self.translations[key]: key for key in ['dark', 'light', 'system']}

    def create_scale_mode(self, index):
        # Scaling selection
        self.scaling_label = ctk.CTkLabel(self.navigation_frame, text=self.get_text("ui_scaling"), anchor="w")
        self.scaling_label.grid(row=index, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkComboBox(self.navigation_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                   command=self.change_scaling_event)
        self.scaling_optionemenu.set("100%")
        self.scaling_optionemenu.grid(row=index+1, column=0, padx=20, pady=(10, 20))

    def select_frame(self, name):
        # Update button colors
        for button, item in self.nav_buttons:
            if item == name:
                button.configure(fg_color=("gray75", "gray25"))
            else:
                button.configure(fg_color="transparent")

        # Show selected frame
        frame = self.frames[name]
        frame.refresh()
        frame.tkraise()

    def center_window(self):
        """Center the window on the screen."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 1000
        window_height = 580
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def get_text(self, key):
        return self.translations.get(key, key)

    def text_to_key(self, text):
        """Convert display text back to key"""
        for key, value in self.translations.items():
            if value == text:
                return key
        return text

    def on_language_change(self, language_value):
        # Dynamically generate the mapping based on the language list
        language = self.text_to_key(language_value)
        self.change_language(language)
        self.create_navigation_frame()
        self.language_setting.set(self.get_text(self.current_language))

    def change_appearance_mode_event(self, new_appearance_mode: str):
        new_mode = self.theme_map[new_appearance_mode]
        # self.theme.set()
        ctk.set_appearance_mode(new_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def change_language(self, language):
        if language in self.language_modes:
            self.current_language = language
            self.translations = self.get_translation()
            # Update navigation
            self.nav_label.configure(text=self.get_text("nav_menu"))
            logger.info(f"Language changed to {language}")
            for button, item in self.nav_buttons:
                button.configure(text=self.get_text(item))
            # Update all frames
            for frame in self.frames.values():
                frame.update_language()
            # Update others
            self.copyright_label.configure(text=self.get_text("copyright"))
            self.language_label.configure(text=self.get_text("ui_language"))
            self.theme_label.configure(text=self.get_text("theme"))
            self.theme.set(self.get_text(self.theme_map[self.theme.get()]))
            self.theme_map = {self.translations[key]: key for key in ['dark', 'light', 'system']}
            self.scaling_label.configure(text=self.get_text("ui_scaling"))

    def get_translation(self):
        if self.current_language in self._translations_cache:
            return self._translations_cache[self.current_language]

        locale_dir = resource_path(os.path.join('locales', self.current_language))
        translation_file = os.path.join(locale_dir, 'messages.json')

        if not os.path.exists(translation_file):
            locale_dir = resource_path(os.path.join('locales', self.language_modes[0]))
            translation_file = os.path.join(locale_dir, 'messages.json')

        with open(translation_file, 'r', encoding='utf-8') as f:
            translations = json.load(f)

        self._translations_cache[self.current_language] = translations
        return translations


def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):  # 打包后运行环境
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def get_locales_subdirectories():
    # Get the absolute path to the current file
    current_file_path = os.path.abspath(__file__)
    # Get the directory path of the current file
    current_directory = os.path.dirname(current_file_path)
    # Get the parent path of the current directory
    parent_directory = os.path.dirname(current_directory)
    # Get the absolute path of the parent directory
    language_locales_path = os.path.join(parent_directory, 'locales')
    try:
        # Get all entries in the directory
        entries = os.listdir(language_locales_path)
        # Filter out subdirectories
        subdirectories = [
            entry for entry in entries
            if os.path.isdir(os.path.join(language_locales_path, entry)) and entry != '__pycache__'
        ]
        return subdirectories
    except FileNotFoundError:
        logger.error(f"Directory {language_locales_path} doesn't exist!")
        return []
    except PermissionError:
        logger.error(f"No permission to access the directory {language_locales_path}")
        return []
