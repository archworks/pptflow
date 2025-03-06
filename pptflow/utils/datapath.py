# Author: Valley-e
# Date: 2025/2/27  
# Description:
import os
import pathlib
import sys
from dotenv import load_dotenv
import os


def get_father_dir():
    home = pathlib.Path.home()
    system_paths = {
        'win32': home / 'AppData/Roaming',
        'linux': home / '.local/share',
        'darwin': home / 'Library/Application Support'
    }

    # 修改原来的data_path定义
    data_path = system_paths[sys.platform]
    if os.getenv('ENV') == 'dev':
        # father_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        father_dir = os.getcwd()
    else:
        father_dir = os.path.join(data_path, 'pptflow')
    return father_dir


def get_absolute_data_path(path_name: str = ''):
    if path_name == '' or path_name is None:
        return get_father_dir()
    else:
        return os.path.join(get_father_dir(), path_name)


def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):  # 打包后运行环境
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath(""), relative_path)


def get_install_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)  # 安装目录
    else:  # 开发模式
        return os.path.dirname(os.path.abspath(__file__))


env_path = os.path.join(get_absolute_data_path(), ".env")
init_content = """
# Configuration file
# Format: key=value
# Example:
# TTS_SERVICE_PROVIDER=kokoro
# Azure TTS
# TTS_AZURE_SPEECH_KEY=xxxx
# TTS_AZURE_SPEECH_REGION=eastasia
# Kokoro TTS
# KOKORO_MODEL_PATH=D:/workspace/pycharm/pptflow/model/kokoro-v1.0.fp16.onnx
# KOKORO_VOICE_PATH=D:/workspace/pycharm/pptflow/model/voices-v1.0.bin
# BAIDU_APP_ID=xxxx
# BAIDU_API_KEY=xxxx
# BAIDU_SECRET_KEY=xxxx
"""
# 创建目录（如果不存在）
os.makedirs(os.path.dirname(env_path), exist_ok=True)
try:
    with open(env_path, "x") as f:
        f.write(init_content)
        print("The file .env has been created successfully")

except FileExistsError:
    print("The file .env already exists. Skip creation")

load_dotenv(env_path, encoding="utf-8")


if __name__ == '__main__':
    print(get_absolute_data_path('log'))
