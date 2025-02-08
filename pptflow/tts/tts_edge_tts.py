# Author: Valley-e
# Date: 2024/12/22  
# Description:
import json
import os
import edge_tts
import asyncio
from pptflow.utils import mylogger
from .tts_service import TtsService
from ..config.setting import Setting


class EdgeTtsService(TtsService):
    logger = mylogger.get_logger(__name__)

    async def tts(self, text: str, output_audio_filename: str, setting: Setting):
        try:
            # Create an EdgeTTS object
            communicate = edge_tts.Communicate(text, voice=setting.tts_voice_name, rate=setting.tts_voice_rate)
            # Save the audio to the specified file
            await communicate.save(output_audio_filename)
            return True
        except Exception as e:
            self.logger.error(f"Error occurred: {e}", exc_info=True)
            return False

    async def list_voices(self, filename: str):
        try:
            # List all voices
            voices = await edge_tts.list_voices()
            # Get the key information
            voice_list = [{"Locale": voice["Locale"], "Gender": voice["Gender"], "ShortName": voice["ShortName"]} for
                          voice
                          in voices]
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(voice_list, file, ensure_ascii=False, indent=4)
                self.logger.info(f"Voice list has been saved to {filename}")
        except Exception as e:
            self.logger.error(f"Error occurred: {e}", exc_info=True)
            self.logger.error(
                "An error occurred while retrieving the voice list. Please check the status of your network.")

    def get_voice_list(self, setting: Setting = None):
        voice_dir = os.path.join(os.getcwd(), 'voice')
        os.makedirs(voice_dir, exist_ok=True)
        filename = os.path.join(voice_dir, 'edge_tts_voice_list.json')
        if not os.path.exists(filename):
            asyncio.run(self.list_voices(filename))
        with open(filename, "r", encoding="utf-8") as file:
            voice_list = json.load(file)
            self.logger.info(f"Voice list has been loaded from {filename}")
        return [f'{voice["ShortName"]} ({voice["Locale"]}, {voice["Gender"]})' for voice in voice_list]
