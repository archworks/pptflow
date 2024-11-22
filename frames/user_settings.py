import customtkinter as ctk


class UserSettingsFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Make scrollable frame expand

        # Title
        self.title = ctk.CTkLabel(self, text=self.app.get_text("user_settings"),
                                  font=ctk.CTkFont(size=24, weight="bold"))
        self.title.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Create scrollable container
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # User info frame
        self.create_user_info_frame()

    def create_user_info_frame(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=0, column=0, padx=0, pady=(0, 10), sticky="ew")

        # User information fields
        # fields = ["用户名", "邮箱", "手机号码"]
        fields = [self.app.get_text('username'), self.app.get_text('email'), self.app.get_text('phone')]

        for i, field in enumerate(fields):
            label = ctk.CTkLabel(frame, text=f"{field}:")
            label.grid(row=i, column=0, padx=20, pady=10, sticky="w")

            entry = ctk.CTkEntry(frame, width=300)
            entry.grid(row=i, column=1, padx=20, pady=10)

        # Save button
        self.save_button = ctk.CTkButton(frame, text=self.app.get_text("save_settings"))
        self.save_button.grid(row=len(fields), column=0, columnspan=2, padx=20, pady=20)

    # Update language
    def update_language(self):
        self.title.configure(text=self.app.get_text("user_settings"))
        self.create_user_info_frame()
