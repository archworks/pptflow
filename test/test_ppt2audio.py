import os, sys

# Add parent directory to the module search path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from pptflow.ppt2audio import ppt_note_to_audio
from pptflow.config.setting import Setting
from dotenv import load_dotenv

load_dotenv()

## import tts module according to service provider
tts_service_provider = os.environ.get("TTS_SERVICE_PROVIDER")
if not tts_service_provider:
    raise NotImplementedError("tts服务未配置")
if tts_service_provider.lower() == "azure":
    from pptflow.tts.tts_azure import tts
elif tts_service_provider.lower() == "xunfei":
    from pptflow.tts.tts_xunfei import tts

test_path = os.path.join(parent_dir, "test")
ppt_path = os.path.join(test_path, "test-en.pptx")
audio_dir_path = os.path.join(os.path.join(parent_dir, "temp"), "audio")

ppt_note_to_audio(tts, ppt_path, audio_dir_path, Setting())
