# Author: Valley-e
# Date: 2024/12/16  
# Description:
import matplotlib.font_manager as fm
import os


# Get all installed fonts
def get_installed_fonts():
    fonts = fm.findSystemFonts(fontpaths=None, fontext='ttf')
    font_dict = {fm.FontProperties(fname=font).get_name(): font for font in fonts}
    sorted_font_dict = dict(sorted(font_dict.items()))  # Sort the dictionary by keys
    return sorted_font_dict


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
tts_servers = ["azure", "xunfei"]
audio_voice_type = ["zh-CN-YunjianNeural", "xxxx"]
audio_speeds = ["1.0x", "0.8x", "1.2x", "1.5x"]
audio_languages = ['zh', 'en', 'jp']
# Subtitle settings
subtitle_font_dict = get_installed_fonts()
font_colors = ['white', 'black', 'red', 'blue', 'yellow', 'green']
border_colors = ['black', 'white', 'no_color']
border_widths = ["0", "1", "2", "3", "4"]
# Language Settings
language_mode = ['en', 'zh']
