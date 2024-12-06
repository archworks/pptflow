from dataclasses import dataclass
import matplotlib.font_manager as fm
import os


# Get all installed fonts
def get_installed_fonts():
    fonts = fm.findSystemFonts(fontpaths=None, fontext='ttf')
    font_dict = {fm.FontProperties(fname=font).get_name(): font for font in fonts}
    sorted_font_dict = dict(sorted(font_dict.items()))  # Sort the dictionary by keys
    return sorted_font_dict


@dataclass
class Setting:
    # 1.Basic Settings
    # PPT settings
    start_page_num: int = None
    end_page_num: int = None
    # Audio settings
    tts_service_provider: str = 'azure'
    narration_language: str = 'zh-cn'
    narration_voice_name: str = 'zh-CN-YunjianNeural'
    narration_voice_speed: int = 1
    # Video settings
    video_formats = ['MP4', 'AVI', 'MKV']
    video_width: int = 1280
    video_height: int = 720
    video_frame_rate: int = 10
    video_path: str = None  # the output video path
    # Subtitle settings
    subtitle_font: str = 'C:/Windows/Fonts/msyh.ttc'
    subtitle_font_dict = get_installed_fonts()
    subtitle_font_size: int = 24
    subtitle_color: str = 'white'
    subtitle_stroke_color: str = 'black'
    subtitle_stroke_width: float = 1

    # 2.Advanced Settings
    # Audio settings
    audio_formats = ['MP3', 'WAV', 'AAC']
    audio_codec: str = 'aac'
    audio_local_cache_enabled: bool = True
    audio_path: str = None
    # Video settings
    video_codec: str = 'libx264'
    video_processing_threads: int = 4

    # 3.Personal Settings
    # Account Settings
    account_name: str = None
    account_key: str = None
    account_email: str = None

    # 4.System Settings
    # Language Settings
    language_mode = ['en', 'zh']  # Default: en
    # Storage Settings
    storage_path: str = None
    # Specify the full path to the PowerPoint presentation
    temp_dir = os.path.join(os.getcwd(), 'temp')
    image_dir_path = os.path.join(temp_dir, 'image')
    audio_dir_path = os.path.join(temp_dir, 'audio')



