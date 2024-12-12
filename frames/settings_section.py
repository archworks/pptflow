import customtkinter as ctk
from tkinter import filedialog
from utils import mylogger

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)


class SettingsSection(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Title
        self.title = ctk.CTkLabel(self,
                                  text=self.app.get_text("system_title"),
                                  font=ctk.CTkFont(size=24, weight="bold"))
        self.title.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Create scrollable container
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Settings frame
        self.create_settings_frame()

    def create_settings_frame(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=0, column=0, padx=0, pady=(0, 10), sticky="ew")

        # Cache path
        self.cache_label = ctk.CTkLabel(frame, text=self.app.get_text("cache_path"))
        self.cache_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.cache_path_var = ctk.StringVar(value=self.app.setting.temp_dir)
        self.cache_path = ctk.CTkEntry(frame, width=300, textvariable=self.cache_path_var)
        self.cache_path.grid(row=0, column=1, padx=5, pady=10)

        self.browse_button = ctk.CTkButton(frame,
                                           text=self.app.get_text("browse"),
                                           command=self.browse_cache_path)
        self.browse_button.grid(row=0, column=2, padx=(0, 20), pady=10)

        # Language selection
        self.lang_label = ctk.CTkLabel(frame, text=self.app.get_text("ui_language"))
        self.lang_label.grid(row=1, column=0, padx=20, pady=10)

        self.language_list = [self.app.get_text(language) for language in self.app.language_modes]
        self.language_setting = ctk.CTkComboBox(frame,
                                                values=self.language_list,
                                                command=self.on_language_change)
        self.language_setting.grid(row=1, column=1, padx=5, pady=10, sticky="w")
        # self.language.set(self.app.current_language)

        # Theme selection
        self.theme_label = ctk.CTkLabel(frame, text=self.app.get_text("theme"))
        self.theme_label.grid(row=2, column=0, padx=20, pady=10)

        self.theme = ctk.CTkComboBox(frame, values=[self.app.get_text("dark"),
                                                    self.app.get_text("light"),
                                                    self.app.get_text("system")],
                                     command=self.change_appearance_mode_event)
        self.theme.grid(row=2, column=1, padx=5, pady=10, sticky="w")
        self.theme_map = {self.app.translations[key]: key for key in ['dark', 'light', 'system']}

        self.scaling_label = ctk.CTkLabel(frame, text=self.app.get_text("ui_scaling"))
        self.scaling_label.grid(row=3, column=0, padx=20, pady=10)
        self.scaling_optionemenu = ctk.CTkComboBox(frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                   command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=3, column=1, padx=5, pady=10, sticky="w")

        # Save button
        self.save_button = ctk.CTkButton(frame,
                                         text=self.app.get_text("save_settings"))
        self.save_button.grid(row=4, column=0, columnspan=3, padx=20, pady=20)

    def browse_cache_path(self):
        path = filedialog.askdirectory()
        if path:
            self.app.setting.temp_dir = path
            self.cache_path.delete(0, "end")
            self.cache_path.insert(0, path)

    def on_language_change(self, language_value):
        # Dynamically generate the mapping based on the language list
        # language_modes = {self.app.get_text(key): key for key in self.app.language_modes}
        # logger.debug(f"Language Modes: {language_modes}")
        language = self.app.text_to_key(language_value)
        self.app.change_language(language)
        self.create_settings_frame()
        # self.language_list = [self.app.get_text(language) for language in self.app.language_modes]
        # self.language_setting.configure(values=self.language_list)
        self.language_setting.set(self.app.get_text(self.app.current_language))

    def change_appearance_mode_event(self, new_appearance_mode: str):
        new_mode = self.theme_map[new_appearance_mode]
        # self.theme.set()
        ctk.set_appearance_mode(new_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    # Update the language of System Settings frame
    def update_language(self):
        self.title.configure(text=self.app.get_text("system_title"))
        self.lang_label.configure(text=self.app.get_text("ui_language"))
        self.cache_label.configure(text=self.app.get_text("cache_path"))
        self.theme_label.configure(text=self.app.get_text("theme"))
        self.browse_button.configure(text=self.app.get_text("browse"))
        self.save_button.configure(text=self.app.get_text("save_settings"))
        self.scaling_label.configure(text=self.app.get_text("ui_scaling"))

        self.theme.set(self.app.get_text(self.theme_map[self.theme.get()]))
        self.theme_map = {self.app.translations[key]: key for key in ['dark', 'light', 'system']}
        # Update theme combobox values
        self.theme.configure(values=[
            self.app.get_text("dark"),
            self.app.get_text("light"),
            self.app.get_text("system")
        ])

    def refresh(self):
        pass
