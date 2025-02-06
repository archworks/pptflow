from abc import ABC, abstractmethod
from .config.setting import Setting

class PptToImage(ABC):
    @abstractmethod
    def convert(self, input_ppt_path: str, setting: Setting, progress_tracker=None):
        pass