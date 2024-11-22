import os,sys
# 获取所在目录的父级目录
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# 将父级目录添加到模块搜索路径
sys.path.append(parent_dir)
from dotenv import load_dotenv
load_dotenv()

from pptflow.clip2video import create_video_from_images_and_audio
from pptflow.setting import Setting


test_path = os.path.join(parent_dir, "test")
ppt_path = os.path.join(test_path, 'test.pptx')
setting = Setting()
create_video_from_images_and_audio(ppt_path, setting)