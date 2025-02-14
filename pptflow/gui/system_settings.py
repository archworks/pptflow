# Author: Valley-e
# Date: 2025/1/16  
# Description:
import customtkinter as ctk
from pptflow.utils import mylogger

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)


class SystemSettingsFrame(ctk.CTkFrame):
    def __init__(self, app, frame):
        super().__init__(frame, fg_color="white")
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.font_size = 12
        self.font = ctk.CTkFont(size=self.font_size, weight="normal")

        # self.title = ctk.CTkLabel(
        #     self,
        #     text=self.app.get_text("system_settings"),
        #     font=ctk.CTkFont(size=12, weight="bold")
        # )
        # self.title.grid(row=0, column=0, padx=20, pady=20)
        # self.title.grid_remove()

        self.setting_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.setting_frame.grid(row=0, column=0, padx=100, pady=(50, 0), sticky="nsew")
        self.setting_frame.grid_columnconfigure(0, weight=1)

        self.create_language_mode()
        # self.create_theme_mode()
        # self.create_scale_mode()
        self.create_confirm_cancel_button()

    def create_language_mode(self):
        # Language selection
        self.language_label = ctk.CTkLabel(self.setting_frame, text=self.app.get_text("ui_language"), font=self.font)
        self.language_label.grid(row=0, column=0, padx=20, pady=10, sticky="s")

        self.language_list = [self.app.get_text(language) for language in self.app.language_modes]
        self.language_var = ctk.StringVar()
        self.language_setting = ctk.CTkComboBox(self.setting_frame, font=self.font,
                                                values=self.language_list,
                                                variable=self.language_var)
        self.language_setting.grid(row=0, column=1, padx=20, pady=10)
        # self.language_setting.set(self.app.get_text(self.app.current_language))
        self.language_var.set(self.app.get_text(self.app.current_language))

    def create_theme_mode(self):
        # Theme selection
        self.theme_label = ctk.CTkLabel(self.setting_frame, text=self.app.get_text("theme"), font=self.font)
        self.theme_label.grid(row=1, column=0, padx=20, pady=10)

        self.theme_var = ctk.StringVar()
        self.theme = ctk.CTkComboBox(self.setting_frame, values=[self.app.get_text("light"),
                                                                 self.app.get_text("dark"),
                                                                 self.app.get_text("system")],
                                     variable=self.theme_var,
                                     font=self.font)
        self.theme.grid(row=1, column=1, padx=20, pady=10)
        self.theme_map = {self.app.translations[key]: key for key in ['light', 'dark', 'system']}
        self.theme_var.set(self.app.get_text(self.app.theme))  # 设置默认值

    # def create_scale_mode(self):
    #     # Scaling selection
    #     self.scaling_label = ctk.CTkLabel(self.setting_frame, text=self.app.get_text("ui_scaling"), font=self.font)
    #     self.scaling_label.grid(row=2, column=0, padx=20, pady=10)
    #     self.scaling_optionemenu = ctk.CTkComboBox(self.setting_frame, values=["80%", "90%", "100%", "110%", "120%"],
    #                                                command=self.change_scaling_event, font=self.font)
    #     self.scaling_optionemenu.set("100%")
    #     self.scaling_optionemenu.grid(row=2, column=1, padx=20, pady=10)

    def create_confirm_cancel_button(self):
        self.confirm_button = ctk.CTkButton(self.setting_frame, text=self.app.get_text("confirm"),
                                            font=self.font, width=120, fg_color="#2563EB", text_color="white", hover_color="#1D4ED8",
                                            command=self.confirm_settings)
        self.confirm_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.return_button = ctk.CTkButton(self.setting_frame, text=self.app.get_text("return"),
                                           font=self.font, width=120, fg_color="gray70", text_color="white",
                                           hover_color="gray",
                                           command=self.cancel_settings)
        self.return_button.grid(row=3, column=1, padx=0, pady=10, sticky="ew")

    def confirm_settings(self):
        if self.language_var.get() == self.app.get_text(self.app.current_language):
            pass
        else:
            self.on_language_change(self.language_var.get())
        # if self.theme_var.get() == self.app.get_text(self.app.theme):
        #     pass
        # else:
        #     self.change_appearance_mode_event(self.theme_var.get())
        for widget in self.winfo_children():
            widget.grid_forget()
        self.app.system_settings.grid_remove()
        self.app.flow_frame.grid()
        self.app.flow_frame.tkraise()
        self.grab_release()

    def cancel_settings(self):
        for widget in self.winfo_children():
            widget.grid_forget()
        self.app.system_settings.grid_remove()
        # for widget in self.app.main_frame.winfo_children():
        #     widget.grid()
        self.app.flow_frame.grid()
        # self.app.create_top_section()
        # self.app.create_workflow_section()
        self.app.flow_frame.tkraise()
        self.grab_release()

    def on_language_change(self, language_value):
        # Dynamically generate the mapping based on the language list
        language = self.app.text_to_key(language_value)
        self.app.change_language(language)
        self.update_language()
        self.create_language_mode()
        self.app.update_language()

        # self.app.create_top_section()
        # self.app.create_workflow_section()
        # self.language_setting.set(self.app.get_text(self.app.current_language))

    def change_appearance_mode_event(self, new_appearance_mode: str):
        new_mode = self.theme_map[new_appearance_mode]
        # self.theme.set()
        ctk.set_appearance_mode(new_mode)
        self.app.theme = self.theme_var.get()

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def update_language(self):
        self.language_label.configure(text=self.app.get_text("ui_language"))
        # self.theme_label.configure(text=self.app.get_text("theme"))
        # self.theme_var.set(self.app.get_text(self.theme_map[self.theme.get()]))
        # self.theme.configure(values=[self.app.get_text("light"),
        #                              self.app.get_text("dark"),
        #                              self.app.get_text("system")])
        # self.theme_map = {self.app.translations[key]: key for key in ['dark', 'light', 'system']}
        # self.scaling_label.configure(text=self.app.get_text("ui_scaling"))
        self.confirm_button.configure(text=self.app.get_text("confirm"))
        self.return_button.configure(text=self.app.get_text("return"))
