# Author: Valley-e
# Date: 2024/12/22  
# Description:
import json
import os
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


async def list_voices():
    try:
        # List all voices
        voices = await edge_tts.list_voices()
        # Get the key information
        voice_list = [{"Locale": voice["Locale"], "Gender": voice["Gender"], "ShortName": voice["ShortName"]} for voice
                      in voices]
        with open("edge_tts_voice_list.json", "w", encoding="utf-8") as file:
            json.dump(voice_list, file, ensure_ascii=False, indent=4)
            logger.info("Voice list has been saved to edge_tts_voice_list.json")
    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
        logger.error("An error occurred while retrieving the voice list. Please check the status of your network.")


def get_voice_list():
    if not os.path.exists("edge_tts_voice_list.json"):
        asyncio.run(list_voices())
    with open("edge_tts_voice_list.json", "r", encoding="utf-8") as file:
        voice_list = json.load(file)
        logger.info("Voice list has been loaded from edge_tts_voice_list.json")
    return [f'{voice["ShortName"]} ({voice["Locale"]}, {voice["Gender"]})' for voice in voice_list]
