# Author: Valley-e
# Date: 2024/12/16  
# Description:
import asyncio
import sys
from pptflow.utils import mylogger

# Setup logger
logger = mylogger.get_logger(__name__)

# 兼容不同操作系统的事件循环
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# tts setting
# tts_service_providers = ["azure", "edge-tts", "coqui-tts", "pyttsx3"]
tts_service_providers = ["azure", "pyttsx3", "baidu"]
tts_speech_regions = ["eastasia", "northeurope", "southeastasia", "westus"]
tts_speech_voices = ["en-US-EmmaNeural"]
# Video settings
video_formats = ['MP4', 'AVI', 'MOV']
video_codecs = ['H.264', 'H.265', 'VP9']
video_sizes = ["1280x720", "1920x1080", "2560x1440", "3840x2160","720x480"]
video_fps = ["10fps", "30fps", "24fps"]
video_processing_threads = ["1", "2", "4", "8", "16"]
# Audio settings
# 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
# 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美
baidu_voice_persons: dict = {
    0: "度小美",
    1: "度小宇",
    3: "度逍遥",
    4: "度丫丫",
    5: "度小娇",
    103: "度米朵",
    106: "度博文",
    110: "度小童",
    111: "度小萌",
 }
audio_formats = ['MP3', 'WAV', 'AAC']
audio_codecs = ['AAC', 'MP3', 'WAV']
audio_bitrates = ['128kbps', '256kbps', '320kbps']
audio_voice_type = ["zh-CN-YunjianNeural", "zh-CN-XiaoxiaoNeural"]
audio_speeds = ["1.0x", "0.8x", "1.2x", "1.5x"]
audio_languages = ['en', 'zh']
# Subtitle settings
subtitle_lengths = ["20", "35", "50", "70"]
subtitle_font_dict = {}
font_colors = ['white', 'black', 'red', 'blue', 'yellow', 'green']
border_colors = ['black', 'white', 'no_color']
border_widths = ["0", "1", "2", "3", "4"]
# Language Settings
language_mode = ['en', 'zh']
