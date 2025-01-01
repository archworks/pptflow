import asyncio
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
        logger.info(f"tts service provider: {tts_service_provider}")
    elif tts_service_provider.lower() == "pyttsx3":
        from .tts_pyttsx3 import tts
        logger.info(f"tts service provider: {tts_service_provider}")
    elif tts_service_provider.lower() == "coqui-tts":
        from .tts_Coqui_tts import tts
        logger.info(f"tts service provider: {tts_service_provider}")
    else:
        logger.error(f"不支持的tts: {tts_service_provider}")
        raise NotImplementedError(f"不支持的tts: {tts_service_provider}")
    return tts


def ppt_to_video(ppt_path, setting: Setting, progress_tracker=None):
    tts = load_tts(setting)
    # Check whether the ppt_path is None or Valid
    if ppt_path is None or not os.path.exists(ppt_path):
        logger.error("ppt_path is None or invalid")
        raise ValueError("ppt_path is None or invalid")

    # set default output path to the mp4 file, same director as the ppt file.
    if setting.video_path is None:
        setting.video_path = re.sub(r"pptx?$", "mp4", ppt_path)
        logger.info(f'video_path:{setting.video_path}')
    # Record the start time
    start_time = time.time()

    # PPT to Image conversion
    if progress_tracker:
        progress_tracker.start_step('ppt_to_image')
    ppt_to_image(ppt_path, setting, progress_tracker)
    if progress_tracker:
        progress_tracker.complete_step()
    end_time_ppt_to_image = time.time()
    logger.info(f"ppt_to_image runtime: {end_time_ppt_to_image - start_time:.2f} seconds")

    # Generate audio from notes
    if progress_tracker:
        progress_tracker.start_step('ppt_note_to_audio')
    asyncio.run(ppt_note_to_audio(tts, ppt_path, setting, progress_tracker))
    if progress_tracker:
        progress_tracker.complete_step()
    end_time_ppt_note_to_audio = time.time()
    logger.info(f"ppt_note_to_audio runtime: {end_time_ppt_note_to_audio - end_time_ppt_to_image:.2f} seconds")

    # Create final video
    if progress_tracker:
        progress_tracker.start_step('create_video')
    create_video_from_images_and_audio(ppt_path, setting, progress_tracker)
    if progress_tracker:
        progress_tracker.complete_step()
    end_time_create_video = time.time()
    logger.info(f"create_video_from_images_and_audio runtime: {end_time_create_video - end_time_ppt_note_to_audio:.2f} seconds")

    # Total runtime
    total_time = end_time_create_video - start_time
    logger.info(f"Runtime: {total_time:.2f} seconds")

    return total_time
