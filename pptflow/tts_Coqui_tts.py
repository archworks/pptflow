# Author: Valley-e
# Date: 2024/12/29  
# Description:
from TTS.api import TTS
import warnings
import subprocess
import os
from utils import mylogger

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)

# 忽略 FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)


# only support English text
async def tts(text, file_path, setting):
    try:
        # 加载模型
        # 多语音模型->英文模型
        # 单语音模型->中文模型
        if setting.audio_language == 'zh':
            coqui_tts = TTS(model_name="tts_models/zh-CN/baker/tacotron2-DDC-GST", gpu=False)
            # 生成语音并保存为文件
            coqui_tts.tts_to_file(text=text, file_path=file_path)
        else:
            coqui_tts = TTS(model_name="tts_models/en/vctk/vits", gpu=False)  # 不使用 GPU
            # 生成语音并保存为文件
            coqui_tts.tts_to_file(text=text, speaker=coqui_tts.speakers[1], file_path=file_path)
        # 单语音模型->英文模型
        # coqui_tts = TTS(model_name="tts_models/en/ljspeech/glow-tts", gpu=False)
        # 单语音模型->中文模型（推荐）
        # coqui_tts = TTS(model_name="tts_models/zh-CN/fastspeech2-ljspeech", gpu=False)
    except Exception as e:
        logger.error(f"Error occurred during TTS: {e}", exc_info=True)

# coqui_tts = TTS(model_name="tts_models/en/vctk/vits", gpu=False)
# coqui_tts.tts_to_file(text="hello, this world", speaker=coqui_tts.speakers[1], file_path="output.mp3")