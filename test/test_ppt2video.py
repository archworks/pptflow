import os, platform
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to the module search path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from pptflow.ppt2video import ppt_to_video
from pptflow.config.setting_factory import get_default_setting
from pptflow.tts.tts_service_factory import get_tts_service


class TestPptToVideo(unittest.TestCase):

    @patch("pptflow.ppt2video.ppt_to_image.convert")
    @patch("pptflow.ppt2video.ppt_note_to_audio")
    @patch("pptflow.ppt2video.create_video_from_images_and_audio")
    def test_ppt_to_video_mock_all(self, mock_create_video, mock_ppt_note_to_audio, mock_ppt_to_image):
        tts = MagicMock()
        setting = get_default_setting(os_name=platform.system())
        ppt_path = os.path.join(parent_dir, "test/test-en.pptx")

        ppt_to_video(tts, ppt_path, setting)

        mock_ppt_to_image.assert_called_once()
        mock_ppt_note_to_audio.assert_called_once()
        mock_create_video.assert_called_once()

    def test_invalid_ppt_path(self):
        tts = MagicMock()
        setting = get_default_setting(os_name=platform.system())
        ppt_path = "invalid/path/to/test.pptx"

        with self.assertRaises(ValueError):
            ppt_to_video(tts, ppt_path, setting)

    def test_ppt_to_video_with_pyttsx3(self):
        tts_service = get_tts_service('pyttsx3')
        os_name = platform.system()
        setting = get_default_setting(os_name=os_name, language='zh', tts_service_provider='pyttsx3')
        ppt_path = os.path.join(parent_dir, "test/test-zh.pptx")

        ppt_to_video(tts_service.tts, ppt_path, setting)
        assert os.path.exists(setting.video_path)

    def test_ppt_to_video_with_azure(self):
        tts_service = get_tts_service('azure')
        os_name = platform.system()
        setting = get_default_setting(os_name=os_name, tts_service_provider='azure')
        setting.tts_voice_name = 'en-US-AndrewMultilingualNeural'
        ppt_path = os.path.join(parent_dir, "test/test-en.pptx")

        ppt_to_video(tts_service.tts, ppt_path, setting)
        assert os.path.exists(setting.video_path)


if __name__ == '__main__':
    unittest.main()
