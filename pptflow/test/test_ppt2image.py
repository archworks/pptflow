import os, sys, platform

# 获取所在目录的父级目录
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
# 将父级目录添加到模块搜索路径
sys.path.append(parent_dir)
from dotenv import load_dotenv
load_dotenv()
os_name = platform.system()
if os_name == "Windows":
    from pptflow.ppt2image_win import ppt_to_image
elif os_name == "Linux":
    from pptflow.ppt2image_linux import ppt_to_image
elif os_name == "Darwin":  # macOS
    from pptflow.ppt2image_mac import ppt_to_image
else:
    raise NotImplementedError(f"不支持的操作系统: {os_name}")
from pptflow.config.setting import Setting

test_path = os.path.join(parent_dir, "test")
ppt_path = os.path.join(test_path, "test.pptx")
image_dir_path = os.path.join(os.path.join(parent_dir, "temp"), "image")
ppt_to_image(ppt_path, image_dir_path, Setting())
