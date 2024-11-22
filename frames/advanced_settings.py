import customtkinter as ctk


class AdvancedSettingsFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Make scrollable frame expand

        # Title
        self.title = ctk.CTkLabel(self, text=self.app.get_text("advanced_title"),
                                  font=ctk.CTkFont(size=24, weight="bold"))
        self.title.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Create scrollable container
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Create settings sections
        self.create_audio_settings()
        self.create_video_settings()

    def create_audio_settings(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=0, column=0, padx=0, pady=(0, 10), sticky="ew")

        self.audio_title = ctk.CTkLabel(frame, text=self.app.get_text("advanced_audio"),
                                        font=ctk.CTkFont(size=16, weight="bold"))
        self.audio_title.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Audio settings
        settings = {
            self.app.get_text("audio_format"): ["WAV", "MP3", "AAC"],
            self.app.get_text("audio_codec"): ["PCM", "MP3", "AAC"],
        }
        self.audio_format_label = ctk.CTkLabel(frame, text=f'{self.app.get_text("audio_format")}:')
        self.audio_format_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.audio_format = ctk.CTkComboBox(frame, values=settings[self.app.get_text("audio_format")])
        self.audio_format.grid(row=1, column=1, padx=5, pady=5)
        self.audio_codec_label = ctk.CTkLabel(frame, text=f'{self.app.get_text("audio_codec")}:')
        self.audio_codec_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        self.audio_codec = ctk.CTkComboBox(frame, values=settings[self.app.get_text("audio_codec")])
        self.audio_codec.grid(row=2, column=1, padx=5, pady=5)

        # Save audio checkbox
        self.save_audio = ctk.CTkCheckBox(frame, text=f'{self.app.get_text("save_audio")}:')
        self.save_audio.grid(row=len(settings) + 1, column=0, padx=20, pady=10, sticky="w")

    def create_video_settings(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=1, column=0, padx=0, pady=(0, 10), sticky="ew")

        self.video_title = ctk.CTkLabel(frame, text=self.app.get_text("advanced_video"),
                                        font=ctk.CTkFont(size=16, weight="bold"))
        self.video_title.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Video codec
        self.video_codec_label = ctk.CTkLabel(frame, text=f'{self.app.get_text("video_codec")}:')
        self.video_codec_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")

        self.video_codec = ctk.CTkComboBox(frame, values=["H.264", "H.265", "VP9"])
        self.video_codec.grid(row=1, column=1, padx=5, pady=5)

        # Thread count
        self.thread_label = ctk.CTkLabel(frame, text=f'{self.app.get_text("threads")}:')
        self.thread_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")

        self.threads = ctk.CTkComboBox(frame, values=["1", "2", "4", "8"])
        self.threads.grid(row=2, column=1, padx=5, pady=5)

    # Update language of Advanced Settings Frame
    def update_language(self):
        self.title.configure(text=self.app.get_text("advanced_title"))
        self.audio_title.configure(text=self.app.get_text("advanced_audio"))
        self.audio_format_label.configure(text=self.app.get_text("audio_format"))
        self.audio_codec_label.configure(text=self.app.get_text("audio_codec"))
        self.save_audio.configure(text=self.app.get_text("save_audio"))
        self.video_title.configure(text=self.app.get_text("advanced_video"))
        self.video_codec_label.configure(text=self.app.get_text("video_codec"))
        self.thread_label.configure(text=self.app.get_text("threads"))
