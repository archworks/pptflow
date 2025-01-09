import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to the module search path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from pptflow.ppt2video import ppt_to_video
from pptflow.config.setting import Setting

class TestPptToVideo(unittest.TestCase):

    @patch("pptflow.ppt2video.ppt_to_image")
    @patch("pptflow.ppt2video.ppt_note_to_audio")
    @patch("pptflow.ppt2video.create_video_from_images_and_audio")
    def test_ppt_to_video_mock_all(self, mock_create_video, mock_ppt_note_to_audio, mock_ppt_to_image):
        tts = MagicMock()
        setting = Setting()
        ppt_path = os.path.join(parent_dir, "test/test.pptx")
        
        ppt_to_video(tts, ppt_path, setting)
        
        mock_ppt_to_image.assert_called_once()
        mock_ppt_note_to_audio.assert_called_once()
        mock_create_video.assert_called_once()

    def test_invalid_ppt_path(self):
        tts = MagicMock()
        setting = Setting()
        ppt_path = "invalid/path/to/test.pptx"
        
        with self.assertRaises(ValueError):
            ppt_to_video(tts, ppt_path, setting)

    def test_ppt_to_video_with_pytttsx3(self):
        from pptflow.tts.tts_pyttsx3 import tts
        setting = Setting()
        # for macOS only
        setting.subtitle_font = 'C:/Windows/Fonts/timesi.ttf'
        ppt_path = os.path.join(parent_dir, "test/test.pptx")
        
        ppt_to_video(tts, ppt_path, setting)
    
    def test_ppt_to_video_with_azure(self):
        from pptflow.tts.tts_azure import tts
        setting = Setting()
        # for macOS only
        setting.subtitle_font = 'C:/Windows/Fonts/timesi.ttf'
        ppt_path = os.path.join(parent_dir, "test/test.pptx")
        
        ppt_to_video(tts, ppt_path, setting)

if __name__ == '__main__':
    unittest.main()