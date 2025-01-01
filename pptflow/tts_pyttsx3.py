# Author: Valley-e
# Date: 2024/12/29  
# Description:
import pyttsx3
import asyncio
from utils import mylogger

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)


async def tts(text, file_path, setting):
    try:
        # 初始化 pyttsx3 引擎
        engine = pyttsx3.init()

        # 设置语速（可选）
        rate = engine.getProperty('rate')  # 获取当前语速
        engine.setProperty('rate', (rate - 50))  # 设置为比默认更慢

        # 设置音量（可选）
        volume = engine.getProperty('volume')  # 获取当前音量
        engine.setProperty('volume', 1)  # 设置为最大音量

        # 设置语音（可选）
        voices = engine.getProperty('voices')
        # 列出所有语音
        # for voice in voices:
        #     print(f"Voice: {voice.name}, Language: {voice.languages}")

        # 设置语音
        if setting.audio_language == 'zh':
            voice = voices[0].id
        else:
            voice = voices[1].id
        # voices[0]为中文语言，voices[1]为英文语言
        engine.setProperty('voice', voice)  # 设置为女性声音

        # 将文本转换为语音并播放
        # engine.say(text)
        # 保存为音频文件（可选）
        engine.save_to_file(text=text, filename=file_path, name=voices[0].name)
        # 等待语音生成完成
        engine.runAndWait()
    except Exception as e:
        logger.error(f"Error occurred during TTS: {e}", exc_info=True)

