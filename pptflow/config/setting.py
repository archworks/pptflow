from dataclasses import dataclass
import os
from pptflow.utils.datapath import get_absolute_data_path


@dataclass
class Setting:
    # 1.Basic Settings
    # Default language: en
    language = 'en'
    # PPT settings
    ppt_total_slides: int = None
    # Audio settings
    tts_service_provider: str = None
    tts_api_key: str = None
    tts_speech_region = 'eastasia'
    tts_voice_name: str = 'en-US-EmmaNeural'
    tts_voice_type: str = 'en-US-EmmaNeural (en-US, Female)'
    tts_voice_rate: str = None
    pytts_voice_rate: int = None
    # Baidu TTS settings
    baidu_app_id: str = None
    baidu_api_key: str = None
    baidu_secret_key: str = None
    per: int = 0
    vol: int = 5
    spd: int = 5
    pit: int = 5
    kokoro_module: str = 'kokoro-v1.0.fp16.onnx'
    kokoro_voice_file: str = 'voices-v1.0.bin'
    kokoro_voice_name: str = 'af_heart'
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
    subtitle_font_name: str = None
    subtitle_font_path: str = None
    subtitle_font_size: int = 28
    subtitle_color: str = 'white'
    subtitle_stroke_color: str = 'black'  # subtitle outline color
    subtitle_stroke_width: int = 1  # subtitle outline width
    subtitle_length: int = None

    # 2.Advanced Settings
    # PPT settings
    start_page_num: int = None
    end_page_num: int = None
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

    # Specify the full path to the PowerPoint presentation
    temp_dir = get_absolute_data_path('temp')
    image_dir_path = os.path.join(temp_dir, 'image')
    audio_dir_path = os.path.join(temp_dir, 'audio')
