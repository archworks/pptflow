import os
from dotenv import load_dotenv
from pptflow.config.setting import Setting

load_dotenv()


def get_default_setting(os_name: str = 'Windows', language: str = 'en', tts_service_provider: str = 'kokoro'):
    setting = Setting()
    setting.language = language
    get_default_subtitle_path(setting, os_name, language)
    get_default_subtitle_length(setting)
    get_default_tts_settings(setting, tts_service_provider=tts_service_provider)

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
        setting.subtitle_length = 35
    else:
        pass


def get_default_tts_settings(setting: Setting, tts_service_provider: str = 'kokoro'):
    if tts_service_provider == 'kokoro':
        setting.tts_service_provider = 'kokoro'
    elif tts_service_provider == 'azure':
        setting.tts_service_provider = 'azure'
        setting.tts_speech_region = 'eastasia'
        setting.tts_api_key = os.getenv("TTS_AZURE_SPEECH_KEY")
    else:
        raise NotImplementedError(f"Unsupported TTS service provider: {tts_service_provider}")


if __name__ == '__main__':
    setting = get_default_setting(os_name='Windows', language='zh', tts_service_provider='azure')
    print(setting.tts_api_key)
