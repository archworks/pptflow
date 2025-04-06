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
    external_notes_path: str = None  # 新增外部笔记文件路径
    has_notes: bool = False
    images_name: str = "黑灰白色极简风年度汇报述职通用ppt演示文稿"
    # Audio settings
    tts_service_provider: str = None
    tts_api_key: str = None
    tts_speech_region = 'eastasia'
    tts_voice_name: str = 'en-US-EmmaNeural'
    tts_voice_type: str = 'en-US-EmmaNeural (en-US, Female)'
    tts_voice_rate: str = None
    pytts_voice_rate: int = None
    # Baidu TTS settings
    baidu_app_id: str = '117675325'
    baidu_api_key: str = 'XAzMnN5M5RHrkv6QUYbmeUmS'
    baidu_secret_key: str = 'cmYU6NfDS8ZdDnju7Xq2lsPj1GW6pJHl'
    per: int = 1
    vol: int = 5
    spd: int = 5
    pit: int = 5
    kokoro_module: str = 'kokoro-v1.0.fp16.onnx'
    kokoro_voice_file: str = 'voices-v1.0.bin'
    kokoro_voice_name: str = 'af_heart'
    # CosyVoice TTS
    cosyvoice_role = '中文女'  # 预置语音角色 "中文男|中文女|英文男|英文女|日语男|韩语女|粤语女" 选其一
    # Video settings
    video_format = 'MP4'
    video_width: int = 1280
    video_height: int = 720
    video_fps: int = 10
    video_path: str = None  # the output video path
    random_pause_enabled: bool = True  # 是否随机插入暂停
    min_pause_duration: int = 0.5
    max_pause_duration: int = 2.0
    estimate_duration_enabled: bool = True  # 是否使用计算时长
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
    subtitle_polishing_enabled: bool = False
    subtitle_style: str = 'presentation'

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
