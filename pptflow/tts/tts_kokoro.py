# Author: Valley-e
# Date: 2025/2/24  
# Description:
from pptflow.utils import mylogger, datapath
import soundfile as sf
from kokoro_onnx import Kokoro
import numpy as np
import random
from pptflow.config.setting import Setting
from model.download_model import check_and_download
import asyncio
from pptflow.tts.tts_service import TtsService
import os
logger = mylogger.get_logger(__name__)


class KokoroTtsService(TtsService):
    module_dir = datapath.resource_path('model')

    async def tts(self, text: str, output_audio_filename: str, setting: Setting):
        model_path = os.getenv("KOKORO_MODEL_PATH", os.path.join(self.module_dir, setting.kokoro_module))
        voice_path = os.getenv("KOKORO_VOICE_PATH", os.path.join(self.module_dir, setting.kokoro_voice_file))
        # 检查并自动下载模型文件
        if not check_and_download(model_path, setting.kokoro_module):
            raise FileNotFoundError("模型文件下载失败，请检查网络连接")

        # 检查并自动下载语音文件
        if not check_and_download(voice_path, setting.kokoro_voice_file):
            raise FileNotFoundError("语音文件下载失败，请检查网络连接")
        kokoro = Kokoro(model_path, voice_path)
        logger.info("Using Kokoro TTS")
        samples, sample_rate = kokoro.create(
            text,
            voice=setting.kokoro_voice_name,
            speed=1.0,
            lang="en-us",
        )
        audio = []
        audio.append(samples)
        # Add random silence after each sentence
        if text and text.strip()[-1] in {'.', ',', ';', '?', '!'}:
            audio.append(random_pause(sample_rate))
        # Concatenate all audio parts
        audio = np.concatenate(audio)

        # Save the generated audio to file
        sf.write(output_audio_filename, audio, sample_rate)
        logger.info(f"Created {output_audio_filename}")

    def get_voice_list(self, setting: Setting = None):
        kokoro = Kokoro(os.path.join(self.module_dir, setting.kokoro_module),
                        os.path.join(self.module_dir, setting.kokoro_voice_file))
        voice_list = [voice for voice in kokoro.get_voices() if voice.split("_")[0] in ["af", "am", "bf", "bm"]]
        logger.info(f"Voices: {voice_list}")
        return voice_list


def random_pause(sample_rate, min_duration=0.5, max_duration=2.0):
    silence_duration = random.uniform(min_duration, max_duration)
    silence = np.zeros(int(silence_duration * sample_rate))
    return silence


def filter_names(lang_code, gender_code, all_names):
    prefix = f"{lang_code}{gender_code}_"
    return [name.split('_')[1] for name in all_names if name.startswith(prefix)]


if __name__ == '__main__':
    setting = Setting()
    tts = KokoroTtsService()
    asyncio.run(tts.tts("你好，世界！", "output.mp3", setting))
