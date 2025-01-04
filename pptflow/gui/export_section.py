import customtkinter as ctk
from tkinter import filedialog, messagebox
from pptflow.utils import mylogger, setting_dic as sd

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
        self.tts_settings_vars = {}
        # self.audio_settings_vars = {}
        self.video_settings_vars = {}
        self.subtitle_settings_vars = {}

        # Add settings sections
        self.create_tts_settings()
        self.create_cache_path()
        # self.create_audio_settings()
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

        self.browse_button = ctk.CTkButton(frame, width=100,
                                           text=self.app.get_text("browse"),
                                           command=self.browse_cache_path)
        self.browse_button.grid(row=0, column=2, padx=20, pady=10)

        self.clear_cache_button = ctk.CTkButton(frame, width=100,
                                                text=self.app.get_text("clear_cache"),
                                                command=self.app.clear_temp_cache)
        self.clear_cache_button.grid(row=0, column=3, padx=(0, 20), pady=10)

    def create_tts_settings(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=1, column=0, padx=0, pady=(0, 10), sticky="ew")

        title = ctk.CTkLabel(
            frame,
            text=self.app.get_text("tts_settings"),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.tts_providers_label = ctk.CTkLabel(
            frame,
            text=self.app.get_text("tts_service_provider"),
        )
        self.tts_providers_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.tts_providers_var = ctk.StringVar(value=self.app.setting.tts_service_provider)
        self.tts_providers = ctk.CTkComboBox(frame, values=sd.tts_service_providers, variable=self.tts_providers_var)
        self.tts_providers.grid(row=1, column=1, padx=5, pady=10)
        # 绑定选择变化的事件
        # self.tts_providers.bind("<<ComboboxSelected>>", lambda event: self.on_tts_provider_change)
        self.tts_providers_var.trace("w", lambda *args: self.on_tts_provider_change(frame))
        # 初始化加载当前选项的设置
        self.on_tts_provider_change(frame)

    def on_tts_provider_change(self, frame):
        # 清除之前的组件（如果需要）
        for widget in frame.winfo_children():
            if widget not in {self.tts_providers_label, self.tts_providers}:
                widget.destroy()

        # 根据选择的 TTS 提供商加载相应的设置 frame
        logger.info(f"Selected TTS Provider: {self.tts_providers_var.get()}")
        if self.tts_providers_var.get() == "pyttsx3":
            self.create_pyttsx3_settings(frame)
        elif self.tts_providers_var.get() == "azure":
            self.app.load_tts("azure")
            self.create_azure_settings(frame)
        # elif self.tts_providers_var.get() == "edge-tts":
        #     self.create_edge_tts_settings(frame)

    def create_pyttsx3_settings(self, frame):
        tts_settings = {
            self.app.get_text("audio_language"): [self.app.get_text(s) for s in sd.audio_languages]
        }
        create_combo_box(frame, 1, tts_settings, self.tts_settings_vars)
        self.tts_settings_vars[self.app.get_text("audio_language")].set(
            self.app.get_text(self.app.text_to_key(self.app.setting.audio_language)))

    def create_azure_settings(self, frame):
        tts_settings = {
            self.app.get_text("tts_speech_region"): sd.tts_speech_regions,
            self.app.get_text("tts_voice_type"): sd.tts_speech_voices,
        }
        create_combo_box(frame, 1, tts_settings, self.tts_settings_vars)
        # self.tts_settings_vars[self.app.get_text("tts_service_provider")].set(self.app.setting.tts_service_provider)
        self.tts_settings_vars[self.app.get_text("tts_speech_region")].set(self.app.setting.tts_speech_region)
        self.tts_settings_vars[self.app.get_text("tts_voice_type")].set(self.app.setting.tts_voice_type)
        # api key
        self.api_key_label = ctk.CTkLabel(frame, text=self.app.get_text("tts_api_key"))
        self.api_key_label.grid(row=2 + len(tts_settings), column=0, padx=20, pady=10, sticky="w")
        self.api_key_var = ctk.StringVar(value=self.app.setting.tts_azure_api_key)
        self.api_key = ctk.CTkEntry(frame, width=300, textvariable=self.api_key_var)
        self.api_key.grid(row=2 + len(tts_settings), column=1, padx=5, pady=10, sticky="ew")

    def create_edge_tts_settings(self, frame):
        # tts voice rate
        self.rate_slider_label = ctk.CTkLabel(frame, text=self.app.get_text("tts_voice_rate"))
        self.rate_slider_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        # 创建滑动条
        self.rate_slider = ctk.CTkSlider(frame, from_=-1, to=1, orientation="horizontal", command=self.update_progress)
        self.rate_slider.grid(row=2, column=1, padx=5, pady=10, sticky="ew")
        self.rate_slider.set(0)  # 初始滑动条值设置为 0（中间）
        # 创建显示进度的标签
        self.voice_rate = ctk.CTkLabel(frame, text="0%")
        self.voice_rate.grid(row=2, column=2, padx=5, pady=10, sticky="w")

        # 创建复位按钮
        self.reset_button = ctk.CTkButton(frame, width=100, text=self.app.get_text("reset"),
                                          command=self.reset_progress)
        self.reset_button.grid(row=2, column=3, padx=5, pady=10)

    # def create_audio_settings(self):
        # frame = ctk.CTkFrame(self.scrollable_frame)
        # frame.grid(row=2, column=0, padx=0, pady=(0, 10), sticky="ew")
        #
        # title = ctk.CTkLabel(
        #     frame,
        #     text=self.app.get_text("audio_settings"),
        #     font=ctk.CTkFont(size=16, weight="bold")
        # )
        # title.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        #
        # self.audio_settings = {
        #     self.app.get_text("audio_language"): [self.app.get_text(s) for s in sd.audio_languages],
            # self.app.get_text("audio_voice_type"): sd.audio_voice_type,
            # self.app.get_text("audio_speed"): sd.audio_speeds
        # }

        # create_combo_box(frame, 0, self.audio_settings, self.audio_settings_vars)
        # self.audio_settings_vars[self.app.get_text("audio_language")].set(self.app.get_text(self.app.setting.audio_language))
        # self.audio_settings_vars[self.app.get_text("audio_voice_type")].set(self.app.setting.tts_voice_type)
        # self.audio_settings_vars[self.app.get_text("audio_speed")].set(self.app.setting.narration_voice_speed)

    def create_video_settings(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=3, column=0, padx=0, pady=(0, 10), sticky="ew")

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
            frame, width=100,
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
        self.video_settings_vars[self.app.get_text("video_size")].set(
            f'{self.app.setting.video_width}x{self.app.setting.video_height}')
        self.video_settings_vars[self.app.get_text("video_fps")].set(self.app.setting.video_fps)
        self.video_settings_vars[self.app.get_text("video_threads")].set(self.app.setting.video_processing_threads)

    def create_subtitle_settings(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=4, column=0, padx=0, pady=(0, 10), sticky="ew")

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
        self.subtitle_settings_vars[self.app.get_text("font_color")].set(
            self.app.get_text(self.app.setting.subtitle_color))
        self.subtitle_settings_vars[self.app.get_text("border_color")].set(
            self.app.get_text(self.app.setting.subtitle_stroke_color))
        self.subtitle_settings_vars[self.app.get_text("border_width")].set(self.app.setting.subtitle_stroke_width)

    def create_save_button(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=5, column=0, padx=0, pady=(0, 10), sticky="ew")
        self.save_button = ctk.CTkButton(frame, text=self.app.get_text("save_settings"), command=self.save_settings)
        self.save_button.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

    def save_settings(self):
        if self.cache_path_var.get():
            self.app.setting.temp_dir = self.cache_path_var.get()
            logger.info(f"Updated cache path: {self.app.setting.temp_dir}")
        else:
            logger.warning(self.app.get_text("path_invalid"))
        self.update_tts_settings()
        # self.update_audio_settings()
        self.update_video_settings()
        self.update_subtitle_settings()
        messagebox.showinfo("Success", "Settings saved successfully!")
        logger.info(f"Settings saved successfully!")

    def update_tts_settings(self):
        tts_voice_type = tts_voice_rate = None
        tts_service_provider = self.tts_providers_var.get()
        self.app.setting.tts_service_provider = tts_service_provider
        logger.info(f"Updated TTS service provider: {tts_service_provider}")
        if tts_service_provider == "pyttsx3":
            audio_language = self.tts_settings_vars[self.app.get_text("audio_language")].get()
            self.app.setting.audio_language = self.app.text_to_key(audio_language)
            logger.info(f"Updated audio language: {audio_language}")
        if tts_service_provider == "azure":
            tts_voice_type = self.tts_settings_vars[self.app.get_text("tts_voice_type")].get()
            tts_speech_region = self.tts_settings_vars[self.app.get_text("tts_speech_region")].get()
            tts_api_key = self.api_key_var.get()
            self.app.setting.tts_api_key = tts_api_key
            self.app.setting.tts_voice_type = tts_voice_type
            self.app.setting.tts_voice_name = tts_voice_type.split(' ')[0]
            self.app.setting.tts_speech_region = tts_speech_region
            logger.info(f"Updated Azure settings - API Key: {tts_api_key}, Speech Region: {tts_speech_region}, "
                        f"Voice Type: {tts_voice_type}")
        if tts_service_provider == "edge-tts":
            tts_voice_rate = f'{int(self.rate_slider.get() * 100):+d}%'
            self.app.setting.tts_voice_rate = tts_voice_rate
        if tts_voice_type is not None and tts_voice_type != self.app.setting.tts_voice_type \
                or tts_voice_rate is not None and tts_voice_rate != self.app.setting.tts_voice_rate:
            self.app.clear_audio_cache()
        self.app.tts = self.app.load_tts(self.app.setting.tts_service_provider)

    # def update_audio_settings(self):
        # Gets the currently selected value for each ComboBox by variable
        # audio_language = self.audio_settings_vars[self.app.get_text("audio_language")].get()
        # audio_voice_type = self.audio_settings_vars[self.app.get_text("audio_voice_type")].get()
        # audio_speed = float(self.audio_settings_vars[self.app.get_text("audio_speed")].get().split("x")[0])

        # update the app setting
        # self.app.setting.audio_language = self.app.text_to_key(audio_language)
        # self.app.setting.audio_voice_type = audio_voice_type
        # self.app.setting.audio_speed = audio_speed

        # logger.info(
        #     f"Updated audio settings - Language: {audio_language}, "
        # f"Voice Type: {audio_voice_type}, Speed: {audio_speed}")

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
        self.app.setting.subtitle_font = subtitle_font
        self.app.setting.subtitle_font_path = sd.subtitle_font_dict[subtitle_font]
        self.app.setting.subtitle_font_size = int(subtitle_font_size)
        self.app.setting.subtitle_color = self.app.text_to_key(subtitle_font_color)
        self.app.setting.subtitle_stroke_color = self.app.text_to_key(subtitle_border_color)
        self.app.setting.subtitle_stroke_width = int(subtitle_border_width)
        logger.info(f"Updated subtitle settings - Font: {subtitle_font}, "
                    f"Font Path: {self.app.setting.subtitle_font_path}, Font Size: {subtitle_font_size}, "
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

    # 定义进度条更新函数
    def update_progress(self, value):
        value = float(value)
        # 计算进度百分比
        percentage = int(value * 100)
        self.voice_rate.configure(text=f"{percentage:+d}%")  # 显示 + 或 -

    # 定义复位函数
    def reset_progress(self):
        self.rate_slider.set(0)  # 将滑动条值重置为 0
        self.voice_rate.configure(text="0%")  # 更新标签文本

    def update_language(self):
        self.title.configure(text=self.app.get_text("export_settings"))
        # self.cache_label.configure(text=self.app.get_text("cache_path"))
        # self.path_label.configure(text=self.app.get_text("export_path"))
        # self.browse_btn.configure(text=self.app.get_text("browse"))
        # self.browse_button.configure(text=self.app.get_text("browse"))
        # self.reset_button.configure(text=self.app.get_text("reset"))
        self.create_cache_path()
        self.create_tts_settings()
        # self.create_audio_settings()
        self.create_video_settings()
        self.create_subtitle_settings()
        self.create_save_button()

    def refresh(self):
        if self.export_path_var.get() == "" and self.app.setting.video_path:
            self.export_path_var.set(self.app.setting.video_path)
