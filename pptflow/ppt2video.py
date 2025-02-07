import asyncio
import os
import re
import time
from .utils import mylogger
from .clip2video import create_video_from_images_and_audio
from .ppt2audio import ppt_note_to_audio
from pptflow.config.setting import Setting
from pptflow.ppt2image_factory import get_ppt_to_image

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)
ppt_to_image = get_ppt_to_image()


def ppt_to_video(tts, ppt_path, setting: Setting, progress_tracker=None):
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
    ppt_to_image.convert(ppt_path, setting, progress_tracker)
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
    logger.info(
        f"create_video_from_images_and_audio runtime: {end_time_create_video - end_time_ppt_note_to_audio:.2f} seconds")

    # Total runtime
    total_time = end_time_create_video - start_time
    logger.info(f"Runtime: {total_time:.2f} seconds")

    return total_time
