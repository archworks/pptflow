from dotenv import load_dotenv

load_dotenv()

import os, re, platform, time
from .ppt2audio import ppt_note_to_audio
from .clip2video import create_video_from_images_and_audio
from .setting import Setting
from utils import mylogger

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)
# import tts module according to service provider
tts_service_provider = os.environ.get("TTS_SERVICE_PROVIDER")
if not tts_service_provider:
    logger.error("tts服务未配置")
    raise NotImplementedError(f"tts服务未配置")
if tts_service_provider.lower() == "azure":
    from .tts_azure import tts
elif tts_service_provider.lower() == "xunfei":
    from .tts_xunfei import tts
else:
    logger.error(f"不支持的tts: {tts_service_provider}")
    raise NotImplementedError(f"不支持的tts: {tts_service_provider}")

# import ppt to image module according to os platform
os_name = platform.system()
if os_name == "Windows":
    from .ppt2image_win import ppt_to_image
elif os_name == "Linux":
    from .ppt2image_linux import ppt_to_image
elif os_name == "Darwin":  # macOS
    from .ppt2image_mac import ppt_to_image
else:
    logger.error(f"不支持的操作系统: {os_name}")
    raise NotImplementedError(f"不支持的操作系统: {os_name}")


def process(ppt_path, setting: Setting, video_path=None):
    start_time = time.time()
    # Specify the full path to the PowerPoint presentation
    temp_dir = os.path.join(os.getcwd(), "temp")
    image_dir_path = os.path.join(temp_dir, "image")
    audio_dir_path = os.path.join(temp_dir, "audio")

    # set default path to the mp4 file, same director as the ppt file.
    if video_path is None:
        video_path = re.sub(r"pptx?$", "mp4", ppt_path)
        logger.info(f'video_path:{video_path}')
    ppt_to_image(ppt_path, image_dir_path, setting)
    ppt_note_to_audio(tts, ppt_path, audio_dir_path, setting)
    create_video_from_images_and_audio(
        image_dir_path,
        audio_dir_path,
        ppt_path,
        video_path,
        setting
    )
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"运行时间:{elapsed_time:.2f}秒")
