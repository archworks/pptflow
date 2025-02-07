from abc import ABC, abstractmethod
from ..config.setting import Setting

class TtsService(ABC):
    @abstractmethod
    async def tts(self, text: str, output_audio_filename: str, setting: Setting):
        pass

    @abstractmethod
    def get_voice_list(self, setting: Setting = None):
        pass
