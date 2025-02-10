import platform
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
    pytts_voice_rate: int = 150
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
    win_subtitle_font: str = 'Microsoft YaHei'  # @金枫 注意以subtitle_font_path为准，需要重构
    mac_subtitle_font: str = 'Times New Roman'
    subtitle_font_name: str = None
    subtitle_font_path: str = None
    subtitle_font_size: int = 28
    subtitle_color: str = 'white'
    subtitle_stroke_color: str = 'black'  # subtitle outline color
    subtitle_stroke_width: int = 1  # subtitle outline width
    subtitle_length: int = 100

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

    def __init__(self, os_name: str = 'Windows'):
        if os_name == "Windows":
            if self.language == 'zh':
                self.subtitle_font_name = 'STSong'
                self.subtitle_font_path = 'C:/Windows/Fonts/STSONG.TTF'
            elif self.language == 'en':
                self.subtitle_font_name = 'Microsoft YaHei'
                self.subtitle_font_path = 'C:/Windows/Fonts/msyh.ttc'
        elif os_name == "Linux":
            if self.language == 'zh':
                self.subtitle_font_name = 'WenQuanYi Zen Hei'
                self.subtitle_font_path = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
            elif self.language == 'en':
                self.subtitle_font_name = 'DejaVu Sans'
                self.subtitle_font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
            # self.subtitle_font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
        elif os_name == "Darwin":
            if self.language == 'zh':
                self.subtitle_font_name = 'Songti SC'
                self.subtitle_font_path = '/System/Library/Fonts/Supplemental/Songti.ttc'
            elif self.language == 'en':
                self.subtitle_font_name = 'Arial'
                self.subtitle_font_path = '/System/Library/Fonts/Supplemental/Arial.ttf'
        else:
            raise NotImplementedError(f"Unsupported OS: {os_name}")


if __name__ == '__main__':
    setting = Setting(os_name="Linux")
    print(setting.subtitle_font_path)
    print(setting.subtitle_font_name)
