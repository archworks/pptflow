from dotenv import load_dotenv
import os
import customtkinter as ctk
from pptflow.setting import Setting
from frames.file_section import FileSection
from frames.export_section import ExportSection
from frames.settings_section import SettingsSection
import json
import sys

from utils import mylogger

logger = mylogger.get_logger(__name__)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_language = "en"
        self.language_modes = get_locales_subdirectories() if len(
            get_locales_subdirectories()) > 0 else Setting.language_mode
        self._translations_cache = {}  # Add translation cache
        self.translations = self.get_translation()
        self.setting = Setting()

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
            "export_settings": ExportSection,
            "system_settings": SettingsSection
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
        nav_items = ["video_generation", "export_settings", "system_settings"]

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
                anchor="w",
                command=lambda x=item: self.select_frame(x)
            )
            button.grid(row=i + 1, column=0, sticky="ew")
            self.nav_buttons.append((button, item))

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
    language_locales_path = os.path.join(current_directory, 'locales')
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


if __name__ == "__main__":
    # Load the .env file
    load_dotenv()
    app = App()
    logger.info("Application started")
    app.mainloop()
