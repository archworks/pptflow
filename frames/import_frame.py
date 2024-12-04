import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import pptflow.ppt2video as ppt2video
import threading
from utils import mylogger

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)


class ImportFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.grid_columnconfigure(0, weight=1)

        # Title
        self.title = ctk.CTkLabel(self, text=self.app.get_text("import_title"),
                                  font=ctk.CTkFont(size=24, weight="bold"))
        self.title.grid(row=0, column=0, padx=20, pady=(40, 20))

        # File selection frame
        self.file_frame = ctk.CTkFrame(self)
        self.file_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        # self.file_frame.grid_columnconfigure(0, weight=1)
        self.file_display = ""
        self.file_path = ctk.CTkEntry(self.file_frame, width=200, placeholder_text=self.app.get_text("select_ppt"))
        self.file_path.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="ew")

        self.browse_button = ctk.CTkButton(self.file_frame, text=self.app.get_text("browse"),
                                           command=self.browse_file)
        self.browse_button.grid(row=0, column=1, padx=(0, 20), pady=20)
        # File info
        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

        self.file_info = ctk.CTkLabel(self.info_frame, text=self.app.get_text("no_file"),
                                      font=ctk.CTkFont(size=14))
        self.file_info.grid(row=0, column=0, padx=20, pady=20)
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.info_frame, orientation="horizontal", mode="determinate")
        self.progress_bar.grid_forget()  # Hide progress bar initially

        # Generate video button
        self.generate_button = ctk.CTkButton(self.info_frame, text=self.app.get_text("generate_video"),
                                             command=self.start_video_generation)
        self.generate_button.grid(row=3, column=0, padx=20, pady=20)
        # Loading prompt
        self.loading_title = self.app.get_text("generate_video")
        # Play video button
        self.play_button = ctk.CTkButton(self.info_frame, text=self.app.get_text("play_video"),
                                         command=self.play_video)
        self.play_button.grid(row=4, column=0, padx=20, pady=20)

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

    # Generate video button action
    def generate_video(self):
        # logger.info(f'file_path:{self.file_display}')
        # self.progress_bar.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        # self.progress_bar.set(0)
        # self.update_idletasks()  # 确保界面更新

        try:
            # 假设 ppt2video.process 返回一个生成器，每次生成一部分视频
            ppt2video.process(self.file_display, self.app.setting)
            messagebox.showinfo(self.loading_title, self.app.get_text("video_generated"))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate video: {str(e)}")
            logger.error(e)
        # Hide progress bar after completion
        self.progress_bar.grid_forget()

    def start_video_generation(self):
        # Run the video generation in a separate thread
        threading.Thread(target=self.generate_video).start()

        messagebox.showinfo(self.loading_title, self.app.get_text("start_generate_video"))

    # Play video button action
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

    # Update language of ImportFrame
    def update_language(self):
        self.title.configure(text=self.app.get_text("import_title"))
        self.file_path.configure(placeholder_text=self.app.get_text("select_ppt"))
        self.browse_button.configure(text=self.app.get_text("browse"))
        self.file_info.configure(text=self.app.get_text("no_file") if not self.file_display else f"{self.app.get_text('selected_file')}: {os.path.basename(self.file_display)}")
        self.generate_button.configure(text=self.app.get_text("generate_video"))
        self.play_button.configure(text=self.app.get_text("play_video"))
        self.loading_title = self.app.get_text("generate_video")
