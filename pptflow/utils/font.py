# Author: Valley-e
# Date: 2025/1/8  
# Description:
from pptflow.utils import mylogger
import json
import os
import platform

logger = mylogger.get_logger(__name__)

# Default font file name
FONT_FILE_NAME = 'installed_fonts.json'


def get_platform_based_font_file():
    """根据当前操作系统返回不同的字体 JSON 文件路径"""
    current_platform = platform.system().lower()
    if current_platform == 'windows':
        return 'installed_fonts_windows.json'
    elif current_platform == 'darwin':  # macOS
        return 'installed_fonts_macos.json'
    else:
        logger.warning(f"Unsupported platform: {current_platform}. Using default file name.")
        return FONT_FILE_NAME


# 获取所有已安装的字体
def get_installed_fonts():
    import matplotlib.font_manager as fm
    logger.info("Loaded matplotlib")
    """获取所有已安装的字体并返回字典"""
    fonts = fm.findSystemFonts(fontpaths=None, fontext='ttf')
    font_dict = {}
    for font in fonts:
        try:
            font_name = fm.FontProperties(fname=font).get_name()
            font_dict[font_name] = font
        except Exception as e:
            logger.warning(f"Error processing font {font}: {e}")
    sorted_font_dict = dict(sorted(font_dict.items()))  # 按键排序字典
    return sorted_font_dict


def save_fonts_to_json(font_dict, file_path=FONT_FILE_NAME):
    """将字体信息保存到 JSON 文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(font_dict, f, ensure_ascii=False, indent=4)
    logger.info(f"Fonts have been saved to {file_path}")


def load_fonts_from_json(file_path=FONT_FILE_NAME):
    """从 JSON 文件加载字体信息"""
    font_dir = os.path.join(os.getcwd(), 'fonts')
    os.makedirs(font_dir, exist_ok=True)
    file_path = os.path.join(font_dir, file_path)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            font_dict = json.load(f)
        logger.info(f"Fonts have been loaded from {file_path}")
        return font_dict
    else:
        logger.info(f"Font file {file_path} does not exist, fetching fonts...")
        font_dict = get_installed_fonts()
        save_fonts_to_json(font_dict, file_path)
        return font_dict


def get_or_load_fonts():
    """获取当前操作系统的字体文件，若文件不存在则从系统中获取并保存"""
    platform_font_file = get_platform_based_font_file()
    return load_fonts_from_json(platform_font_file)


def find_font_path(font_name):
    """根据字体名称搜索匹配的字体路径"""
    for font, font_path in get_or_load_fonts().items():
        if font_name.lower() in font.lower():  # 字体名称匹配
            return font_path
    return None


if __name__ == '__main__':
    # 示例：查找 "Arial" 字体的路径
    font_name = "Arial"
    font_path = find_font_path(font_name)

    if font_path:
        print(f"字体 '{font_name}' 的路径是: {font_path}")
    else:
        print(f"未找到字体 '{font_name}'")
