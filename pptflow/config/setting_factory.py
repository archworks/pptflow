from .setting import Setting


def get_defalut_setting(os_name: str = 'Windows', language: str = 'en'):
    setting = Setting()
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
    ## 这里可以增加tts默认值的设置，比如tts_azure_api_key等，建议从环境变量.env中读取
    return setting