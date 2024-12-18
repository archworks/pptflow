import customtkinter as ctk
from tkinter import filedialog, messagebox
from utils import mylogger
from utils import setting_dic as sd

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)


def create_combo_box(parent, index, options, variable, command=None):
    for i, (key, values) in enumerate(options.items()):
        label = ctk.CTkLabel(parent, text=f"{key}:")
        label.grid(row=index + i + 1, column=0, padx=20, pady=5, sticky="w")

        # Create a StringVar variable for each ComboBox
        var = ctk.StringVar(value=values[0])
        variable[key] = var

        combo = ctk.CTkComboBox(parent, values=values, variable=var)
        combo.grid(row=index + i + 1, column=1, padx=20, pady=5)


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
        self.create_cache_path()
        self.create_audio_settings()
        self.create_video_settings()
        self.create_subtitle_settings()
        self.create_save_button()

    def create_cache_path(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=0, column=0, padx=0, pady=(0, 10), sticky="ew")
        # Cache path
        self.cache_label = ctk.CTkLabel(frame, text=self.app.get_text("cache_path"))
        self.cache_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.cache_path_var = ctk.StringVar(value=self.app.setting.temp_dir)
        self.cache_path = ctk.CTkEntry(frame, width=300, textvariable=self.cache_path_var)
        self.cache_path.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        self.browse_button = ctk.CTkButton(frame,
                                           text=self.app.get_text("browse"),
                                           command=self.browse_cache_path)
        self.browse_button.grid(row=0, column=2, padx=20, pady=10)

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
            self.app.get_text("tts_server"): sd.tts_servers,
            self.app.get_text("audio_language"): [self.app.get_text(s) for s in sd.audio_languages],
            self.app.get_text("audio_voice_type"): sd.audio_voice_type,
            self.app.get_text("audio_speed"): sd.audio_speeds
        }

        create_combo_box(frame, 0, self.audio_settings, self.audio_settings_vars)
        self.audio_settings_vars[self.app.get_text("tts_server")].set(self.app.setting.tts_service_provider)
        self.audio_settings_vars[self.app.get_text("audio_language")].set(self.app.get_text(self.app.current_language))
        self.audio_settings_vars[self.app.get_text("audio_voice_type")].set(self.app.setting.narration_voice_name)
        self.audio_settings_vars[self.app.get_text("audio_speed")].set(self.app.setting.narration_voice_speed)

    def create_video_settings(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=2, column=0, padx=0, pady=(0, 10), sticky="ew")

        title = ctk.CTkLabel(
            frame,
            text=self.app.get_text("video_settings"),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Export path
        self.path_label = ctk.CTkLabel(frame, text=self.app.get_text("export_path"))
        self.path_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.export_path = ctk.CTkEntry(frame, width=300, textvariable=self.export_path_var)
        self.export_path.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

        self.browse_btn = ctk.CTkButton(
            frame,
            text=self.app.get_text("browse"),
            command=self.browse_export_path
        )
        self.browse_btn.grid(row=1, column=2, padx=20, pady=10)

        self.video_settings = {
            self.app.get_text("video_format"): sd.video_formats,
            self.app.get_text("video_size"): sd.video_sizes,
            self.app.get_text("video_fps"): sd.video_fps,
            self.app.get_text("video_threads"): sd.video_processing_threads
        }
        create_combo_box(frame, 1, self.video_settings, self.video_settings_vars)
        self.video_settings_vars[self.app.get_text("video_format")].set(self.app.setting.video_format)
        self.video_settings_vars[self.app.get_text("video_size")].set(f'{self.app.setting.video_width}x{self.app.setting.video_height}')
        self.video_settings_vars[self.app.get_text("video_fps")].set(self.app.setting.video_fps)
        self.video_settings_vars[self.app.get_text("video_threads")].set(self.app.setting.video_processing_threads)

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
            self.app.get_text("font_type"): [key for key in sd.subtitle_font_dict],
            self.app.get_text("font_size"): [str(i) for i in range(18, 49, 2)],
            self.app.get_text("font_color"): [self.app.get_text(s) for s in sd.font_colors],
            self.app.get_text("border_color"): [self.app.get_text(s) for s in sd.border_colors],
            self.app.get_text("border_width"): sd.border_widths
        }
        create_combo_box(frame, 0, self.subtitle_settings, self.subtitle_settings_vars)
        self.subtitle_settings_vars[self.app.get_text("font_type")].set(self.app.setting.subtitle_font)
        self.subtitle_settings_vars[self.app.get_text("font_size")].set(self.app.setting.subtitle_font_size)
        self.subtitle_settings_vars[self.app.get_text("font_color")].set(self.app.get_text(self.app.setting.subtitle_color))
        self.subtitle_settings_vars[self.app.get_text("border_color")].set(self.app.get_text(self.app.setting.subtitle_stroke_color))
        self.subtitle_settings_vars[self.app.get_text("border_width")].set(self.app.setting.subtitle_stroke_width)

    def create_save_button(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=4, column=0, padx=0, pady=(0, 10), sticky="ew")
        self.save_button = ctk.CTkButton(frame, text=self.app.get_text("save_settings"), command=self.save_settings)
        self.save_button.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

    def save_settings(self):
        if self.cache_path_var.get():
            self.app.setting.temp_dir = self.cache_path_var.get()
            logger.info(f"Updated cache path: {self.app.setting.temp_dir}")
        else:
            logger.warning(self.app.get_text("path_invalid"))
        self.update_audio_settings()
        self.update_video_settings()
        self.update_subtitle_settings()
        messagebox.showinfo("Success", "Settings saved successfully!")
        logger.info(f"Settings saved successfully!")

    def update_audio_settings(self):
        # Gets the currently selected value for each ComboBox by variable
        audio_engine = self.audio_settings_vars[self.app.get_text("tts_server")].get()
        audio_language = self.audio_settings_vars[self.app.get_text("audio_language")].get()
        audio_voice_type = self.audio_settings_vars[self.app.get_text("audio_voice_type")].get()
        audio_speed = float(self.audio_settings_vars[self.app.get_text("audio_speed")].get().split("x")[0])

        # update the app setting
        self.app.setting.tts_service_provider = audio_engine
        self.app.setting.audio_language = self.app.text_to_key(audio_language)
        self.app.setting.audio_voice_type = audio_voice_type
        self.app.setting.audio_speed = audio_speed

        logger.info(
            f"Updated audio settings - Engine: {audio_engine}, Language: {audio_language}, Voice Type: {audio_voice_type}, Speed: {audio_speed}")

    def update_video_settings(self):
        video_format = self.video_settings_vars[self.app.get_text("video_format")].get()
        video_size = self.video_settings_vars[self.app.get_text("video_size")].get().split("x")
        video_fps = self.video_settings_vars[self.app.get_text("video_fps")].get().split("fps")[0]
        video_processing_threads = self.video_settings_vars[self.app.get_text("video_threads")].get()
        self.app.setting.video_path = self.export_path_var.get() if self.export_path_var.get() else None
        self.app.setting.video_format = video_format
        self.app.setting.video_width = video_size[0]
        self.app.setting.video_height = video_size[1]
        self.app.setting.video_fps = int(video_fps)
        self.app.setting.video_processing_threads = int(video_processing_threads)
        logger.info(f"Updated video settings - Video_path:{self.app.setting.video_path}, "
                    f"Format: {video_format}, Size: {video_size}, FPS: {video_fps}, "
                    f"Threads: {video_processing_threads}")

    def update_subtitle_settings(self):
        subtitle_font = self.subtitle_settings_vars[self.app.get_text("font_type")].get()
        subtitle_font_size = self.subtitle_settings_vars[self.app.get_text("font_size")].get()
        subtitle_font_color = self.subtitle_settings_vars[self.app.get_text("font_color")].get().lower()
        subtitle_border_color = self.subtitle_settings_vars[self.app.get_text("border_color")].get().lower()
        subtitle_border_width = self.subtitle_settings_vars[self.app.get_text("border_width")].get()
        self.app.setting.subtitle_font = sd.subtitle_font_dict[subtitle_font]
        self.app.setting.subtitle_font_size = int(subtitle_font_size)
        self.app.setting.subtitle_color = self.app.text_to_key(subtitle_font_color)
        self.app.setting.subtitle_stroke_color = self.app.text_to_key(subtitle_border_color)
        self.app.setting.subtitle_stroke_width = int(subtitle_border_width)
        logger.info(f"Updated subtitle settings - Font: {subtitle_font}, Font Size: {subtitle_font_size}, "
                    f"Font Color: {subtitle_font_color}, Border Color: {subtitle_border_color}, "
                    f"Border Width: {subtitle_border_width}")

    def browse_cache_path(self):
        path = filedialog.askdirectory()
        if path:
            self.app.setting.temp_dir = path
            self.cache_path.delete(0, "end")
            self.cache_path.insert(0, path)

    def browse_export_path(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4")]
        )
        if path:
            self.export_path_var.set(path)

    def update_language(self):
        self.title.configure(text=self.app.get_text("export_settings"))
        self.cache_label.configure(text=self.app.get_text("cache_path"))
        self.path_label.configure(text=self.app.get_text("export_path"))
        self.browse_btn.configure(text=self.app.get_text("browse"))
        self.create_audio_settings()
        self.create_video_settings()
        self.create_subtitle_settings()

    def refresh(self):
        if self.export_path_var.get() == "" and self.app.setting.video_path:
            self.export_path_var.set(self.app.setting.video_path)
