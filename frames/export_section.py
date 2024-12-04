import customtkinter as ctk
from tkinter import filedialog


class ExportSection(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Title
        self.title = ctk.CTkLabel(
            self,
            text=self.app.get_text("export_settings"),
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title.grid(row=0, column=0, padx=20, pady=20)

        # Create scrollable frame for settings
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Add settings sections
        self.create_export_path()
        self.create_audio_settings()
        self.create_video_settings()
        self.create_subtitle_settings()

    def create_export_path(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=0, column=0, padx=0, pady=(0, 10), sticky="ew")

        # Export path
        self.path_label = ctk.CTkLabel(frame, text=self.app.get_text("export_path"))
        self.path_label.grid(row=0, column=0, padx=20, pady=10)

        self.export_path = ctk.CTkEntry(frame, width=300)
        self.export_path.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        self.browse_btn = ctk.CTkButton(
            frame,
            text=self.app.get_text("browse"),
            command=self.browse_export_path
        )
        self.browse_btn.grid(row=0, column=2, padx=20, pady=10)

    def create_audio_settings(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=1, column=0, padx=0, pady=(0, 10), sticky="ew")

        title = ctk.CTkLabel(
            frame,
            text=self.app.get_text("audio_settings"),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        settings = {
            self.app.get_text("audio_engine"): ["Azure TTS", "讯飞 TTS"],
            self.app.get_text("audio_language"): ["Simplified Chinese", "English", "Japanese"],
            self.app.get_text("audio_voice_type"): ["zh-CN-YunjianNeural", "xxxx"],
            self.app.get_text("audio_speed"): ["0.8x", "1.0x", "1.2x", "1.5x"]
        }

        for i, (key, values) in enumerate(settings.items()):
            label = ctk.CTkLabel(frame, text=f"{key}:")
            label.grid(row=i + 1, column=0, padx=20, pady=5, sticky="w")

            combo = ctk.CTkComboBox(frame, values=values)
            combo.grid(row=i + 1, column=1, padx=20, pady=5)

    def create_video_settings(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=2, column=0, padx=0, pady=(0, 10), sticky="ew")

        title = ctk.CTkLabel(
            frame,
            text=self.app.get_text("video_settings"),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        settings = {
            self.app.get_text("video_format"): ["MP4", "AVI", "MOV"],
            self.app.get_text("video_size"): ["1920x1080", "1280x720", "854x480"],
            self.app.get_text("video_fps"): ["10fps", "30fps", "24fps"]
        }

        for i, (key, values) in enumerate(settings.items()):
            label = ctk.CTkLabel(frame, text=f"{key}:")
            label.grid(row=i + 1, column=0, padx=20, pady=5, sticky="w")

            combo = ctk.CTkComboBox(frame, values=values)
            combo.grid(row=i + 1, column=1, padx=20, pady=5)

    def create_subtitle_settings(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=3, column=0, padx=0, pady=(0, 10), sticky="ew")

        title = ctk.CTkLabel(
            frame,
            text=self.app.get_text("subtitle_settings"),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        settings = {
            self.app.get_text("font_type"): ["Microsoft YaHei", "Calibri", "Arial", "Song"],
            self.app.get_text("font_size"): ["12", "14", "16", "18", "20"],
            self.app.get_text("font_color"): ["White", "Black", "Yellow", "Red"],
            self.app.get_text("border_color"): ["Black", "White", "No"]
        }

        for i, (key, values) in enumerate(settings.items()):
            label = ctk.CTkLabel(frame, text=f"{key}:")
            label.grid(row=i + 1, column=0, padx=20, pady=5, sticky="w")

            combo = ctk.CTkComboBox(frame, values=values)
            combo.grid(row=i + 1, column=1, padx=20, pady=5)

    def browse_export_path(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4")]
        )
        if path:
            self.export_path.delete(0, "end")
            self.export_path.insert(0, path)

    def update_language(self):
        self.title.configure(text=self.app.get_text("export_settings"))
        self.path_label.configure(text=self.app.get_text("export_path"))
        self.export_path.configure(placeholder_text=self.app.get_text("export_path"))
        self.browse_btn.configure(text=self.app.get_text("browse"))
        self.create_audio_settings()
        self.create_video_settings()
        self.create_subtitle_settings()

    def start_export(self):
        # Add export logic here
        pass
