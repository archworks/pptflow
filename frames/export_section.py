import customtkinter as ctk
from tkinter import filedialog, messagebox
from utils import mylogger

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)


def create_combo_box(parent, options, variable, command=None):
    for i, (key, values) in enumerate(options.items()):
        label = ctk.CTkLabel(parent, text=f"{key}:")
        label.grid(row=i + 1, column=0, padx=20, pady=5, sticky="w")

        # Create a StringVar variable for each ComboBox
        var = ctk.StringVar(value=values[0])
        variable[key] = var

        combo = ctk.CTkComboBox(parent, values=values, variable=var)
        combo.grid(row=i + 1, column=1, padx=20, pady=5)


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

        # Create a dict for audio/video/subtitle settings
        self.export_path_var = ctk.StringVar()
        self.audio_settings_vars = {}
        self.video_settings_vars = {}
        self.subtitle_settings_vars = {}

        # Add settings sections
        self.create_export_path()
        self.create_audio_settings()
        self.create_video_settings()
        self.create_subtitle_settings()
        self.create_save_button()

    def create_export_path(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=0, column=0, padx=0, pady=(0, 10), sticky="ew")

        # Export path
        self.path_label = ctk.CTkLabel(frame, text=self.app.get_text("export_path"))
        self.path_label.grid(row=0, column=0, padx=20, pady=10)

        self.export_path = ctk.CTkEntry(frame, width=300, textvariable=self.export_path_var)
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

        self.audio_settings = {
            self.app.get_text("audio_engine"): ["azure", "xunfei"],
            self.app.get_text("audio_language"): [self.app.get_text("zh"), self.app.get_text("en"),
                                                  self.app.get_text("jp")],
            self.app.get_text("audio_voice_type"): ["zh-CN-YunjianNeural", "xxxx"],
            self.app.get_text("audio_speed"): ["1.0x", "0.8x", "1.2x", "1.5x"]
        }

        create_combo_box(frame, self.audio_settings, self.audio_settings_vars)

    def create_video_settings(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=2, column=0, padx=0, pady=(0, 10), sticky="ew")

        title = ctk.CTkLabel(
            frame,
            text=self.app.get_text("video_settings"),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.video_settings = {
            self.app.get_text("video_format"): ["MP4", "AVI", "MOV"],
            self.app.get_text("video_size"): ["1280x720", "1920x1080", "854x480"],
            self.app.get_text("video_fps"): ["10fps", "30fps", "24fps"]
        }
        create_combo_box(frame, self.video_settings, self.video_settings_vars)

    def create_subtitle_settings(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=3, column=0, padx=0, pady=(0, 10), sticky="ew")

        title = ctk.CTkLabel(
            frame,
            text=self.app.get_text("subtitle_settings"),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.subtitle_settings = {
            self.app.get_text("font_type"): [key for key in self.app.setting.subtitle_font_dict],
            self.app.get_text("font_size"): [str(i) for i in range(18, 49, 2)],
            self.app.get_text("font_color"): [self.app.get_text("white"),
                                              self.app.get_text("black"),
                                              self.app.get_text("red"),
                                              self.app.get_text("yellow")],
            self.app.get_text("border_color"): [self.app.get_text("black"), self.app.get_text("white"),
                                                self.app.get_text("no_color")],
            self.app.get_text("border_width"): ["0", "1", "2", "3", "4"]
        }
        create_combo_box(frame, self.subtitle_settings, self.subtitle_settings_vars)
        self.subtitle_settings_vars[self.app.get_text("font_type")].set("Microsoft YaHei")

    def create_save_button(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=4, column=0, padx=0, pady=(0, 10), sticky="ew")
        self.save_button = ctk.CTkButton(frame, text=self.app.get_text("save_settings"), command=self.save_settings)
        self.save_button.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

    def save_settings(self):
        self.app.setting.video_path = self.export_path_var if self.export_path_var else None
        if self.app.setting.video_path:
            logger.info(f"Updated video settings - Video_path:{self.app.setting.video_path}")
        self.update_audio_settings()
        self.update_video_settings()
        self.update_subtitle_settings()
        messagebox.showinfo("Success", "Settings saved successfully!")
        logger.info(f"Settings saved successfully!")

    def update_audio_settings(self):
        # Gets the currently selected value for each ComboBox by variable
        audio_engine = self.audio_settings_vars[self.app.get_text("audio_engine")].get()
        audio_language = self.audio_settings_vars[self.app.get_text("audio_language")].get()
        audio_voice_type = self.audio_settings_vars[self.app.get_text("audio_voice_type")].get()
        audio_speed = float(self.audio_settings_vars[self.app.get_text("audio_speed")].get().split("x")[0])

        # update the app setting
        self.app.setting.tts_service_provider = audio_engine
        self.app.setting.audio_language = audio_language
        self.app.setting.audio_voice_type = audio_voice_type
        self.app.setting.audio_speed = audio_speed

        logger.info(
            f"Updated audio settings - Engine: {audio_engine}, Language: {audio_language}, Voice Type: {audio_voice_type}, Speed: {audio_speed}")

    def update_video_settings(self):
        video_format = self.video_settings_vars[self.app.get_text("video_format")].get()
        video_size = self.video_settings_vars[self.app.get_text("video_size")].get().split("x")
        video_fps = self.video_settings_vars[self.app.get_text("video_fps")].get().split("fps")[0]
        self.app.setting.video_format = video_format
        self.app.setting.video_width = video_size[0]
        self.app.setting.video_height = video_size[1]
        self.app.setting.video_fps = video_fps
        logger.info(f"Updated video settings - Format: {video_format}, Size: {video_size}, FPS: {video_fps}")

    def update_subtitle_settings(self):
        subtitle_font = self.app.setting.subtitle_font_dict[
            self.subtitle_settings_vars[self.app.get_text("font_type")].get()]
        subtitle_font_size = self.subtitle_settings_vars[self.app.get_text("font_size")].get()
        subtitle_font_color = self.subtitle_settings_vars[self.app.get_text("font_color")].get().lower()
        subtitle_border_color = self.subtitle_settings_vars[self.app.get_text("border_color")].get().lower()
        subtitle_border_width = self.subtitle_settings_vars[self.app.get_text("border_width")].get()
        self.app.setting.subtitle_font = subtitle_font
        self.app.setting.subtitle_font_size = int(subtitle_font_size)
        self.app.setting.subtitle_color = subtitle_font_color
        self.app.setting.subtitle_stroke_color = subtitle_border_color
        self.app.setting.subtitle_stroke_width = int(subtitle_border_width)
        logger.info(f"Updated subtitle settings - Font: {subtitle_font}, Font Size: {subtitle_font_size}, "
                    f"Font Color: {subtitle_font_color}, Border Color: {subtitle_border_color}, "
                    f"Border Width: {subtitle_border_width}")

    def browse_export_path(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4")]
        )
        if path:
            self.export_path_var.set(path)

    def update_language(self):
        self.title.configure(text=self.app.get_text("export_settings"))
        self.path_label.configure(text=self.app.get_text("export_path"))
        self.browse_btn.configure(text=self.app.get_text("browse"))
        self.create_audio_settings()
        self.create_video_settings()
        self.create_subtitle_settings()

    def refresh(self):
        if self.export_path_var.get() == "" and self.app.setting.video_path:
            self.export_path_var.set(self.app.setting.video_path)
