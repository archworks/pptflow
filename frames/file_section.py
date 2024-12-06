import os
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pptflow import ppt2video
from utils import mylogger

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)


class FileSection(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Title
        self.title = ctk.CTkLabel(
            self,
            text=self.app.get_text("video_generation"),
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title.grid(row=0, column=0, padx=20, pady=20)

        # Main content frame
        # Create scrollable frame for settings
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Loading prompt
        self.loading_title = self.app.get_text("generate_video")

        # File selection
        self.file_display = ""
        self.create_file_selection()
        self.create_file_info()
        self.create_page_range()
        self.create_generate_button()
        self.create_play_button()

    def create_file_selection(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=0, column=0, padx=0, pady=(0, 10), sticky="ew")

        # File path entry
        self.file_path = ctk.CTkEntry(
            frame, width=300,
            placeholder_text=self.app.get_text("select_ppt"),
        )
        self.file_path.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Browse button
        self.browse_btn = ctk.CTkButton(
            frame,
            text=self.app.get_text("browse"),
            command=self.browse_file
        )
        self.browse_btn.grid(row=0, column=2, padx=(0, 20), pady=10)

    def create_file_info(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=1, column=0, padx=0, pady=5, sticky="ew")

        self.file_info = ctk.CTkLabel(frame, text=self.app.get_text("no_file"),
                                      font=ctk.CTkFont(size=14))
        self.file_info.grid(row=0, column=0, padx=20, pady=5)

    def create_page_range(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=2, column=0, padx=0, pady=10, sticky="ew")

        # Title
        self.page_title = ctk.CTkLabel(
            frame,
            text=self.app.get_text("page_range"),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.page_title.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="w")

        # Start page
        self.start_label = ctk.CTkLabel(frame, text=self.app.get_text("start_page"))
        self.start_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.start_page = ctk.CTkEntry(frame, width=150, placeholder_text=self.app.get_text("start_page_info"))
        self.start_page.grid(row=1, column=1, padx=5, pady=10, sticky="w")
        # self.start_page.insert(0, "1")

        # End page
        self.end_label = ctk.CTkLabel(frame, text=self.app.get_text("end_page"))
        self.end_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.end_page = ctk.CTkEntry(frame, width=150, placeholder_text=self.app.get_text("end_page_info"))
        self.end_page.grid(row=2, column=1, padx=5, pady=10, sticky="w")

    def create_generate_button(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=3, column=0, padx=0, pady=(0, 10), sticky="ew")

        self.generate_button = ctk.CTkButton(
            frame,
            text=self.app.get_text("generate_video"),
            command=self.start_video_generation
        )
        self.generate_button.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

    def create_play_button(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=4, column=0, padx=0, pady=(0, 10), sticky="ew")

        self.play_button = ctk.CTkButton(
            frame,
            text=self.app.get_text("play_video"),
            command=self.play_video
        )
        self.play_button.grid(row=0, column=0, padx=20, pady=(0, 20), sticky="ew")

    def browse_file(self):
        self.file_display = filedialog.askopenfilename(
            filetypes=[("PowerPoint files", "*.ppt;*.pptx")]
        )
        if self.file_display:
            self.file_path.configure(state=ctk.NORMAL)
            self.file_path.delete(0, "end")
            self.file_path.insert(0, self.file_display)
            self.file_info.configure(
                text=f"{self.app.get_text('selected_file')}: {os.path.basename(self.file_display)}"
            )
            self.file_path.configure(state=ctk.DISABLED)

    def generate_video(self):
        try:
            # 假设 ppt2video.process 返回一个生成器，每次生成一部分视频
            ppt2video.process(self.file_display, self.app.setting)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate video: {str(e)}")
            logger.error(e)
            return
        messagebox.showinfo(self.loading_title, self.app.get_text("video_generated"))
        # Hide progress bar after completion

    def start_video_generation(self):
        if not self.file_display:
            messagebox.showerror(self.loading_title, self.app.get_text("no_file_selected"))
            return
        # Run the video generation in a separate thread
        threading.Thread(target=self.generate_video).start()
        messagebox.showinfo(self.loading_title, self.app.get_text("start_generate_video"))

    def play_video(self):
        logger.info(f'video_path:{self.app.setting.video_path}')
        try:
            if not os.path.exists(self.app.setting.video_path):
                logger.error(f'video_path:{self.app.setting.video_path} does not exist!')
                raise FileNotFoundError(f'video_path:{self.app.setting.video_path} does not exist!')
            os.startfile(self.app.setting.video_path)
        except Exception as e:
            messagebox.showerror("Error", "No video was generated!")
            logger.error(e)

    def update_language(self):
        self.title.configure(text=self.app.get_text("video_generation"))
        self.file_path.configure(placeholder_text=self.app.get_text("select_ppt"))
        self.generate_button.configure(text=self.app.get_text("generate_video"))
        self.play_button.configure(text=self.app.get_text("play_video"))
        self.file_info.configure(text=self.app.get_text("no_file"))
        self.browse_btn.configure(text=self.app.get_text("browse"))
        self.page_title.configure(text=self.app.get_text("page_range"))
        self.start_label.configure(text=self.app.get_text("start_page"))
        self.start_page.configure(placeholder_text=self.app.get_text("start_page_info"))
        self.end_label.configure(text=self.app.get_text("end_page"))
        self.end_page.configure(placeholder_text=self.app.get_text("end_page_info"))
