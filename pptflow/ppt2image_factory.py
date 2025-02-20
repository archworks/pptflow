import platform


def get_ppt_to_image():
    os_name = platform.system()
    if os_name == "Windows":
        from .ppt2image_win import PptToImageWin
        return PptToImageWin()
    elif os_name == "Linux":
        from .ppt2image_linux import PptToImageLinux
        return PptToImageLinux()
    elif os_name == "Darwin":  # macOS
        from .ppt2image_mac import PptToImageMac
        return PptToImageMac()
    else:
        raise NotImplementedError(f"Unsupported OS: {os_name}")