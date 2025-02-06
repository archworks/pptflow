import os, sys, platform

# Add parent directory to the module search path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from dotenv import load_dotenv
load_dotenv()
from pptflow.config.setting import Setting
from pptflow.ppt2image_factory import get_ppt_to_image


test_path = os.path.join(parent_dir, "test")
ppt_path = os.path.join(test_path, "test-en.pptx")
image_dir_path = os.path.join(os.path.join(parent_dir, "temp"), "image")
setting = Setting()
ppt_to_image = get_ppt_to_image()
ppt_to_image.convert(ppt_path, setting)
