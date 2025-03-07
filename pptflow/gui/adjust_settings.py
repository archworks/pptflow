# Author: Valley-e
# Date: 2025/1/14  
# Description:
import os
import re
import webbrowser

import customtkinter as ctk
from .custom_tooltip import CustomTooltip
from tkinter import filedialog, messagebox
from pptflow.utils import mylogger, setting_dic as sd

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
        self.grid_rowconfigure(0, weight=1)

        self.font_size = 12
        self.font = ctk.CTkFont(size=self.font_size, weight="normal")
        self.help_image = self.app.load_ctk_image(os.path.join(self.app.icon_dir, "question-red.png"), 15)



        # Create scrollable frame for settings
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable_frame.grid(row=0, column=0, padx=70, pady=(30, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Create a dict for audio/video/subtitle settings
        self.api_key_help = None
        self.export_path_var = ctk.StringVar()
        self.tts_providers_var = ctk.StringVar()
        self.language_settings_var = ctk.StringVar()
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
        self.tts_providers_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        providers = sd.tts_service_providers.get(self.app.setting.language, ["kokoro", "baidu", "azure"])
        self.tts_providers_var.set(providers[0])
        self.tts_providers = ctk.CTkComboBox(frame, values=providers, state="readonly",
                                             variable=self.tts_providers_var, font=self.font)
        self.tts_providers.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.language_setting_label = ctk.CTkLabel(
            frame,
            text=self.app.get_text("audio_language"), font=self.font
        )
        self.language_setting_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.language_settings_var.set(self.app.get_text(self.app.setting.language))
        self.language_settings = ctk.CTkComboBox(frame, values=[self.app.get_text(s) for s in sd.audio_languages], state="readonly",
                                                 variable=self.language_settings_var, font=self.font)
        self.language_settings.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        # 绑定选择变化的事件
        self.tts_providers_var.trace("w", lambda *args: self.on_tts_provider_change(frame))
        # 初始化加载当前选项的设置
        self.on_tts_provider_change(frame)

    def on_tts_provider_change(self, frame):
        # 清除之前的组件（如果需要）
        for widget in frame.winfo_children():
            if widget not in {self.tts_providers_label, self.tts_providers,
                              self.language_setting_label, self.language_settings}:
                widget.destroy()

        # 根据选择的 TTS 提供商加载相应的设置 frame
        logger.info(f"Selected TTS Provider: {self.tts_providers_var.get()}")
        if self.tts_providers_var.get() == "kokoro":
            self.create_kokoro_settings(frame)
        elif self.tts_providers_var.get() == "azure":
            self.create_azure_settings(frame)
        elif self.tts_providers_var.get() == "baidu":
            self.create_baidu_settings(frame)

    def create_kokoro_settings(self, frame):
        self.app.load_tts(self.tts_providers_var.get())
        tts_settings = {
            self.app.get_text("audio_voice_name"): [self.app.get_text(s) for s in sd.kokoro_voice_type],
        }
        create_combo_box(frame, 2, tts_settings, self.tts_settings_vars)
        self.tts_settings_vars[self.app.get_text("audio_voice_name")].set(self.app.setting.kokoro_voice_name)

    def create_baidu_settings(self, frame):
        # baidu api
        baidu_api_frame = ctk.CTkFrame(frame, fg_color="transparent")
        baidu_api_frame.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        # 新增实例变量用于存储真实值
        self._app_id_var_real = self.app.setting.baidu_app_id
        self._baidu_api_key_real = self.app.setting.baidu_api_key
        self._baidu_secret_key_real = self.app.setting.baidu_secret_key
        self.app_id_label = ctk.CTkLabel(baidu_api_frame, text='App ID:', font=self.font)
        self.app_id_label.grid(row=0, column=0, sticky="w")

        self.app_id_help_label = ctk.CTkLabel(baidu_api_frame,
                                              image=self.help_image,
                                              text="", text_color="red",
                                              fg_color="transparent", font=self.font)
        self.app_id_help_label.grid(row=0, column=1, padx=5, sticky="w")
        self.app_id_help_tip = CustomTooltip(self.app_id_help_label,
                                             self.app.get_text("tts_api_key_help"), delay=10)
        self.app_id_help_label.bind("<Button-1>", lambda event: self.get_api_key_help(event))

        self.app_id_var = ctk.StringVar(value="******" if self._app_id_var_real else "")
        self.app_id = ctk.CTkEntry(frame, width=140, textvariable=self.app_id_var,
                                   font=self.font, show="*")
        self.app_id.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.baidu_api_key_label = ctk.CTkLabel(frame, text='API Key:', font=self.font)
        self.baidu_api_key_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.baidu_api_key_var = ctk.StringVar(value="******" if self._baidu_api_key_real else "")
        self.baidu_api_key = ctk.CTkEntry(frame, width=140, textvariable=self.baidu_api_key_var,
                                          font=self.font, show="*")
        self.baidu_api_key.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.baidu_secret_key_label = ctk.CTkLabel(frame, text='Secret Key:', font=self.font)
        self.baidu_secret_key_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.baidu_secret_key_var = ctk.StringVar(value="******" if self._baidu_secret_key_real else "")
        self.baidu_secret_key = ctk.CTkEntry(frame, width=140, textvariable=self.baidu_secret_key_var,
                                             font=self.font, show="*")
        self.baidu_secret_key.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        tts_settings = {
            self.app.get_text("baidu_tts_per"): [value for key, value in sd.baidu_voice_persons.items()],
        }
        create_combo_box(frame, 3, tts_settings, self.tts_settings_vars)
        self.tts_settings_vars[self.app.get_text("baidu_tts_per")].set(sd.baidu_voice_persons.get(self.app.setting.baidu_tts_per))

    def create_azure_settings(self, frame):
        # api key
        self.app.load_tts(self.tts_providers_var.get())
        api_key_frame = ctk.CTkFrame(frame, fg_color="transparent")
        api_key_frame.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.api_key_label = ctk.CTkLabel(api_key_frame, text=self.app.get_text("tts_api_key"), font=self.font)
        self.api_key_label.grid(row=0, column=0, sticky="w")
        self.api_key_help_label = ctk.CTkLabel(api_key_frame, image=self.help_image,
                                               text="", text_color="red",
                                               fg_color="transparent", font=self.font)
        self.api_key_help_label.grid(row=0, column=1, padx=5, sticky="w")
        self.api_key_help = CustomTooltip(self.api_key_help_label,
                                          self.app.get_text("tts_api_key_help"), delay=10)
        self.api_key_help_label.bind("<Button-1>", lambda event: self.get_api_key_help(event))
        self._api_key_real = self.app.setting.tts_api_key
        self.api_key_var = ctk.StringVar(value="******" if self._api_key_real else "")
        self.api_key = ctk.CTkEntry(frame, width=140, textvariable=self.api_key_var,
                                    font=self.font, show="*")
        self.api_key.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        tts_settings = {
            self.app.get_text("tts_speech_region"): sd.tts_speech_regions,
            self.app.get_text("tts_voice_type"): sd.tts_speech_voices,
        }
        create_combo_box(frame, 3, tts_settings, self.tts_settings_vars)
        self.tts_settings_vars[self.app.get_text("tts_speech_region")].set(self.app.setting.tts_speech_region)
        self.tts_settings_vars[self.app.get_text("tts_voice_type")].set(self.app.setting.tts_voice_type)

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
                from pptflow.utils import font
                self.utils_font = font
                if not self.app.setting.subtitle_font_path:
                    self.app.setting.subtitle_font_path = self.utils_font.find_font_path(self.app.setting.subtitle_font_name)
                sd.subtitle_font_dict = self.utils_font.get_or_load_fonts()
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
        if not self.validate_settings():  # 先执行校验
            return
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
        language = self.app.text_to_key(self.language_settings_var.get())
        if tts_service_provider != self.app.setting.tts_service_provider \
                or language != self.app.setting.language:
            self.app.clear_audio_cache()
        self.app.setting.tts_service_provider = tts_service_provider
        self.app.setting.language = language
        logger.info(f"Updated TTS service provider: {tts_service_provider}, Audio Language: {language}")
        if tts_service_provider == "kokoro":
            audio_voice_name = self.tts_settings_vars[self.app.get_text("audio_voice_name")].get()
            if audio_voice_name != self.app.setting.kokoro_voice_name:
                self.app.clear_audio_cache()
            self.app.setting.kokoro_voice_name = audio_voice_name
            logger.info(f"Updated Kokoro settings - Voice Name: {audio_voice_name}")
        if tts_service_provider == "baidu":
            app_id = self.app_id_var.get() if self.app_id_var.get() != "******" else self._app_id_var_real
            api_key = self.baidu_api_key_var.get() if \
                self.baidu_api_key_var.get() != "******" else self._baidu_api_key_real
            secret_key = self.baidu_secret_key_var.get() if \
                self.baidu_secret_key_var.get() != "******" else self._baidu_secret_key_real
            self.app.setting.baidu_app_id = app_id
            self.app.setting.baidu_api_key = api_key
            self.app.setting.baidu_secret_key = secret_key
            tts_voice_per = self.tts_settings_vars[self.app.get_text("baidu_tts_per")].get()
            tts_voice_per = get_key_by_value(sd.baidu_voice_persons, tts_voice_per)
            if tts_voice_per != self.app.setting.baidu_tts_per:
                self.app.clear_audio_cache()
            self.app.setting.baidu_tts_per = tts_voice_per
            logger.info(f"Updated Baidu settings - App ID: {self.app_id_var.get()}, "
                        f"API Key: {self.baidu_api_key_var.get()}, "
                        f"Secret Key: {self.baidu_secret_key_var.get()}, "
                        f"TTS Voice Person: {self.tts_settings_vars[self.app.get_text('baidu_tts_per')].get()}")
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
            len(sd.subtitle_font_dict) > 0 else self.utils_font.get_or_load_fonts()[subtitle_font]
        self.app.setting.subtitle_font_size = int(subtitle_font_size)
        self.app.setting.subtitle_color = self.app.text_to_key(subtitle_font_color)
        self.app.setting.subtitle_length = int(subtitle_length)
        self.app.setting.subtitle_stroke_color = self.app.text_to_key(subtitle_border_color)
        self.app.setting.subtitle_stroke_width = int(subtitle_border_width)
        logger.info(f"Updated subtitle settings - Font: {subtitle_font}, "
                    f"Font Path: {self.app.setting.subtitle_font_path}, Font Size: {subtitle_font_size}, "
                    f"Font Color: {subtitle_font_color}, Subtitle Length: {subtitle_length}, "
                    f"Border Color: {subtitle_border_color}, Border Width: {subtitle_border_width}")

    def validate_settings(self):
        """校验配置是否完整"""
        errors = []

        # 校验音频设置
        if self.is_audio_settings_visible:
            if self.tts_providers_var.get() == "azure":
                if not self.api_key_var.get().strip():
                    errors.append(self.app.get_text("tts_api_key"))
                if not self.tts_settings_vars[self.app.get_text("tts_speech_region")].get():
                    errors.append(self.app.get_text("tts_speech_region"))
                if not self.tts_settings_vars[self.app.get_text("tts_voice_type")].get():
                    errors.append(self.app.get_text("tts_voice_type"))
            elif self.tts_providers_var.get() == "kokoro":
                if not self.tts_settings_vars[self.app.get_text("audio_voice_name")].get():
                    errors.append(self.app.get_text("audio_voice_name"))
            elif self.tts_providers_var.get() == "baidu":
                if not self.app_id_var.get().strip():
                    errors.append(self.app.get_text("app_id"))
                if not self.baidu_api_key_var.get().strip():
                    errors.append(self.app.get_text("baidu_api_key"))
                if not self.baidu_secret_key_var.get().strip():
                    errors.append(self.app.get_text("baidu_secret_key"))

        # 校验视频设置
        if self.is_video_settings_visible:
            if not self.export_path_var.get().strip():
                errors.append(self.app.get_text("export_path"))
            if not self.video_settings_vars[self.app.get_text("video_format")].get():
                errors.append(self.app.get_text("video_format"))
            if not self.video_settings_vars[self.app.get_text("video_size")].get():
                errors.append(self.app.get_text("video_size"))

        # 校验字幕设置
        if self.is_subtitle_settings_visible:
            required_fields = [
                self.app.get_text("font_type"),
                self.app.get_text("font_size"),
                self.app.get_text("font_color")
            ]
            for field in required_fields:
                if not self.subtitle_settings_vars[field].get():
                    errors.append(field)

        # 处理校验结果
        if errors:
            error_msg = self.app.get_text("required_fields_missing") + ":\n- " + "\n- ".join(errors)
            messagebox.showerror(self.app.get_text("validation_error"), error_msg)
            return False
        return True

    def browse_export_path(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4")]
        )
        if path:
            self.export_path_var.set(path)

    def get_api_key_help(self, event):
        api_key_help_url = "https://pptflow.com/en/blog/set-up-azure-tts"
        if self.tts_providers_var.get() == "azure":
            api_key_help_url = "https://pptflow.com/en/blog/set-up-azure-tts"
        elif self.tts_providers_var.get() == "baidu":
            api_key_help_url = "https://pptflow.com/en/blog/set-up-azure-tts"
        webbrowser.open(api_key_help_url)

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


def get_key_by_value(dictionary, target_value):
    """根据value反向查找字典中的key"""
    for key, value in dictionary.items():
        if value == target_value:
            return key
    logger.error(f"未找到对应value的key: {target_value}")
    return None  # 未找到时返回None
