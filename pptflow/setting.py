from dataclasses import dataclass

@dataclass
class Setting:
    # 1.Basic Settings
    ## PPT settings
    ppt_start_page_num: int = None
    ppt_end_page_num: int = None
    ## Audio settings
    tts_service_provider: str = 'azure'
    narration_language: str = 'zh-cn'
    narration_voice_name: str = 'zh-CN-YunjianNeural'
    narration_voice_speed: int = 1
    ## Video settings
    video_format: str = 'mp4'
    video_width: int = 1280
    video_height: int = 720
    video_frame_rate: int = 10
    ## Subtitle settings
    subtitle_font: str = 'Microsoft-YaHei-&-Microsoft-YaHei-UI'
    subtitle_fontsize: int = 24
    subtitle_color: str = 'white'
    subtitle_stroke_color: str = 'black'
    
    # 2.Advanced Settings
    # Audio settings
    audio_format: str = 'mp3'
    audio_codec: str = 'aac'
    audio_local_cache: bool = True
    ## Video settings
    video_codec: str = 'libx264'
    video_processing_threads: int = 4