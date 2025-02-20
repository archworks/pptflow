# Author: Valley-e
# Date: 2025/1/14  
# Description:
import os
import re
import webbrowser

import customtkinter as ctk
from .custom_tooltip import CustomTooltip
from tkinter import filedialog, messagebox
from pptflow.utils import mylogger, font, setting_dic as sd

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)


def create_combo_box(parent, index, options, variable, command=None):
    for i, (key, values) in enumerate(options.items()):
        label = ctk.CTkLabel(parent, text=f"{key}:", font=ctk.CTkFont(size=12, weight="normal"))
        label.grid(row=index + i + 1, column=0, padx=5, pady=5, sticky="w")

        # Create a StringVar variable for each ComboBox
        var = ctk.StringVar(value=values[0])
        variable[key] = var

        combo = ctk.CTkComboBox(parent, values=values, variable=var,
                                font=ctk.CTkFont(size=12, weight="normal"),
                                state="readonly")
        combo.grid(row=index + i + 1, column=1, padx=5, pady=5, sticky="w")


class AdjustSettingsFrame(ctk.CTkFrame):
    def __init__(self, app, frame):
        super().__init__(frame, fg_color="white")
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(0, weight=1)

        self.font_size = 12
        self.font = ctk.CTkFont(size=self.font_size, weight="normal")

        # Create scrollable frame for settings
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable_frame.grid(row=0, column=0, padx=70, pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Create a dict for audio/video/subtitle settings
        self.api_key_help = None
        self.export_path_var = ctk.StringVar()
        self.tts_providers_var = ctk.StringVar()
        self.tts_settings_vars = {}
        self.audio_settings_vars = {}
        self.video_settings_vars = {}
        self.subtitle_settings_vars = {}

        # Add settings sections
        self.create_audio_settings()
        self.create_video_settings()
        self.create_subtitle_settings()
        self.create_save_cancel_button()

    def create_tts_settings(self, frame):
        self.tts_providers_label = ctk.CTkLabel(
            frame,
            text=self.app.get_text("tts_service_provider"), font=self.font
        )
        self.tts_providers_label.grid(row=1, column=0, padx=5, pady=10, sticky="w")
        self.tts_providers_var.set(self.app.setting.tts_service_provider)
        self.tts_providers = ctk.CTkComboBox(frame, values=sd.tts_service_providers, state="readonly",
                                             variable=self.tts_providers_var, font=self.font)
        self.tts_providers.grid(row=1, column=1, padx=5, pady=10, sticky="w")
        # 绑定选择变化的事件
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
            self.app.setting.tts_speech_region = os.getenv("TTS_AZURE_SPEECH_REGION") if \
                self.app.setting.tts_speech_region is None else self.app.setting.tts_speech_region
            self.app.setting.tts_azure_api_key = os.getenv("TTS_AZURE_SPEECH_KEY") if \
                self.app.setting.tts_azure_api_key is None else self.app.setting.tts_azure_api_key

            self.create_azure_settings(frame)

    def create_pyttsx3_settings(self, frame):
        tts_settings = {
            self.app.get_text("audio_language"): [self.app.get_text(s) for s in sd.audio_languages]
        }
        create_combo_box(frame, 1, tts_settings, self.tts_settings_vars)
        self.tts_settings_vars[self.app.get_text("audio_language")].set(
            self.app.get_text(self.app.text_to_key(self.app.setting.language)))

    def create_azure_settings(self, frame):
        tts_settings = {
            self.app.get_text("audio_language"): [self.app.get_text(s) for s in sd.audio_languages],
            self.app.get_text("tts_speech_region"): sd.tts_speech_regions,
            self.app.get_text("tts_voice_type"): sd.tts_speech_voices,
        }
        create_combo_box(frame, 1, tts_settings, self.tts_settings_vars)
        self.tts_settings_vars[self.app.get_text("tts_speech_region")].set(self.app.setting.tts_speech_region)
        self.tts_settings_vars[self.app.get_text("tts_voice_type")].set(self.app.setting.tts_voice_type)
        # api key
        api_key_frame = ctk.CTkFrame(frame, fg_color="transparent")
        api_key_frame.grid(row=2 + len(tts_settings), column=0, padx=5, pady=10, sticky="w")
        self.api_key_label = ctk.CTkLabel(api_key_frame, text=self.app.get_text("tts_api_key"), font=self.font)
        self.api_key_label.grid(row=2 + len(tts_settings), column=0, sticky="w")
        self.api_key_help_label = ctk.CTkLabel(api_key_frame, text="?", text_color="red",
                                               fg_color="transparent", font=self.font)
        self.api_key_help_label.grid(row=2 + len(tts_settings), column=1, padx=5, sticky="w")
        self.api_key_help = CustomTooltip(self.api_key_help_label,
                                          self.app.get_text("tts_api_key_help"), delay=10)
        self.api_key_help_label.bind("<Button-1>", lambda event: self.get_api_key_help(event))
        self.api_key_var = ctk.StringVar(value=self.app.setting.tts_azure_api_key)
        self.api_key = ctk.CTkEntry(frame, width=140, textvariable=self.api_key_var, font=self.font)
        self.api_key.grid(row=2 + len(tts_settings), column=1, padx=5, pady=10, sticky="w")

    def create_edge_tts_settings(self, frame):
        # tts voice rate
        self.rate_slider_label = ctk.CTkLabel(frame, text=self.app.get_text("tts_voice_rate"),
                                              fg_color="transparent", font=self.font)
        self.rate_slider_label.grid(row=2, column=0, padx=5, pady=10, sticky="w")
        # 创建滑动条
        self.rate_slider = ctk.CTkSlider(frame, from_=-1, to=1, orientation="horizontal", command=self.update_progress)
        self.rate_slider.grid(row=2, column=1, padx=5, pady=10, sticky="w")
        self.rate_slider.set(0)  # 初始滑动条值设置为 0（中间）
        # 创建显示进度的标签
        self.voice_rate = ctk.CTkLabel(frame, text="0%", font=self.font)
        self.voice_rate.grid(row=2, column=2, padx=5, pady=10, sticky="w")

        # 创建复位按钮
        self.reset_button = ctk.CTkButton(frame, width=100, text=self.app.get_text("reset"), font=self.font,
                                          command=self.reset_progress)
        self.reset_button.grid(row=2, column=3, padx=5, pady=10)

    def create_audio_settings(self):
        frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        frame.grid(row=2, column=0, padx=60, pady=(0, 10), sticky="nsew")

        self.audio_settings_frame = None  # 添加一个实例变量来存储设置面板的frame
        self.is_audio_settings_visible = False  # 添加一个状态变量来跟踪设置面板的可见性

        self.audio_settings_button = ctk.CTkButton(
            frame, image=self.app.load_ctk_image(os.path.join(self.app.icon_dir, "down-arrow.png"), 20),
            text=self.app.get_text("audio_settings"), font=self.font, width=250,
            bg_color="transparent", fg_color="#2563EB", hover_color="#1D4ED8",
            command=lambda: self.toggle_audio_settings(frame)
        )
        self.audio_settings_button.grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.toggle_audio_settings(frame)

    def toggle_audio_settings(self, frame):
        if self.is_audio_settings_visible:
            # 如果设置面板是可见的，则隐藏它
            self.audio_settings_frame.grid_remove()
            self.is_audio_settings_visible = False
            self.audio_settings_button.configure(
                image=self.app.load_ctk_image(os.path.join(self.app.icon_dir, "down-arrow.png"), 20)
            )
        else:
            if self.audio_settings_frame is None:
                self.audio_settings_frame = ctk.CTkFrame(frame, fg_color="transparent")
                self.audio_settings_frame.grid(row=1, column=0, pady=(0, 10), sticky="ew")
                self.audio_settings_button.configure(
                    image=self.app.load_ctk_image(os.path.join(self.app.icon_dir, "up-arrow.png"), 20))
                self.create_tts_settings(self.audio_settings_frame)
            self.audio_settings_frame.grid()
            self.is_audio_settings_visible = True

    def create_video_settings(self):
        frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        frame.grid(row=3, column=0, padx=60, pady=(0, 10), sticky="nsew")

        self.video_settings_frame = None  # 添加一个实例变量来存储设置面板的frame
        self.is_video_settings_visible = False  # 添加一个状态变量来跟踪设置面板的可见性

        self.video_settings_button = ctk.CTkButton(
            frame, image=self.app.load_ctk_image(os.path.join(self.app.icon_dir, "down-arrow.png"), 20),
            text=self.app.get_text("video_settings"), font=self.font, width=250,
            bg_color="transparent", fg_color="#2563EB", hover_color="#1D4ED8",
            command=lambda: self.toggle_video_settings(frame)
        )
        self.video_settings_button.grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.toggle_video_settings(frame)

    def toggle_video_settings(self, frame):
        if self.is_video_settings_visible:
            # 如果设置面板是可见的，则隐藏它
            self.video_settings_frame.grid_remove()
            self.is_video_settings_visible = False
            self.video_settings_button.configure(
                image=self.app.load_ctk_image(os.path.join(self.app.icon_dir, "down-arrow.png"), 20))
        else:
            # 如果设置面板是隐藏的，则显示它
            if self.video_settings_frame is None:
                self.video_settings_frame = ctk.CTkFrame(frame, fg_color="transparent")
                self.video_settings_frame.grid(row=1, column=0, pady=(0, 10), sticky="ew")
                self.video_settings_button.configure(
                    image=self.app.load_ctk_image(os.path.join(self.app.icon_dir, "up-arrow.png"), 20))
                # Export path
                self.path_label = ctk.CTkLabel(self.video_settings_frame, font=self.font,
                                               text=self.app.get_text("export_path"))
                self.path_label.grid(row=1, column=0, padx=5, pady=10, sticky="w")

                self.export_path = ctk.CTkEntry(self.video_settings_frame, width=140,
                                                textvariable=self.export_path_var, font=self.font)
                self.export_path.grid(row=1, column=1, padx=5, pady=10, sticky="w")

                self.browse_btn = ctk.CTkButton(
                    self.video_settings_frame, width=40, fg_color="#2563EB", text_color="white",
                    text=self.app.get_text("browse"), font=self.font, hover_color="#1D4ED8",
                    command=self.browse_export_path
                )
                self.browse_btn.grid(row=1, column=2, padx=0, pady=10)

                self.video_settings = {
                    self.app.get_text("video_format"): sd.video_formats,
                    self.app.get_text("video_size"): sd.video_sizes,
                    self.app.get_text("video_fps"): sd.video_fps,
                    self.app.get_text("video_threads"): sd.video_processing_threads
                }
                create_combo_box(self.video_settings_frame, 1, self.video_settings, self.video_settings_vars)
                self.video_settings_vars[self.app.get_text("video_format")].set(self.app.setting.video_format)
                self.video_settings_vars[self.app.get_text("video_size")].set(
                    f'{self.app.setting.video_width}x{self.app.setting.video_height}')
                self.video_settings_vars[self.app.get_text("video_fps")].set(self.app.setting.video_fps)
                self.video_settings_vars[self.app.get_text("video_threads")].set(
                    self.app.setting.video_processing_threads)
                self.video_settings_vars[self.app.get_text("video_format")] \
                    .trace("w", lambda *args: self.on_video_format_change())
                # 初始化加载当前选项的设置
                self.on_video_format_change()

            self.video_settings_frame.grid()
            self.is_video_settings_visible = True

    def on_video_format_change(self):
        logger.info(f'video_format: {self.video_settings_vars[self.app.get_text("video_format")].get()}')
        if self.app.file_display:
            self.app.setting.video_path = re.sub(
                r"pptx?$", self.video_settings_vars[self.app.get_text("video_format")].get().lower(),
                self.app.file_display)
            self.export_path_var.set(self.app.setting.video_path)

    def create_subtitle_settings(self):
        frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        frame.grid(row=4, column=0, padx=60, pady=(0, 10), sticky="nsew")

        self.subtitle_settings_frame = None  # 添加一个实例变量来存储设置面板的frame
        self.is_subtitle_settings_visible = False  # 添加一个状态变量来跟踪设置面板的可见性

        self.subtitle_settings_button = ctk.CTkButton(
            frame, image=self.app.load_ctk_image(os.path.join(self.app.icon_dir, "down-arrow.png"), 20),
            text=self.app.get_text("subtitle_settings"), font=self.font, width=250,
            bg_color="transparent", fg_color="#2563EB", hover_color="#1D4ED8",
            command=lambda: self.toggle_subtitle_settings(frame)
        )
        self.subtitle_settings_button.grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.toggle_subtitle_settings(frame)

    def toggle_subtitle_settings(self, frame):
        if self.is_subtitle_settings_visible:
            # 如果设置面板是可见的，则隐藏它
            self.subtitle_settings_frame.grid_remove()
            self.is_subtitle_settings_visible = False
            self.subtitle_settings_button.configure(
                image=self.app.load_ctk_image(os.path.join(self.app.icon_dir, "down-arrow.png"), 20))
        else:
            # 如果设置面板是隐藏的，则显示它
            if self.subtitle_settings_frame is None:
                self.subtitle_settings_frame = ctk.CTkFrame(frame, fg_color="transparent")
                self.subtitle_settings_frame.grid(row=1, column=0, pady=10, sticky="ew")
                self.subtitle_settings_button.configure(
                    image=self.app.load_ctk_image(os.path.join(self.app.icon_dir, "up-arrow.png"), 20))

                sd.subtitle_font_dict = font.get_or_load_fonts()
                self.subtitle_settings = {
                    self.app.get_text("font_type"): [key for key in sd.subtitle_font_dict],
                    self.app.get_text("font_size"): [str(i) for i in range(18, 49, 2)],
                    self.app.get_text("font_color"): [self.app.get_text(s) for s in sd.font_colors],
                    self.app.get_text("subtitle_length"): [self.app.get_text(s) for s in sd.subtitle_lengths],
                    self.app.get_text("border_color"): [self.app.get_text(s) for s in sd.border_colors],
                    self.app.get_text("border_width"): sd.border_widths
                }
                create_combo_box(self.subtitle_settings_frame, 0, self.subtitle_settings, self.subtitle_settings_vars)
                self.subtitle_settings_vars[self.app.get_text("font_type")].set(self.app.setting.subtitle_font_name)
                self.subtitle_settings_vars[self.app.get_text("font_size")].set(self.app.setting.subtitle_font_size)
                self.subtitle_settings_vars[self.app.get_text("font_color")].set(
                    self.app.get_text(self.app.setting.subtitle_color))
                self.subtitle_settings_vars[self.app.get_text("subtitle_length")].set(
                    self.app.get_text(self.app.setting.subtitle_length))
                self.subtitle_settings_vars[self.app.get_text("border_color")].set(
                    self.app.get_text(self.app.setting.subtitle_stroke_color))
                self.subtitle_settings_vars[self.app.get_text("border_width")].set(
                    self.app.setting.subtitle_stroke_width)

            self.subtitle_settings_frame.grid()
            self.is_subtitle_settings_visible = True

    def create_save_cancel_button(self):
        frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        frame.grid(row=5, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        self.save_button = ctk.CTkButton(frame, text=self.app.get_text("save_settings"),
                                         font=self.font, width=120,
                                         fg_color="#2563EB", hover_color="#1D4ED8", text_color="white",
                                         command=self.save_settings)
        self.save_button.grid(row=0, column=0, padx=(10, 50), pady=10, sticky="ew")
        self.cancel_button = ctk.CTkButton(frame, text=self.app.get_text("cancel_settings"), font=self.font,
                                           fg_color="gray70", hover_color="gray", text_color='white', width=120,
                                           command=self.cancel_settings)
        self.cancel_button.grid(row=0, column=1, padx=(0, 50), pady=10, sticky="ew")

    def save_settings(self):
        if self.is_audio_settings_visible:
            self.update_tts_settings()
        if self.is_video_settings_visible:
            self.update_video_settings()
        if self.is_subtitle_settings_visible:
            self.update_subtitle_settings()
        messagebox.showinfo("Success", "Settings saved successfully!")
        self.app.step += 1
        self.app.setting_flow_1(1)
        self.app.cancel_settings.grid()
        self.app.generation_flow_2(2)
        self.cancel_settings()
        self.grab_release()
        logger.info(f"Settings saved successfully!")

    def cancel_settings(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.app.adjust_settings.grid_remove()
        self.app.flow_frame.grid()
        self.app.flow_frame.tkraise()
        self.grab_release()

    def update_tts_settings(self):
        tts_service_provider = self.tts_providers_var.get()
        if tts_service_provider != self.app.setting.tts_service_provider:
            self.app.clear_audio_cache()
        self.app.setting.tts_service_provider = tts_service_provider
        logger.info(f"Updated TTS service provider: {tts_service_provider}")
        if tts_service_provider == "pyttsx3":
            audio_language = self.tts_settings_vars[self.app.get_text("audio_language")].get()
            if audio_language != self.app.setting.language:
                self.app.clear_audio_cache()
            self.app.setting.language = self.app.text_to_key(audio_language)
            logger.info(f"Updated audio language: {audio_language}")
        if tts_service_provider == "azure":
            tts_voice_type = self.tts_settings_vars[self.app.get_text("tts_voice_type")].get()
            tts_speech_region = self.tts_settings_vars[self.app.get_text("tts_speech_region")].get()
            tts_api_key = self.api_key_var.get()
            if tts_voice_type != self.app.setting.tts_voice_type:
                self.app.clear_audio_cache()
            self.app.setting.tts_api_key = tts_api_key
            self.app.setting.tts_voice_type = tts_voice_type
            self.app.setting.tts_voice_name = tts_voice_type.split(' ')[0]
            self.app.setting.tts_speech_region = tts_speech_region
            logger.info(f"Updated Azure settings - API Key: {tts_api_key}, Speech Region: {tts_speech_region}, "
                        f"Voice Type: {tts_voice_type}")
        if tts_service_provider == "edge-tts":
            tts_voice_rate = f'{int(self.rate_slider.get() * 100):+d}%'
            if tts_voice_rate != self.app.setting.tts_voice_rate:
                self.app.clear_audio_cache()
            self.app.setting.tts_voice_rate = tts_voice_rate
        self.app.tts = self.app.load_tts(self.app.setting.tts_service_provider)

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
        subtitle_length = self.subtitle_settings_vars[self.app.get_text("subtitle_length")].get()
        subtitle_border_color = self.subtitle_settings_vars[self.app.get_text("border_color")].get().lower()
        subtitle_border_width = self.subtitle_settings_vars[self.app.get_text("border_width")].get()
        self.app.setting.subtitle_font_path = sd.subtitle_font_dict[subtitle_font] if \
            len(sd.subtitle_font_dict) > 0 else font.get_or_load_fonts()[subtitle_font]
        self.app.setting.subtitle_font_size = int(subtitle_font_size)
        self.app.setting.subtitle_color = self.app.text_to_key(subtitle_font_color)
        self.app.setting.subtitle_length = int(subtitle_length)
        self.app.setting.subtitle_stroke_color = self.app.text_to_key(subtitle_border_color)
        self.app.setting.subtitle_stroke_width = int(subtitle_border_width)
        logger.info(f"Updated subtitle settings - Font: {subtitle_font}, "
                    f"Font Path: {self.app.setting.subtitle_font_path}, Font Size: {subtitle_font_size}, "
                    f"Font Color: {subtitle_font_color}, Subtitle Length: {subtitle_length}, "
                    f"Border Color: {subtitle_border_color}, Border Width: {subtitle_border_width}")

    def browse_export_path(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4")]
        )
        if path:
            self.export_path_var.set(path)

    def get_api_key_help(self, event):
        api_key_help_url = "https://pptflow.com/en/blog/set-up-azure-tts"
        webbrowser.open(api_key_help_url)

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
        self.create_audio_settings()
        self.create_video_settings()
        self.create_subtitle_settings()
        self.create_save_cancel_button()
        self.api_key_help = CustomTooltip(self.api_key_help_label,
                                          self.app.get_text("tts_api_key_help"))

    def refresh(self):
        if self.export_path_var.get() == "" and self.app.setting.video_path:
            self.export_path_var.set(self.app.setting.video_path)
