import os,sys

# Add parent directory to the module search path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import pptflow.ppt2video as ppt2video
from pptflow.config.setting import Setting
from pptflow.tts.tts_pyttsx3 import tts

test_path = os.path.join(parent_dir, "test")
ppt_path = os.path.join(test_path, 'test.pptx')
ppt2video.ppt_to_video(tts, ppt_path, Setting())