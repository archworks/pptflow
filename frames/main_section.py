import customtkinter as ctk
from tkinter import filedialog
import os
import threading
from utils import mylogger

logger = mylogger.get_logger(__name__)


class MainSection(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.grid_columnconfigure(0, weight=1)

        # Title
        self.title = ctk.CTkLabel(self,
                                  text=self.app.get_text("import_title"),
                                  font=ctk.CTkFont(size=24, weight="bold"))
        self.title.grid(row=0, column=0, pady=(0, 20))

        # File selection frame
        self.create_file_frame()

        # Settings frame
        self.create_settings_frame()

        # Progress frame
        # self.create_progress_frame()

    def create_file_frame(self):
        frame = ctk.CTkFrame(self)
        frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        frame.grid_columnconfigure(1, weight=1)

        # File selection
        self.file_path = ctk.CTkEntry(frame, placeholder_text=self.app.get_text("select_ppt"))
        self.file_path.grid(row=0, column=1, padx=(10, 10), pady=10, sticky="ew")

        self.browse_button = ctk.CTkButton(frame,
                                           text=self.app.get_text("browse"),
                                           command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=(0, 10), pady=10)

    def create_settings_frame(self):
        frame = ctk.CTkFrame(self)
        frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))
        frame.grid_columnconfigure(1, weight=1)

        # Basic settings
        settings = {
            "video_format": ["MP4", "AVI", "MOV"],
            "video_quality": ["High", "Medium", "Low"],
            "audio_language": ["English", "Chinese", "Japanese"]
        }

        for i, (key, values) in enumerate(settings.items()):
            label = ctk.CTkLabel(frame, text=f"{self.app.get_text(key)}:")
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            combobox = ctk.CTkComboBox(frame, values=values)
            combobox.grid(row=i, column=1, padx=10, pady=5, sticky="ew")

    def create_progress_frame(self):
        frame = ctk.CTkFrame(self)
        frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 10))
        frame.grid_columnconfigure(0, weight=1)

        # Status label
        self.status = ctk.CTkLabel(frame, text=self.app.get_text("ready"))
        self.status.grid(row=1, column=0, pady=(0, 5))

        # Export button
        self.export_button = ctk.CTkButton(frame,
                                           text=self.app.get_text("start_export"),
                                           command=self.start_export)
        self.export_button.grid(row=2, column=0, pady=(0, 10))

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PowerPoint files", "*.ppt;*.pptx")]
        )
        if file_path:
            self.file_path.delete(0, "end")
            self.file_path.insert(0, file_path)

    def start_export(self):
        # Add export logic here
        pass

    def update_language(self):
        self.title.configure(text=self.app.get_text("import_title"))
        self.file_path.configure(placeholder_text=self.app.get_text("select_ppt"))
        self.browse_button.configure(text=self.app.get_text("browse"))
        self.export_button.configure(text=self.app.get_text("start_export"))
        self.status.configure(text=self.app.get_text("ready"))
