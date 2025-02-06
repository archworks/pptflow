# Author: Valley-e
# Date: 2025/1/11  
# Description:
import json
import os
import platform
import shutil
import sys
import re
import threading
import webbrowser
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
from pptx import Presentation
from .custom_tooltip import CustomTooltip
from pptflow import ppt2video
from pptflow.config.setting import Setting
from pptflow.utils import mylogger, font, setting_dic as sd
from pptflow.utils.progress_tracker import ProgressTracker

# 初始化 CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
logger = mylogger.get_logger(__name__)


class PPTFlowApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # 初始化 Setting 和 TTS
        self.setting = Setting()
        self.tts = self.load_tts(self.setting.tts_service_provider)
        self.current_language = self.setting.language
        self.language_modes = get_locales_subdirectories() if len(
            get_locales_subdirectories()) > 0 else sd.language_mode
        self._translations_cache = {}  # Add translation cache
        self.translations = self.get_translation()

        self.step = 0
        self.icons = ["pptfile.png", "settings.png", "arrow.png", "play.png"]
        self.labels = ["Select PPT File", "Adjust Settings", "Generate Video", "Preview and Play"]
        self.completed_icons = ["pptfile_done.png", "settings_done.png", "arrow_done.png", "play_done.png"]
        # self.disabled_icons = ["pptfile_disabled.png", "settings_disabled.png", "arrow_disabled.png",
        #                        "play_disabled.png"]
        self.disabled_icons = ["pptfile.png", "settings.png", "arrow.png", "play.png"]
        # Get icon directory path
        self.icon_dir = resource_path(os.path.join("assets", "icons"))

        self.loading_title = self.get_text("generate_video")
        self.file_display = ""
        self.tooltip = None
        self.cancel_file = None
        self.select_button = None
        self.adjust_settings = None
        self.cancel_settings = None
        self.generate_button = None

        # Configure window
        self.title("PPTFlow")
        self.center_window()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)

        # Create main frame
        # self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # self.main_frame.grid(row=0, column=0, sticky="nsew")
        # self.main_frame.grid_columnconfigure(0, weight=1)
        # self.main_frame.grid_rowconfigure(0, weight=1)
        # self.main_frame.grid_rowconfigure(1, weight=3)
        # self.main_frame.grid_rowconfigure(2, weight=1)

        # 顶部标题和图标部分
        self.create_top_section()

        # 中间流程图布局
        self.create_workflow_section()

        # 底部进度条和进退按钮
        # self.create_bottom_section()

    def create_top_section(self):
        self.top_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, columnspan=7, sticky="nsew")
        self.top_frame.grid_columnconfigure(0, weight=7)
        # 标题部分
        title_frame = ctk.CTkFrame(self.top_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=(100, 0), pady=20)

        # 加粗的 PPT
        ppt_label = ctk.CTkLabel(title_frame, text="PPT", font=ctk.CTkFont(size=24, weight="bold"))
        ppt_label.grid(row=0, column=0)

        # 正常的 Flow
        flow_label = ctk.CTkLabel(title_frame, text="Flow", font=ctk.CTkFont(size=24, weight="normal"))
        flow_label.grid(row=0, column=1)
        # self.title_label = ctk.CTkLabel(self.top_frame, text="PPTFlow",
        #                                 font=ctk.CTkFont(size=24, weight="bold", slant="italic"))
        # self.title_label.grid(row=0, column=0, padx=(60, 0), pady=20, sticky="nsew")

        # 右上角的图标按钮（设置和GitHub）
        self.settings_button = ctk.CTkButton(self.top_frame, text="",
                                             image=self.load_ctk_image(os.path.join(self.icon_dir, "settings1.png"),
                                                                       size=20),
                                             width=20, height=20, fg_color="transparent",
                                             hover_color=("gray70", "gray30"),
                                             command=lambda: self.select_frame("System Settings"))
        self.github_button = ctk.CTkButton(self.top_frame, text="",
                                           image=self.load_ctk_image(os.path.join(self.icon_dir, "github.png"),
                                                                     size=20),
                                           width=20, height=20, fg_color="transparent",
                                           hover_color=("gray70", "gray30"),
                                           command=lambda: self.on_button_click("Github"))
        self.discord_button = ctk.CTkButton(self.top_frame, text="",
                                            image=self.load_ctk_image(os.path.join(self.icon_dir, "discord.png"),
                                                                      size=20),
                                            width=20, height=20, fg_color="transparent",
                                            hover_color=("gray70", "gray30"),
                                            command=lambda: self.on_button_click("Discord"))

        self.settings_button.grid(row=0, column=1, padx=0, pady=10, sticky="ne")
        self.github_button.grid(row=0, column=2, padx=0, pady=10, sticky="ne")
        self.discord_button.grid(row=0, column=3, padx=0, pady=10, sticky="ne")

    def create_workflow_section(self):
        self.flow_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.flow_frame.grid(row=1, column=0, columnspan=7, padx=100, sticky="nsew")
        for i in range(7):
            self.flow_frame.grid_columnconfigure(i, weight=1)
        # 流程图布局
        # row_offset = 1  # 从第1行开始布局

        self.select_flow_0(0)
        self.setting_flow_1(1)
        self.generation_flow_2(2)
        self.review_flow_3(3)

        for i, (icon, label_text) in enumerate(zip(self.icons, self.labels)):
            # 图标
            icon_image = self.load_ctk_image(icon, size=50)  # 调整图标大小
            icon_button = ctk.CTkButton(self.flow_frame, image=icon_image, text="", width=80, height=80,
                                        fg_color="transparent", hover_color="gray")
            icon_button.grid(row=1, column=i * 2, padx=5, pady=(20, 10))

            # 流程连接线
            if i < len(self.icons) - 1:
                line = ctk.CTkLabel(self.flow_frame, text="─" * 3, font=ctk.CTkFont(size=20), text_color="gray")
                line.grid(row=1, column=i * 2 + 1, pady=10)

    def select_flow_0(self, i, row_offset=1):
        # self.file_frame = ctk.CTkFrame(self.flow_frame)
        # self.file_frame.grid(row=row_offset + 1, column=i * 2)
        self.file_label_var = ctk.StringVar()
        self.file_label = ctk.CTkLabel(self.flow_frame, textvariable=self.file_label_var,
                                       font=ctk.CTkFont(size=12), width=100)
        self.file_label.grid(row=row_offset + 1, column=i * 2, padx=5, pady=5)

        self.cancel_file = ctk.CTkButton(self.flow_frame, text=self.get_text("cancel"),
                                         font=ctk.CTkFont(size=12), width=50,
                                         fg_color="transparent", hover_color="gray", text_color="#0d6efd",
                                         command=lambda: self.on_button_click("Cancel File"))
        self.cancel_file.grid(row=row_offset + 2, column=i * 2, padx=5, pady=0)
        self.file_label.grid_remove()
        self.cancel_file.grid_remove()

        self.select_button = ctk.CTkButton(self.flow_frame, text=self.get_text("select_ppt"),
                                           font=ctk.CTkFont(size=12), width=100,
                                           command=lambda: self.on_button_click("Select PPT File"))
        self.select_button.grid(row=row_offset + 1, column=i * 2, pady=5, padx=5)
        self.update_button(i, self.select_button)

    def setting_flow_1(self, i, row_offset=1):
        self.adjust_button = ctk.CTkButton(self.flow_frame, text=self.get_text("adjust_settings"),
                                           font=ctk.CTkFont(size=12), width=100,
                                           command=lambda: self.select_frame("Adjust Settings"))
        self.skip_button = ctk.CTkButton(self.flow_frame, text=self.get_text("skip_settings"),
                                         font=ctk.CTkFont(size=12), width=100,
                                         command=lambda: self.on_button_click("Skip Settings"))
        self.adjust_button.grid(row=row_offset + 1, column=i * 2, pady=5, padx=(5, 5))
        self.skip_button.grid(row=row_offset + 2, column=i * 2, pady=5, padx=(5, 5))
        self.cancel_settings = ctk.CTkButton(self.flow_frame, text=self.get_text("cancel"),
                                             font=ctk.CTkFont(size=12), width=100,
                                             fg_color="transparent", hover_color="gray", text_color="#0d6efd",
                                             command=lambda: self.on_button_click("Cancel Settings"))
        self.cancel_settings.grid(row=row_offset + 3, column=i * 2, pady=5, padx=(5, 5))
        self.cancel_settings.grid_remove()
        self.update_button(i, self.adjust_button)
        self.update_button(i, self.skip_button)

    def generation_flow_2(self, i, row_offset=1):
        # Progress bar and status
        # self.progress_frame = ctk.CTkFrame(self.flow_frame, width=100, height=28)
        # self.progress_frame.grid(row=row_offset + 1, column=i * 2)
        # self.progress_frame.grid_columnconfigure(0, weight=1)

        self.progress_bar = ctk.CTkProgressBar(self.flow_frame, width=100, height=12)
        self.progress_bar.grid(row=row_offset + 1, column=i * 2, padx=5, pady=5)
        self.progress_bar.set(0)

        # self.status_label = ctk.CTkLabel(self.progress_frame, text="")
        # self.status_label.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="ew")

        # Hide progress frame initially
        self.progress_bar.grid_remove()

        self.generate_button = ctk.CTkButton(self.flow_frame, text=self.get_text("generate_video"), font=ctk.CTkFont(size=12),
                                             width=100,
                                             command=lambda label="Generate Video": self.on_button_click(label))
        self.generate_button.grid(row=row_offset + 1, column=i * 2, pady=5, padx=5)
        self.update_button(i, self.generate_button)

    def review_flow_3(self, i, row_offset=1):
        self.play_button = ctk.CTkButton(self.flow_frame, text=self.get_text("preview_and_play"),
                                         font=ctk.CTkFont(size=12), width=100,
                                         command=lambda: self.on_button_click("Preview and Play"))
        self.reselect_button = ctk.CTkButton(self.flow_frame, text=self.get_text("reselect_ppt"),
                                             font=ctk.CTkFont(size=12), width=100,
                                             command=lambda: self.on_button_click("Reselect PPT"))
        self.play_button.grid(row=row_offset + 1, column=i * 2, pady=5, padx=(5, 5))
        self.reselect_button.grid(row=row_offset + 2, column=i * 2, pady=5, padx=(5, 5))
        self.update_button(i, self.play_button)
        self.update_button(i, self.reselect_button)

    def create_bottom_section(self):
        self.bottom_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.bottom_frame.grid(row=2, column=0)
        # 显示进度
        progress_label = ctk.CTkLabel(self.bottom_frame, text=f"Step {self.step + 1}/{len(self.icons)}",
                                      font=ctk.CTkFont(size=14))
        progress_label.grid(row=0, column=1, pady=20)

        # 上一步和下一步按钮
        prev_button = ctk.CTkButton(self.bottom_frame, text="", width=20,
                                    image=self.load_ctk_image(os.path.join(self.icon_dir, "left-arrow.png"), size=20),
                                    command=self.prev_step, fg_color="transparent", hover_color="gray")
        next_button = ctk.CTkButton(self.bottom_frame, text="", width=20,
                                    image=self.load_ctk_image(os.path.join(self.icon_dir, "right-arrow.png"), size=20),
                                    command=self.next_step, fg_color="transparent", hover_color="gray")

        prev_button.grid(row=0, column=0, padx=0, pady=10)
        next_button.grid(row=0, column=2, padx=0, pady=10)

    def update_button(self, icon_index, button):
        # 根据步骤更新图标和按钮状态
        if icon_index < self.step:
            # 完成的步骤
            button.configure(state="disabled", fg_color="#28a745")
            icon_image = self.load_ctk_image(self.completed_icons[icon_index], size=50)
        elif icon_index == self.step:
            # 当前步骤
            button.configure(state="normal")
            if icon_index == len(self.completed_icons) - 1:
                icon_image = self.load_ctk_image(self.completed_icons[icon_index], size=50)
            else:
                icon_image = self.load_ctk_image(self.icons[icon_index], size=50)
        else:
            # 后续步骤，禁用
            button.configure(state="disabled", fg_color="gray")
            icon_image = self.load_ctk_image(self.disabled_icons[icon_index], size=50)
        return icon_image

    def prev_step(self):
        logger.info(f"Current Step: {self.step}")
        if self.step > 0:
            self.step -= 1
            self.update_flow()
        logger.info(f"Go previous Step: {self.step}")

    def next_step(self):
        logger.info(f"Current Step: {self.step}")
        if self.step == 0 and self.file_display == "":
            messagebox.showerror("Error", "Please select a PPT file before proceeding.")
            return
        # if self.step == 3 and not os.path.exists(self.setting.video_path):
        #     messagebox.showerror("Error", "Please generate the video before proceeding.")
        #     return
        if self.step < len(self.icons) - 1:
            self.step += 1
            self.update_flow()
        logger.info(f"Go next Step: {self.step}")

    def update_flow(self):
        # self.create_workflow_section()  # 更新流程部分
        # self.create_bottom_section()  # 更新底部导航
        self.select_flow_0(0)
        self.setting_flow_1(1)
        self.generation_flow_2(2)
        self.review_flow_3(3)

    def center_window(self):
        """Center the window on the screen."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 800
        window_height = 400
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

    def get_translation(self):
        if self.current_language in self._translations_cache:
            return self._translations_cache[self.current_language]

        locale_dir = resource_path(os.path.join('pptflow', os.path.join('locales', self.current_language)))
        translation_file = os.path.join(locale_dir, 'messages.json')

        if not os.path.exists(translation_file):
            locale_dir = resource_path(os.path.join('pptflow', os.path.join('locales', self.language_modes[0])))
            translation_file = os.path.join(locale_dir, 'messages.json')

        with open(translation_file, 'r', encoding='utf-8') as f:
            translations = json.load(f)

        self._translations_cache[self.current_language] = translations
        return translations

    def clear_temp_cache(self):
        self.clear_audio_cache()
        self.clear_image_cache()
        logger.info("Clear temp cache")

    def clear_audio_cache(self):
        if os.path.exists(self.setting.audio_dir_path):
            shutil.rmtree(self.setting.audio_dir_path)
        logger.info("Clear audio cache")

    def clear_image_cache(self):
        if os.path.exists(self.setting.image_dir_path):
            shutil.rmtree(self.setting.image_dir_path)
        logger.info("Clear image cache")

    def on_button_click(self, label_text):
        logger.info(f"Button clicked! Text:{label_text}")
        if label_text == "Select PPT File":
            self.browse_file()
        elif label_text == "Cancel File":
            self.reselect_file()
        elif label_text == "Adjust Settings":
            self.select_frame("Adjust Settings")
        elif label_text == "Skip Settings":
            self.step += 1
            self.adjust_button.grid_remove()
            self.skip_button.grid_remove()
            self.setting_flow_1(1)
            self.cancel_settings.grid()
            self.generation_flow_2(2)
        elif label_text == "Cancel Settings":
            self.step = 1
            self.cancel_settings.grid_remove()
            self.setting_flow_1(1)
            self.generation_flow_2(2)
            self.review_flow_3(3)
        elif label_text == "Generate Video":
            threading.Thread(target=self.generate_video).start()
        elif label_text == "Preview and Play":
            self.play_video()
        elif label_text == "Reselect PPT":
            self.step = 0
            self.file_display = ""
            self.update_flow()
        elif label_text == "Github":
            webbrowser.open("https://github.com/archworks/pptflow")
        elif label_text == "Discord":
            messagebox.showinfo("Discord", "Join our Discord server for support and updates!")

    def browse_file(self):
        self.file_display = filedialog.askopenfilename(
            filetypes=[("PowerPoint files", "*.ppt"), ("PowerPoint files", "*.pptx")]
        )
        if self.file_display:
            logger.info(f"Selected file: {self.file_display}")
            # Open the PowerPoint file and get the number of slides
            presentation = Presentation(self.file_display)
            if len(presentation.slides) == 0:
                messagebox.showerror("Error", self.get_text("no_slide"))
                return
            logger.info(f"Total slides: {len(presentation.slides)}")

            # Set the default output path
            self.setting.video_path = re.sub(r"pptx?$", "mp4", self.file_display)

            self.file_label.grid()
            self.file_label.configure(state=ctk.NORMAL)
            # 显示文件名
            display_text = truncate_text(os.path.basename(self.file_display), max_length=10)
            self.tooltip = CustomTooltip(self.file_label, os.path.basename(self.file_display))
            self.file_label_var.set(display_text)
            self.file_label.configure(state=ctk.DISABLED)
            self.cancel_file.grid()

            self.select_button.grid_remove()
            self.step += 1
            self.setting_flow_1(1)

    def select_frame(self, name):
        # for widget in self.main_frame.winfo_children():
        #     widget.grid_remove()  # 确保组件从布局中移除
        self.flow_frame.grid_remove()
        if name == "Adjust Settings":
            from .adjust_settings import AdjustSettingsFrame
            # 显示 ExportSection
            self.adjust_settings = AdjustSettingsFrame(self)
            self.adjust_settings.grid(row=1, column=0, padx=100, sticky="nsew")
            self.adjust_settings.refresh()
            self.adjust_settings.tkraise()
        elif name == "Skip Settings":
            self.next_step()
        elif name == "System Settings":
            if self.adjust_settings is not None:
                self.adjust_settings.grid_remove()
            self.flow_frame.grid_remove()
            from .system_settings import SystemSettingsFrame
            self.system_settings = SystemSettingsFrame(self)
            self.system_settings.grid(row=1, column=0, padx=200, sticky="nsew")
            self.system_settings.tkraise()

    def load_tts(self, tts_service_provider):
        # import tts module according to service provider
        if not tts_service_provider:
            logger.error("tts服务未配置")
            raise NotImplementedError(f"tts服务未配置")
        if tts_service_provider.lower() == "azure":
            from pptflow.tts.tts_azure import tts, get_voice_list
            sd.tts_speech_voices = get_voice_list(self.setting)
            logger.info(f"tts service provider: {tts_service_provider}")
        elif tts_service_provider.lower() == "edge-tts":
            from pptflow.tts.tts_edge_tts import tts, get_voice_list
            sd.tts_speech_voices = get_voice_list()
            logger.info(f"tts service provider: {tts_service_provider}")
        # elif tts_service_provider.lower() == "xunfei":
        #     from .tts_xunfei import tts
        #     logger.info(f"tts service provider: {tts_service_provider}")
        elif tts_service_provider.lower() == "pyttsx3":
            from pptflow.tts.tts_pyttsx3 import tts
            logger.info(f"tts service provider: {tts_service_provider}")
        elif tts_service_provider.lower() == "coqui-tts":
            from pptflow.tts.tts_Coqui_tts import tts
            logger.info(f"tts service provider: {tts_service_provider}")
        else:
            logger.error(f"不支持的tts: {tts_service_provider}")
            raise NotImplementedError(f"不支持的tts: {tts_service_provider}")
        return tts

    def get_default_subtitle_font(self):
        current_platform = platform.system().lower()
        if current_platform == 'windows':
            return self.setting.win_subtitle_font
        elif current_platform == 'darwin':  # macOS
            return self.setting.mac_subtitle_font
        else:
            logger.info(f"Unsupported platform: {current_platform}. Using default font.")
            return 'Arial'

    def update_progress(self, progress: float, status: str):
        """Update progress bar and status label"""
        self.progress_bar.set(progress)
        # self.status_label.configure(text=status)

    def generate_video(self):
        if not self.setting.subtitle_font_path:
            self.setting.subtitle_font_path = font.find_font_path(self.get_default_subtitle_font())
        if not self.file_display:
            messagebox.showerror(self.loading_title, self.get_text("no_file_selected"))
            return
        try:
            # Show progress frame
            self.generate_button.grid_remove()
            self.progress_bar.grid()
            self.update()
            # self.progress_bar.grid()
            # self.generate_button.grid()
            # self.generate_button.configure(state=ctk.DISABLED)

            # Initialize progress tracker
            self.progress_tracker = ProgressTracker(self.update_progress)

            # self.generate_button.grid_remove()
            ppt2video.ppt_to_video(self.tts, self.file_display, self.setting, self.progress_tracker)

            messagebox.showinfo(self.loading_title,
                                f'{self.get_text("video_generated")}{self.setting.video_path}')
            self.step += 1
            self.generation_flow_2(2)
            self.review_flow_3(3)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate video: {str(e)}")
            logger.error(e, exc_info=True)
            return
        finally:
            # Hide progress frame
            self.progress_bar.grid_remove()
            self.generate_button.grid()
            self.progress_bar.set(0)
            # self.status_label.configure(text="")

    def play_video(self):
        logger.info(f'video_path:{self.setting.video_path}')
        try:
            if not os.path.exists(self.setting.video_path):
                logger.error(f'video_path:{self.setting.video_path} does not exist!')
                raise FileNotFoundError(f'video_path:{self.setting.video_path} does not exist!')
            os.startfile(self.setting.video_path)
        except Exception as e:
            messagebox.showerror("Error", "No video was generated!")
            logger.error(e, exc_info=True)

    def reselect_file(self):
        self.step = 0
        self.file_label_var.set("")
        self.tooltip = None
        self.setting.video_path = ""
        self.cancel_file.grid_remove()
        # self.update_flow()
        self.create_workflow_section()

    def load_ctk_image(self, file_name, size):
        try:
            icon_dir = resource_path(os.path.join("assets", "icons"))
            file_name = os.path.join(icon_dir, file_name)
            # 加载并调整图标大小
            img = Image.open(file_name)
            img = img.resize((size, size), Image.LANCZOS)  # 替换 ANTI_ALIAS 为 LANCZOS
            return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))  # 使用 CTkImage
        except Exception as e:
            print(f"Error loading icon {file_name}: {e}")
            return None

    def update_language(self):
        if self.select_button:
            self.select_button.configure(text=self.get_text("select_ppt"))
        if self.cancel_file:
            self.cancel_file.configure(text=self.get_text("cancel"))
        self.adjust_button.configure(text=self.get_text("adjust_settings"))
        self.skip_button.configure(text=self.get_text("skip_settings"))
        if self.cancel_settings:
            self.cancel_settings.configure(text=self.get_text("cancel"))
        if self.generate_button:
            self.generate_button.configure(text=self.get_text("generate_video"))
        self.play_button.configure(text=self.get_text("preview_and_play"))
        self.reselect_button.configure(text=self.get_text("reselect_ppt"))


def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):  # 打包后运行环境
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath(""), relative_path)


def get_locales_subdirectories():
    # Get the absolute path to the current file
    current_file_path = os.path.abspath(__file__)
    # Get the directory path of the current file
    current_directory = os.path.dirname(current_file_path)
    # Get the parent path of the current directory
    parent_directory = os.path.dirname(current_directory)
    # Get the absolute path of the parent directory
    language_locales_path = os.path.join(parent_directory, 'locales')
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


def truncate_text(text, max_length=20):
    """ 截取文本，确保头部+省略号+尾部不超过 max_length """
    if len(text) > max_length:
        return text[:max_length // 2] + "..." + text[-(max_length // 2):]
    return text


if __name__ == "__main__":
    app = PPTFlowApp()
    app.mainloop()
