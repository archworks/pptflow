import pptflow.ppt2video as ppt2video
import json
from pptflow.setting import Setting
import customtkinter as ctk
import os
from frames.import_frame import ImportFrame
from frames.basic_settings import BasicSettingsFrame
from frames.advanced_settings import AdvancedSettingsFrame
from frames.user_settings import UserSettingsFrame
from frames.system_settings import SystemSettingsFrame
from frames.export_frame import ExportFrame
# from locales.languages import TRANSLATIONS
from utils import mylogger

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


# ppt_path = input("请输入ppt路径: ")
# setting = Setting()
# ppt2video.process(ppt_path, setting=setting)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_language = "en"
        self.language_modes = get_locales_subdirectories() if len(
            get_locales_subdirectories()) > 0 else Setting.language_mode
        self.translations = self.get_translation()
        self.setting = Setting()

        # Configure window
        self.title("PPT to Video Converter")
        self.geometry("1200x800")

        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(7, weight=1)

        self.nav_label = ctk.CTkLabel(self.navigation_frame,
                                      text=self.get_text("nav_menu"),
                                      compound="left",
                                      font=ctk.CTkFont(size=15, weight="bold"))
        self.nav_label.grid(row=0, column=0, padx=20, pady=20)

        # Navigation buttons
        self.nav_buttons = []
        nav_items = ["import_ppt", "basic_settings", "advanced_settings",
                     "user_settings", "system_settings", "export_video"]

        for i, item in enumerate(nav_items):
            button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                   border_spacing=10, text=self.get_text(item),
                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                   hover_color=("gray70", "gray30"),
                                   anchor="w", command=lambda x=item: self.select_frame(x))
            button.grid(row=i + 1, column=0, sticky="ew")
            self.nav_buttons.append((button, item))

        # Create main frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Initialize frames
        self.frames = {}
        frame_classes = {
            "import_ppt": ImportFrame,
            "basic_settings": BasicSettingsFrame,
            "advanced_settings": AdvancedSettingsFrame,
            "user_settings": UserSettingsFrame,
            "system_settings": SystemSettingsFrame,
            "export_video": ExportFrame
        }

        for name, frame_class in frame_classes.items():
            frame = frame_class(self.main_frame, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show default frame
        self.select_frame("import_ppt")

    def get_text(self, key):
        return self.translations.get(key)

    def select_frame(self, name):
        # Update button colors
        for button, item in self.nav_buttons:
            if item == name:
                button.configure(fg_color=("gray75", "gray25"))
            else:
                button.configure(fg_color="transparent")

        # Show selected frame
        frame = self.frames[name]
        frame.tkraise()

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

    def get_translation(self) -> dict:
        locale_dir = os.path.join('locales', self.current_language)
        translation_file = os.path.join(locale_dir, 'messages.json')

        if not os.path.exists(translation_file):
            # Fall back to default locale (English)
            locale_dir = os.path.join('locales', self.language_modes[0])
            translation_file = os.path.join(locale_dir, 'messages.json')

        with open(translation_file, 'r', encoding='utf-8') as f:
            translations = json.load(f)

        return translations


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
        logger.error(f"目录 {language_locales_path} 不存在")
        return []
    except PermissionError:
        logger.error(f"没有权限访问目录 {language_locales_path}")
        return []


if __name__ == "__main__":
    app = App()
    try:
        app.mainloop()
    except KeyboardInterrupt as e:
        logger.error(e)
