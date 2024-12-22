# Author: Valley-e
# Date: 2024/12/16  
# Description:
import matplotlib.font_manager as fm
import edge_tts
import asyncio
import json
import sys
import os
from utils import mylogger

# Setup logger
logger = mylogger.get_logger(__name__)

# 兼容不同操作系统的事件循环
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def list_voices():
    # List all voices
    voices = await edge_tts.list_voices()
    # Get the key information
    voice_list = [{"Locale": voice["Locale"], "Gender": voice["Gender"], "ShortName": voice["ShortName"]} for voice in voices]
    with open("voice_list.json", "w", encoding="utf-8") as file:
        json.dump(voice_list, file, ensure_ascii=False, indent=4)
        logger.info("Voice list has been saved to voice_list.json")


def get_voice_list():
    if not os.path.exists("voice_list.json"):
        asyncio.run(list_voices())
    with open("voice_list.json", "r", encoding="utf-8") as file:
        voice_list = json.load(file)
        logger.info("Voice list has been loaded from voice_list.json")
    return [f'{voice["ShortName"]} ({voice["Locale"]}, {voice["Gender"]})' for voice in voice_list]


# Get all installed fonts
def get_installed_fonts():
    fonts = fm.findSystemFonts(fontpaths=None, fontext='ttf')
    font_dict = {fm.FontProperties(fname=font).get_name(): font for font in fonts}
    sorted_font_dict = dict(sorted(font_dict.items()))  # Sort the dictionary by keys
    logger.info("Installed fonts have been loaded")
    return sorted_font_dict


# tts setting
tts_service_providers = ["AZURE", "xunfei", "edge-tts"]
tts_speech_regions = ["eastasia", "northeurope", "southeastasia", "westus"]
tts_speech_voices = get_voice_list()
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
audio_languages = ['zh', 'en', 'jp']
# Subtitle settings
subtitle_font_dict = get_installed_fonts()
font_colors = ['white', 'black', 'red', 'blue', 'yellow', 'green']
border_colors = ['black', 'white', 'no_color']
border_widths = ["0", "1", "2", "3", "4"]
# Language Settings
language_mode = ['en', 'zh']
