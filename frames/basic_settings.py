import customtkinter as ctk
from pptflow.setting import Setting


class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1)


class BasicSettingsFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Make scrollable frame expand

        # Title
        self.title = ctk.CTkLabel(self, text=self.app.get_text("basic_settings"),
                                  font=ctk.CTkFont(size=24, weight="bold"))
        self.title.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Create scrollable container
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Settings sections
        self.create_ppt_settings()
        self.create_audio_settings()
        self.create_video_settings()
        self.create_subtitle_settings()

    def create_ppt_settings(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=0, column=0, padx=0, pady=(0, 10), sticky="ew")

        self.ppt_setting_label = ctk.CTkLabel(frame, text=self.app.get_text("ppt_settings"),
                             font=ctk.CTkFont(size=16, weight="bold"))
        self.ppt_setting_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Start and end pages
        self.start_label = ctk.CTkLabel(frame, text=f'{self.app.get_text("start_page")}:')
        self.start_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.start_page = ctk.CTkEntry(frame, width=100)
        self.start_page.grid(row=1, column=1, padx=5, pady=5)

        self.end_label = ctk.CTkLabel(frame, text=f'{self.app.get_text("end_page")}:')
        self.end_label.grid(row=1, column=2, padx=20, pady=5, sticky="w")
        self.end_page = ctk.CTkEntry(frame, width=100)
        self.end_page.grid(row=1, column=3, padx=5, pady=5)
        Setting.start_page_num = self.start_page
        Setting.end_page_num = self.end_page


    def create_audio_settings(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=1, column=0, padx=0, pady=(0, 10), sticky="ew")

        self.audio_setting_label = ctk.CTkLabel(frame, text=self.app.get_text("audio_settings"),
                             font=ctk.CTkFont(size=16, weight="bold"))
        self.audio_setting_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # TTS settings
        options = [self.app.get_text("audio_engine"), self.app.get_text("audio_language"),
                   self.app.get_text("audio_voice_type"), self.app.get_text("audio_speed")]
        for i, option in enumerate(options):
            label = ctk.CTkLabel(frame, text=f"{option}:")
            label.grid(row=i + 1, column=0, padx=20, pady=5, sticky="w")

            combobox = ctk.CTkComboBox(frame, values=["选项1", "选项2", "选项3"])
            combobox.grid(row=i + 1, column=1, padx=5, pady=5)

    def create_video_settings(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=2, column=0, padx=0, pady=(0, 10), sticky="ew")

        self.video_setting_label = ctk.CTkLabel(frame, text=self.app.get_text("video_settings"),
                             font=ctk.CTkFont(size=16, weight="bold"))
        self.video_setting_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Video settings
        settings = {
            self.app.get_text("video_format"): ["MP4", "AVI", "MOV"],
            self.app.get_text("video_size"): ["1920x1080", "1280x720", "854x480"],
            self.app.get_text("video_framerate"): ["10fps", "24fps", "30fps"]
        }

        for i, (key, values) in enumerate(settings.items()):
            label = ctk.CTkLabel(frame, text=f"{key}:")
            label.grid(row=i + 1, column=0, padx=20, pady=5, sticky="w")

            combobox = ctk.CTkComboBox(frame, values=values)
            combobox.grid(row=i + 1, column=1, padx=5, pady=5)

    def create_subtitle_settings(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=3, column=0, padx=0, pady=(0, 10), sticky="ew")

        self.subtitle_setting_label = ctk.CTkLabel(frame, text=self.app.get_text("subtitle_settings"),
                             font=ctk.CTkFont(size=16, weight="bold"))
        self.subtitle_setting_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Subtitle settings
        settings = [self.app.get_text("font_type"), self.app.get_text("font_size"),
                    self.app.get_text("font_color"), self.app.get_text("border_color")]
        for i, setting in enumerate(settings):
            label = ctk.CTkLabel(frame, text=f"{setting}:")
            label.grid(row=i + 1, column=0, padx=20, pady=5, sticky="w")

            if setting in [self.app.get_text("font_type")]:
                widget = ctk.CTkComboBox(frame, values=["Arial", "Times New Roman", "微软雅黑"])
            elif setting in [self.app.get_text("font_size")]:
                widget = ctk.CTkComboBox(frame, values=["12", "14", "16", "18", "20"])
            else:
                widget = ctk.CTkButton(frame, text=self.app.get_text("select_color"))

            widget.grid(row=i + 1, column=1, padx=5, pady=5)

    # Update language of Basic Settings Frame
    def update_language(self):
        self.title.configure(text=self.app.get_text("basic_settings"))
        self.ppt_setting_label.configure(text=self.app.get_text("ppt_settings"))
        self.start_label.configure(text=self.app.get_text("start_page"))
        self.end_label.configure(text=self.app.get_text("end_page"))
        self.create_audio_settings()
        self.create_video_settings()
        self.create_subtitle_settings()

