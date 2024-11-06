import pptflow.ppt2video as ppt2video
from pptflow.setting import Setting

ppt_path = input("请输入ppt路径: ")
setting = Setting()
ppt2video.process(ppt_path, setting=setting)