# Author: Valley-e
# Date: 2024/12/29  
# Description:
import pyttsx3
from pptflow.utils import mylogger
from .tts_service import TtsService
from ..config.setting import Setting
import sys

class Pyttsx3TtsService(TtsService):
    logger = mylogger.get_logger(__name__)

    async def tts(self, text: str, output_audio_filename: str, setting: Setting):
        self.logger.info(f"Using pyttsx3")
        try:
            # 初始化 pyttsx3 引擎
            engine = pyttsx3.init()

            # 设置语速（可选）
            # rate = engine.getProperty('rate')  # 获取当前语速
            # logger.info(f"Current Rate: {rate}")
            engine.setProperty('rate', setting.pytts_voice_rate)

            # 设置音量（可选）
            volume = engine.getProperty('volume')  # 获取当前音量
            engine.setProperty('volume', 1)  # 设置为最大音量

            # 设置语音（可选）
            voices = engine.getProperty('voices')
            # 列出所有语音
            # 打印所有语音信息
            # for voice in voices:
            #     logger.info(voice)
            # logger.info(f"setting.audio_language: {setting.audio_language}")
            voice = voices[0]
            if self.is_chinese(text):
                self.logger.info(f"Chinese text detected, using Chinese voice")
                voice = self.get_chinese_voices(voices)
            # voices[0]为中文语言，voices[1]为英文语言
            engine.setProperty('voice', voice.id)  # 设置为女性声音

            # 将文本转换为语音并播放
            # engine.say(text)
            # 保存为音频文件（可选）
            engine.save_to_file(text=text, filename=output_audio_filename, name=voice.name)
            # 等待语音生成完成
            engine.runAndWait()
        except Exception as e:
            self.logger.error(f"Error occurred during TTS: {e}", exc_info=True)

    def get_voice_list(self, setting: Setting = None):
        return []

    def is_chinese(self, text):
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False


    def get_chinese_voices(self, voices):
        # 判断操作系统
        if sys.platform == 'win32':
            return voices[0]
        elif sys.platform == 'darwin':
            language = 'zh_CN'
            for voice in voices:
                if voice.languages and voice.languages[0] == language:
                    return voice
