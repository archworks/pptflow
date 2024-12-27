import asyncio
from concurrent.futures import ThreadPoolExecutor
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy import CompositeVideoClip, concatenate_videoclips
from moviepy.video.VideoClip import ImageClip, TextClip
from moviepy.video.tools.subtitles import SubtitlesClip
import os
from utils import mylogger

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)


# Create a video from images and audio
def create_video_from_images_and_audio(ppt_file_path, setting, progress_tracker=None):
    if not os.path.exists(setting.image_dir_path):
        logger.error(f"{setting.image_dir_path} not exist")
        raise ValueError(f"{setting.image_dir_path} not exist")
    if not os.path.exists(setting.audio_dir_path):
        logger.error(f"{setting.audio_dir_path} not exist")
        raise ValueError(f"{setting.audio_dir_path} not exist")

    file_name_raw = os.path.basename(ppt_file_path).split('.')[0]

    # Sort the images extracted from the ppt
    image_files = sorted(
        [f for f in os.listdir(setting.image_dir_path) if f.endswith((".jpg", ".png")) and file_name_raw in f],
        key=lambda x: int(x.split('.')[0].split('-P')[1])
    )

    if len(image_files) == 0:
        logger.error(f"image files don't exist in {setting.image_dir_path}")
        raise ValueError("image files don't exist")

    clips = []
    total_files = len(image_files)
    for idx, image_file in enumerate(image_files):
        if setting.start_page_num and idx + 1 < setting.start_page_num:
            continue
        if setting.end_page_num and idx + 1 > setting.end_page_num:
            continue
        file_name_without_ext = image_file.split('.')[0]
        image_file_path = os.path.join(setting.image_dir_path, image_file)
        audio_file_path = os.path.join(setting.audio_dir_path, f"{file_name_without_ext}.mp3")
        subtitle_file_path = os.path.join(setting.audio_dir_path, f"{file_name_without_ext}.srt")
        if os.path.exists(audio_file_path):
            audio_clip = AudioFileClip(audio_file_path)
            image_clip = ImageClip(image_file_path).with_duration(audio_clip.duration)
            # Adds audio to a video clip
            video_clip = image_clip.with_audio(audio_clip)
            # Add subtitles
            if os.path.exists(subtitle_file_path):
                generator = lambda txt: TextClip(font=setting.subtitle_font, text=txt,
                                                 font_size=setting.subtitle_font_size,
                                                 color=setting.subtitle_color,
                                                 stroke_color=setting.subtitle_stroke_color,
                                                 stroke_width=setting.subtitle_stroke_width,
                                                 method='caption',
                                                 size=(int(video_clip.w * 0.9), None))
                subtitles = SubtitlesClip(subtitles=subtitle_file_path, make_textclip=generator)
                video_clip = CompositeVideoClip([video_clip, subtitles.with_position(('center', video_clip.h * 0.85))])

            clips.append(video_clip)
            # Update progress (70% for clip creation, 30% for final rendering)
            if progress_tracker:
                progress = 0.3 * (idx + 1) / total_files
                progress_tracker.update_step(progress)
        else:
            logger.warning(f"Audio file {audio_file_path} not found")
            raise ValueError(f"Please check whether the ppt has notes.")
    # Synthesize all video clips
    final_clip = concatenate_videoclips(clips)
    # Write the clips to a video file
    logger.info(f"Writing video to {setting.video_path}")

    # final_clip.write_videofile(setting.video_path, codec=setting.video_codec,
    #                            audio_codec=setting.audio_codec, fps=setting.video_fps,
    #                            threads=setting.video_processing_threads, logger=None)
    asyncio.run(write_video_async(final_clip, setting, progress_tracker))
    if progress_tracker:
        # Map progress from 0-1 to 70-100%
        progress_tracker.complete_step()
    # Release resources
    final_clip.close()


# 目标函数包装：接受位置参数和关键字参数
def write_video_with_kwargs(final_clip, setting):
    """
    包装 final_clip.write_videofile，支持通过关键字参数调用
    """
    kwargs = {
        "filename": setting.video_path,
        "codec": setting.video_codec,
        "audio_codec": setting.audio_codec,
        "fps": float(setting.video_fps),  # 确保 fps 是 float 类型
        "threads": setting.video_processing_threads,
        "logger": None,
    }
    # 调用原始方法，传递剩余的关键字参数
    final_clip.write_videofile(**kwargs)


# 进度更新函数
async def update_progress_tracker(progress_tracker, start, end, step=0.01):
    current = start
    while current < end:
        progress_tracker.update_step(current)
        current += step
        await asyncio.sleep(0.1)


# 异步写视频函数
async def write_video_async(final_clip, setting, progress_tracker):
    loop = asyncio.get_event_loop()

    with ThreadPoolExecutor() as executor:
        # 使用线程池异步写视频
        write_video_future = loop.run_in_executor(
            executor,
            write_video_with_kwargs,  # 调用包装函数
            final_clip,  # 传递 final_clip 作为第一个参数
            setting,  # 传递 setting 作为第二个参数
        )

        # 同时更新进度条从 0.7 到 0.99
        await asyncio.gather(
            update_progress_tracker(progress_tracker, 0.7, 0.99),
            write_video_future
        )
