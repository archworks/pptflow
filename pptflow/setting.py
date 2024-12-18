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
    tts_service_provider: str = 'azure'
    narration_language: str = 'zh-cn'
    narration_voice_name: str = 'zh-CN-YunjianNeural'
    narration_voice_speed: float = 1
    # Video settings
    video_format = 'MP4'
    video_width: int = 1280
    video_height: int = 720
    video_fps: int = 10
    video_path: str = None  # the output video path
    # Subtitle settings
    subtitle_font: str = 'Microsoft YaHei'
    subtitle_font_size: int = 24
    subtitle_color: str = 'white'
    subtitle_stroke_color: str = 'black'  # subtitle outline color
    subtitle_stroke_width: int = 1  # subtitle outline width

    # 2.Advanced Settings
    # Audio settings
    audio_format = 'MP3'
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
    language = 'en'  # Default: en
    # Storage Settings
    storage_path: str = None
    # Specify the full path to the PowerPoint presentation
    temp_dir = os.path.join(os.getcwd(), 'temp')
    image_dir_path = os.path.join(temp_dir, 'image')
    audio_dir_path = os.path.join(temp_dir, 'audio')



