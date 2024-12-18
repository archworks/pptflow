import os
import re
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pptflow import ppt2video
from utils import mylogger
from pptx import Presentation
from utils import setting_dic as sd

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
        # self.create_file_info()
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

    # def create_file_info(self):
    #     frame = ctk.CTkFrame(self.scrollable_frame)
    #     frame.grid(row=1, column=0, padx=0, pady=5, sticky="ew")
    #
    #     self.file_info = ctk.CTkLabel(frame, text=self.app.get_text("no_file"),
    #                                   font=ctk.CTkFont(size=14))
    #     self.file_info.grid(row=0, column=0, padx=20, pady=5)

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

        # 创建一个StringVar对象，并设置输入验证
        validate_cmd = frame.register(self.validate_input)
        # Create variables of start and end page
        self.start_page_var = ctk.StringVar()
        self.end_page_var = ctk.StringVar()

        # Start page
        self.start_label = ctk.CTkLabel(frame, text=self.app.get_text("start_page"))
        self.start_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.start_page = ctk.CTkEntry(frame, width=50, textvariable=self.start_page_var,
                                       validate="key", validatecommand=(validate_cmd, "%P"))
        self.start_page.bind("<FocusOut>", self.adjust_start_page)
        self.start_page.grid(row=1, column=1, padx=5, pady=10, sticky="w")
        # self.start_page.insert(0, "1")

        # End page
        self.end_label = ctk.CTkLabel(frame, text=self.app.get_text("end_page"))
        self.end_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.end_page = ctk.CTkEntry(frame, width=50, textvariable=self.end_page_var,
                                     validate="key", validatecommand=(validate_cmd, "%P"))
        self.end_page.bind("<FocusOut>", self.adjust_end_page)
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
            # Open the PowerPoint file and get the number of slides
            presentation = Presentation(self.file_display)
            self.app.setting.ppt_total_slides = len(presentation.slides)
            if self.app.setting.ppt_total_slides == 0:
                messagebox.showerror("Error", self.app.get_text("no_slide"))
                return
            logger.info(f"Total slides: {self.app.setting.ppt_total_slides}")

            # Set the default start and end page numbers
            self.start_page_var.set("1")
            self.end_page_var.set(str(self.app.setting.ppt_total_slides))

            # Set the default output path
            self.app.setting.video_path = re.sub(r"pptx?$", "mp4", self.file_display)

            # Update the file path entry
            self.file_path.configure(state=ctk.NORMAL)
            self.file_path.delete(0, "end")
            self.file_path.insert(0, self.file_display)
            # self.file_info.configure(
            #     text=f"{self.app.get_text('selected_file')}: {os.path.basename(self.file_display)}"
            # )
            self.file_path.configure(state=ctk.DISABLED)

    def generate_video(self):
        try:
            # Get start and end page numbers from the entry fields
            self.app.setting.start_page_num = int(self.start_page.get())
            self.app.setting.end_page_num = int(self.end_page.get())

            # Check if start and end page numbers are valid
            if self.app.setting.end_page_num < self.app.setting.start_page_num:
                messagebox.showerror("Error", "End page number must be greater than or equal to start page number.")
                return
            ppt2video.process(self.file_display, self.app.setting)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate video: {str(e)}")
            logger.error(e, exc_info=True)
            return
        messagebox.showinfo(self.loading_title, f'{self.app.get_text("video_generated")}{self.app.setting.video_path}')

    def start_video_generation(self):
        if not os.path.exists(self.app.setting.subtitle_font):
            self.app.setting.subtitle_font = sd.subtitle_font_dict[self.app.setting.subtitle_font]
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
            logger.error(e, exc_info=True)

    def validate_input(self, text):
        """检查输入是否为数字"""
        return text.isdigit() or text == ""  # 允许数字和空字符串（用于删除）

    def adjust_start_page(self, event):
        """调整start_page的值"""
        value = self.start_page_var.get()
        MAX_PAGE = self.app.setting.ppt_total_slides if self.app.setting.ppt_total_slides else 1
        if value == "" or int(value) < 1:  # 如果为空或小于1
            self.start_page_var.set("1")  # 自动设置为1
        elif int(value) > MAX_PAGE:  # 如果超过最大页数
            self.start_page_var.set(str(MAX_PAGE))  # 自动设置为最大页数

    def adjust_end_page(self, event):
        """调整end_page的值"""
        value = self.end_page_var.get()
        MAX_PAGE = self.app.setting.ppt_total_slides if self.app.setting.ppt_total_slides else 1
        if value == "" or int(value) < 1:  # 如果为空或小于1
            self.end_page_var.set("1")  # 自动设置为1
        elif int(value) > MAX_PAGE:  # 如果超过最大页数
            self.end_page_var.set(str(MAX_PAGE))  # 自动设置为最大页数

    def update_language(self):
        self.title.configure(text=self.app.get_text("video_generation"))
        self.file_path.configure(placeholder_text=self.app.get_text("select_ppt"))
        self.generate_button.configure(text=self.app.get_text("generate_video"))
        self.play_button.configure(text=self.app.get_text("play_video"))
        # self.file_info.configure(text=self.app.get_text("no_file"))
        self.browse_btn.configure(text=self.app.get_text("browse"))
        self.page_title.configure(text=self.app.get_text("page_range"))
        self.start_label.configure(text=self.app.get_text("start_page"))
        # self.start_page.configure(placeholder_text=self.app.get_text("start_page_info"))
        self.end_label.configure(text=self.app.get_text("end_page"))
        # self.end_page.configure(placeholder_text=self.app.get_text("end_page_info"))

    def refresh(self):
        pass
