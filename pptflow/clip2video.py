from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, ImageClip, \
    TextClip
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.config import change_settings
import os
from utils import mylogger

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)

if os.environ.get("IMAGEMAGICK_BINARY"):
    change_settings({'IMAGEMAGICK_BINARY': f'{os.environ.get("IMAGEMAGICK_BINARY")}'})


# Create a video from images and audio
def create_video_from_images_and_audio(input_image_dir_path, input_audio_dir_path,
                                       input_ppt_file_path, output_video_file_path, setting):
    if not os.path.exists(input_image_dir_path):
        logger.error(f"{input_image_dir_path} not exist")
        raise ValueError(f"{input_image_dir_path} not exist")
    if not os.path.exists(input_audio_dir_path):
        logger.error(f"{input_audio_dir_path} not exist")
        raise ValueError(f"{input_audio_dir_path} not exist")

    file_name_raw = os.path.basename(input_ppt_file_path).split('.')[0]

    # Sort the images extracted from the ppt
    image_files = sorted(
        [f for f in os.listdir(input_image_dir_path) if f.endswith(".png") and file_name_raw in f],
        key=lambda x: int(x.split('.')[0].split('-P')[1])
    )

    if len(image_files) == 0:
        logger.error(f"image files don't exist in {input_image_dir_path}")
        raise ValueError("image files don't exist")

    clips = []
    for idx, image_file in enumerate(image_files):
        if setting.start_page_num and idx + 1 < setting.start_page_num:
            continue
        if setting.end_page_num and idx + 1 > setting.end_page_num:
            continue
        file_name_without_ext = image_file.split('.')[0]
        image_file_path = os.path.join(input_image_dir_path, image_file)
        audio_file_path = os.path.join(input_audio_dir_path, f"{file_name_without_ext}.mp3")
        subtitle_file_path = os.path.join(input_audio_dir_path, f"{file_name_without_ext}.srt")
        if os.path.exists(audio_file_path):
            audio_clip = AudioFileClip(audio_file_path)
            image_clip = ImageClip(image_file_path).set_duration(audio_clip.duration)
            # Adds audio to a video clip
            video_clip = image_clip.set_audio(audio_clip)
            # Add subtitles
            if os.path.exists(subtitle_file_path):
                subtitles = SubtitlesClip(subtitle_file_path,
                                          lambda txt: TextClip(txt, font='Microsoft-YaHei-&-Microsoft-YaHei-UI',
                                                               fontsize=24, color='white', stroke_color='black',
                                                               stroke_width=0.5, method='caption',
                                                               size=(video_clip.w * 0.9, None)))
                video_clip = CompositeVideoClip([video_clip, subtitles.set_position(('center', video_clip.h * 0.85))])

            clips.append(video_clip)

    # Synthesize all video clips
    final_clip = concatenate_videoclips(clips)
    # Write the clips to a videofile
    final_clip.write_videofile(output_video_file_path, codec="libx264", audio_codec="aac", fps=10, threads=4)
    # Release resources
    final_clip.close()
