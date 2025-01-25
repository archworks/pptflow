import platform
from .ppt2image_win import PptToImageWin
from .ppt2image_linux import PptToImageLinux
from .ppt2image_mac import PptToImageMac

def get_ppt_to_image():
    os_name = platform.system()
    if os_name == "Windows":
        return PptToImageWin()
    elif os_name == "Linux":
        return PptToImageLinux()
    elif os_name == "Darwin":  # macOS
        return PptToImageMac()
    else:
        raise NotImplementedError(f"Unsupported OS: {os_name}")