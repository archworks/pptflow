import os,sys
# Add parent directory to the module search path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from dotenv import load_dotenv
load_dotenv()
from pptflow.clip2video import create_video_from_images_and_audio
from pptflow.config.setting import Setting


test_path = os.path.join(parent_dir, "test")
ppt_path = os.path.join(test_path, 'test.pptx')
setting = Setting()
setting.video_path = os.path.join(os.path.join(parent_dir, "temp"), "test.mp4")
create_video_from_images_and_audio(ppt_path, setting)