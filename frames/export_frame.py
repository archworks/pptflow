import customtkinter as ctk
from tkinter import filedialog
from pptflow.setting import Setting
from utils import mylogger

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)


def start_export():
    try:
        if Setting.start_page_num is not None and Setting.end_page_num is not None:
            if Setting.start_page_num > Setting.end_page_num:
                raise ValueError("Start page number cannot be greater than end page number.")
    except ValueError as e:
        logger.error(str(e))
    # Add export logic here
    pass


class ExportFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.run_export = None
        self.app = app
        self.grid_columnconfigure(0, weight=1)

        # Title
        self.title = ctk.CTkLabel(self, text=self.app.get_text("export_title"),
                                  font=ctk.CTkFont(size=24, weight="bold"))
        self.title.grid(row=0, column=0, padx=20, pady=(40, 20))

        # Export settings
        self.create_export_frame()
        self.create_progress_frame()


    def create_export_frame(self):
        frame = ctk.CTkFrame(self)
        frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Output path
        self.path_label = ctk.CTkLabel(frame, text=f'{self.app.get_text("export_path")}:')
        self.path_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.output_path = ctk.CTkEntry(frame, width=400)
        self.output_path.grid(row=0, column=1, padx=(20, 10), pady=10)

        self.browse_button = ctk.CTkButton(frame, text=self.app.get_text("browse"),
                                           command=self.browse_output_path)
        self.browse_button.grid(row=0, column=2, padx=(0, 20), pady=10)

        # Export button
        self.export_button = ctk.CTkButton(frame, text=self.app.get_text("export_button"),
                                           command=start_export)
        self.export_button.grid(row=1, column=0, columnspan=3, padx=20, pady=20)

    def create_progress_frame(self):
        frame = ctk.CTkFrame(self)
        frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # Progress bar
        self.progress = ctk.CTkProgressBar(frame)
        self.progress.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.progress.set(0)

        # Status label
        self.status = ctk.CTkLabel(frame, text=self.app.get_text("export_progress"))
        self.status.grid(row=1, column=0, padx=20, pady=(0, 20))

    def browse_output_path(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4")]
        )
        if path:
            self.output_path.delete(0, "end")
            self.output_path.insert(0, path)

    def update_language(self):
        self.title.configure(text=self.app.get_text("export_title"))
        self.path_label.configure(text=self.app.get_text("export_path"))
        self.browse_button.configure(text=self.app.get_text("browse"))
        self.export_button.configure(text=self.app.get_text("export_button"))
        self.status.configure(text=self.app.get_text("export_progress"))
