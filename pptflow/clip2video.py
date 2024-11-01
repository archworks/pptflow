from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips
import os

# Create a video from images and audio
def create_video_from_images_and_audio(input_image_dir_path, input_audio_dir_path, 
    input_ppt_file_path, output_video_file_path, start_page_num=None, end_page_num=None):
    if not os.path.exists(input_image_dir_path):
        raise ValueError(f"{input_image_dir_path} not exist")
    if not os.path.exists(input_audio_dir_path):
        raise ValueError(f"{input_audio_dir_path} not exist")

    file_name_raw = os.path.basename(input_ppt_file_path).split('.')[0]
    print(file_name_raw)

    image_files = sorted(
        [f for f in os.listdir(input_image_dir_path) if f.endswith(".png") and file_name_raw in f],
        key=lambda x: int(x.split('.')[0].split('-P')[1])
    )

    if len(image_files) == 0:
        raise ValueError("image files don't exist")

    clips = []
    for idx, image_file in enumerate(image_files):
        if start_page_num and idx + 1  < start_page_num:
            continue
        if end_page_num and idx + 1  > end_page_num:
            continue
        file_name_without_ext = image_file.split('.')[0]
        audio_file_path = os.path.join(input_audio_dir_path, f"{file_name_without_ext}.mp3")
        if os.path.exists(audio_file_path):
            audio = AudioFileClip(audio_file_path)
            img_clip = ImageSequenceClip(
                [os.path.join(input_image_dir_path, image_file)], durations=[audio.duration]
            )
            img_clip = img_clip.set_audio(audio)
            clips.append(img_clip)

    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_video_file_path, codec="libx264", audio_codec="aac", fps=10)