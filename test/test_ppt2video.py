import os,sys
# 获取所在目录的父级目录
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# 将父级目录添加到模块搜索路径
sys.path.append(parent_dir)
import pptflow.ppt2video as ppt2video

current_dir = os.getcwd()
asset_path = os.path.join(current_dir, "test")
ppt_path = os.path.join(asset_path, 'test.pptx')
video_path = os.path.join(asset_path, "test.mp4")
ppt2video.process(ppt_path, video_path)