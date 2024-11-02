import os, sys

# 获取所在目录的父级目录
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# 将父级目录添加到模块搜索路径
sys.path.append(parent_dir)
from pptflow.ppt2image_win import ppt_to_image
from dotenv import load_dotenv

load_dotenv()


test_path = os.path.join(parent_dir, "test")
ppt_path = os.path.join(test_path, "test.pptx")
image_dir_path = os.path.join(os.path.join(parent_dir, "temp"), "image")
ppt_to_image(ppt_path, image_dir_path)
