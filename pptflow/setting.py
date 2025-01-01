from dataclasses import dataclass
import os


@dataclass
class Setting:
    # 1.Basic Settings
    # PPT settings
    start_page_num: int = None
    end_page_num: int = None
    ppt_path: str = None
    ppt_total_slides: int = None
    # Audio settings
    tts_service_provider: str = 'pyttsx3'
    tts_api_key: str = None
    tts_azure_api_key = "917b9e6040b4466caa22c6f62227af35"
    tts_speech_region = "eastasia"
    tts_voice_name: str = 'zh-CN-YunjianNeural'
    tts_voice_type: str = 'zh-CN-YunjianNeural (zh-CN, Male)'
    tts_voice_rate: str = '+0%'
    # Video settings
    video_format = 'MP4'
    video_width: int = 1280
    video_height: int = 720
    video_fps: int = 10
    video_path: str = None  # the output video path
    # Subtitle settings
    subtitle_width: int = None
    subtitle_height: int = None
    max_height_ratio: float = 0.1
    subtitle_font: str = 'Microsoft YaHei'
    subtitle_font_path: str = 'C:/Windows/Fonts/msyhbd.ttc'
    subtitle_font_size: int = 24
    subtitle_color: str = 'white'
    subtitle_stroke_color: str = 'black'  # subtitle outline color
    subtitle_stroke_width: int = 1  # subtitle outline width
    subtitle_text_length: int = 100

    # 2.Advanced Settings
    # Audio settings
    audio_format = 'MP3'
    audio_codec: str = 'aac'
    audio_local_cache_enabled: bool = True
    audio_path: str = None
    audio_language = 'en'
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
    language = 'en'  # Default: en
    # Storage Settings
    storage_path: str = None
    # Specify the full path to the PowerPoint presentation
    temp_dir = os.path.join(os.getcwd(), 'temp')
    image_dir_path = os.path.join(temp_dir, 'image')
    audio_dir_path = os.path.join(temp_dir, 'audio')


