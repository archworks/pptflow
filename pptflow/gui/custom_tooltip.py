# Author: Valley-e
# Date: 2025/1/16  
# Description:
import customtkinter as ctk


class CustomTooltip:
    def __init__(self, widget, text, font=("Arial", 12, "bold"), delay=100):
        self.widget = widget
        self.text = text
        self.font = font
        self.tooltip = None
        self.after_id = None
        self.delay = delay  # 延迟显示时间

        self.widget.bind("<Enter>", self.schedule_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        self.widget.bind("<Motion>", self.track_mouse)  # 监听鼠标移动
        self.widget.bind("<FocusOut>", self.hide_tooltip)  # 失去焦点时隐藏

    def schedule_tooltip(self, event=None):
        """ 在指定时间后显示 tooltip """
        self.after_id = self.widget.after(self.delay, self.show_tooltip)

    def show_tooltip(self, event=None):
        """ 显示 tooltip """
        if self.tooltip:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + self.widget.winfo_width() // 2 - 100
        y = self.widget.winfo_rooty() - 30  # 组件上方，留点空间

        self.tooltip = ctk.CTkToplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        # self.tooltip.wm_attributes("-topmost", True)  # 确保始终在最上层
        # self.tooltip.wm_attributes("-alpha", 0.85)  # 85% 透明度
        self.tooltip.geometry(f"+{x}+{y}")

        label = ctk.CTkLabel(self.tooltip, text=self.text, font=self.font, padx=5, pady=3, fg_color="transparent")
        label.pack()

    def hide_tooltip(self, event=None):
        """ 隐藏 tooltip """
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

    def track_mouse(self, event):
        """ 监听鼠标是否仍在组件内，否则隐藏 tooltip """
        if not (0 <= event.x <= self.widget.winfo_width() and 0 <= event.y <= self.widget.winfo_height()):
            self.hide_tooltip()


if __name__ == '__main__':
    root = ctk.CTk()
    root.geometry("400x200")

    label = ctk.CTkLabel(root, text="Hover over me!", font=ctk.CTkFont(size=14, weight="bold"))
    label.pack(pady=50)

    # 绑定自定义 tooltip
    CustomTooltip(label, "This is a custom tooltip!", font=("Arial", 14, "bold"))

    root.mainloop()
