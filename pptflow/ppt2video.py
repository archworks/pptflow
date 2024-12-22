import os
import platform
import re
import time
from utils import mylogger
from .clip2video import create_video_from_images_and_audio
from .ppt2audio import ppt_note_to_audio
from .setting import Setting

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)
# import ppt to image module according to os platform
os_name = platform.system()
if os_name == "Windows":
    from .ppt2image_win import ppt_to_image
elif os_name == "Linux":
    from .ppt2image_linux import ppt_to_image
elif os_name == "Darwin":  # macOS
    from .ppt2image_mac import ppt_to_image
else:
    logger.error(f"Unsupported OS: {os_name}")
    raise NotImplementedError(f"Unsupported OS: {os_name}")
logger.info(f"OS:{os_name}")


def load_tts(setting: Setting):
    # import tts module according to service provider
    tts_service_provider = setting.tts_service_provider

    if not tts_service_provider:
        logger.error("tts服务未配置")
        raise NotImplementedError(f"tts服务未配置")
    if tts_service_provider.lower() == "azure":
        from .tts_azure import tts
        logger.info(f"tts service provider: {tts_service_provider}")
    elif tts_service_provider.lower() == "edge-tts":
        from .tts_edge_tts import tts
        logger.info(f"tts service provider: {tts_service_provider}")
    elif tts_service_provider.lower() == "xunfei":
        from .tts_xunfei import tts
    else:
        logger.error(f"不支持的tts: {tts_service_provider}")
        raise NotImplementedError(f"不支持的tts: {tts_service_provider}")
    return tts


def ppt_to_video(ppt_path, setting: Setting):
    tts = load_tts(setting)
    # Check whether the ppt_path is None or Valid
    if ppt_path is None or not os.path.exists(ppt_path):
        logger.error("ppt_path is None or invalid")
        raise ValueError("ppt_path is None or invalid")
    start_time = time.time()

    # set default output path to the mp4 file, same director as the ppt file.
    if setting.video_path is None:
        setting.video_path = re.sub(r"pptx?$", "mp4", ppt_path)
        logger.info(f'video_path:{setting.video_path}')
    ppt_to_image(ppt_path, setting)
    ppt_note_to_audio(tts, ppt_path, setting)
    create_video_from_images_and_audio(ppt_path, setting)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Runtime:{elapsed_time:.2f}seconds")
    return elapsed_time
