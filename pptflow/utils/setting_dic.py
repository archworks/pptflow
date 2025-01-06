# Author: Valley-e
# Date: 2024/12/16  
# Description:
import matplotlib.font_manager as fm
import asyncio
import sys
from pptflow.utils import mylogger

# Setup logger
logger = mylogger.get_logger(__name__)

# 兼容不同操作系统的事件循环
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# Get all installed fonts
def get_installed_fonts():
    fonts = fm.findSystemFonts(fontpaths=None, fontext='ttf')
    font_dict = {}
    for font in fonts:
        try:
            font_name = fm.FontProperties(fname=font).get_name()
            font_dict[font_name] = font
        except Exception as e:
            logger.warning(f"Error processing font {font}: {e}")
    sorted_font_dict = dict(sorted(font_dict.items()))  # Sort the dictionary by keys
    logger.info("Installed fonts have been loaded")
    return sorted_font_dict


# tts setting
# tts_service_providers = ["azure", "edge-tts", "coqui-tts", "pyttsx3"]
tts_service_providers = ["azure", "pyttsx3"]
tts_speech_regions = ["eastasia", "northeurope", "southeastasia", "westus"]
tts_speech_voices = []
# Video settings
video_formats = ['MP4', 'AVI', 'MKV']
video_codecs = ['H.264', 'H.265', 'VP9']
video_sizes = ["1280x720", "1920x1080", "854x480"]
video_fps = ["10fps", "30fps", "24fps"]
video_processing_threads = ["1", "2", "4", "8", "16"]
# Audio settings
audio_formats = ['MP3', 'WAV', 'AAC']
audio_codecs = ['AAC', 'MP3', 'WAV']
audio_bitrates = ['128kbps', '256kbps', '320kbps']
audio_voice_type = ["zh-CN-YunjianNeural", "zh-CN-XiaoxiaoNeural"]
audio_speeds = ["1.0x", "0.8x", "1.2x", "1.5x"]
audio_languages = ['en', 'zh']
# Subtitle settings
subtitle_font_dict = get_installed_fonts()
font_colors = ['white', 'black', 'red', 'blue', 'yellow', 'green']
border_colors = ['black', 'white', 'no_color']
border_widths = ["0", "1", "2", "3", "4"]
# Language Settings
language_mode = ['en', 'zh']

print(get_installed_fonts())