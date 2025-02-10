from .setting import Setting


def get_default_setting(os_name: str = 'Windows', language: str = 'en'):
    setting = Setting()
    get_default_subtitle_path(setting, os_name, language)
    get_default_subtitle_length(setting)
    get_default_tts_settings(setting, tts_service_provider='pyttsx3')

    return setting


def get_default_subtitle_path(setting: Setting, os_name: str = 'Windows', language: str = 'en'):
    if os_name == "Windows":
        if language == 'zh':
            setting.subtitle_font_name = 'STSong'
            setting.subtitle_font_path = 'C:/Windows/Fonts/STSONG.TTF'
        elif language == 'en':
            setting.subtitle_font_name = 'Microsoft YaHei'
            setting.subtitle_font_path = 'C:/Windows/Fonts/msyh.ttc'
    elif os_name == "Linux":
        if language == 'zh':
            setting.subtitle_font_name = 'WenQuanYi Zen Hei'
            setting.subtitle_font_path = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
        elif language == 'en':
            setting.subtitle_font_name = 'DejaVu Sans'
            setting.subtitle_font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    elif os_name == "Darwin":
        if language == 'zh':
            setting.subtitle_font_name = 'Songti SC'
            setting.subtitle_font_path = '/System/Library/Fonts/Supplemental/Songti.ttc'
        elif language == 'en':
            setting.subtitle_font_name = 'Arial'
            setting.subtitle_font_path = '/System/Library/Fonts/Supplemental/Arial.ttf'
    else:
        raise NotImplementedError(f"Unsupported OS: {os_name}")


def get_default_subtitle_length(setting: Setting):
    if setting.language == 'en':
        setting.subtitle_length = 70
    elif setting.language == 'zh':
        setting.subtitle_length = 25
    else:
        pass


def get_default_tts_settings(setting: Setting, tts_service_provider: str = 'pyttsx3'):
    if tts_service_provider == 'pyttsx3':
        setting.tts_service_provider = 'pyttsx3'
        setting.pytts_voice_rate = 150
    elif tts_service_provider == 'azure':
        setting.tts_speech_region = "eastasia"
        setting.tts_azure_api_key = "917b9e6040b4466caa22c6f62227af35"
        setting.tts_voice_name = 'zh-CN-YunjianNeural'
        setting.tts_voice_type = 'zh-CN-YunjianNeural (zh-CN, Male)'
    elif tts_service_provider == 'edge_tts':
        setting.tts_voice_rate = '+0%'
    else:
        raise NotImplementedError(f"Unsupported TTS service provider: {tts_service_provider}")