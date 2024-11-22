from dataclasses import dataclass
import os


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
    subtitle_font: str = 'Microsoft-YaHei-&-Microsoft-YaHei-UI'
    subtitle_fontsize: int = 24
    subtitle_color: str = 'white'
    subtitle_stroke_color: str = 'black'

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
