# Author: Valley-e
# Date: 2024/12/22  
# Description:
import edge_tts
import asyncio
from utils import mylogger

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)


async def tts(text, output_file, setting):
    try:
        # Create an EdgeTTS object
        communicate = edge_tts.Communicate(text, voice=setting.tts_voice_name, rate=setting.tts_voice_rate)
        # Save the audio to the specified file
        await communicate.save(output_file)
        return True
    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
        return False
