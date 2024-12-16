from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy import CompositeVideoClip, concatenate_videoclips
from moviepy.video.VideoClip import ImageClip, TextClip
from moviepy.video.tools.subtitles import SubtitlesClip
import os
from utils import mylogger

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)


# Create a video from images and audio
def create_video_from_images_and_audio(ppt_file_path, setting):
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

    # Synthesize all video clips
    final_clip = concatenate_videoclips(clips)
    # Write the clips to a video file
    logger.info(f"Writing video to {setting.video_path}")
    final_clip.write_videofile(setting.video_path, codec=setting.video_codec,
                               audio_codec=setting.audio_codec, fps=setting.video_fps,
                               threads=setting.video_processing_threads, logger=None)
    # Release resources
    final_clip.close()
