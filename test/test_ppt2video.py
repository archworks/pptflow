import os,sys
# 获取所在目录的父级目录
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# 将父级目录添加到模块搜索路径
sys.path.append(parent_dir)
import pptflow.ppt2video as ppt2video
from pptflow.setting import Setting

test_path = os.path.join(parent_dir, "test")
ppt_path = os.path.join(test_path, 'test.pptx')
ppt2video.ppt_to_video(ppt_path, Setting())