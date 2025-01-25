from moviepy.editor import AudioFileClip
import os

def get_audio_total_duration(input_audio_dir_path):
    total_duration = 0
    for file_name in os.listdir(input_audio_dir_path):
        if not file_name.endswith(".mp3"):
            continue
        audio_file_path = os.path.join(input_audio_dir_path, file_name)
        audio = AudioFileClip(audio_file_path)
        total_duration += audio.duration
        audio.close()
    return total_duration

print(get_audio_total_duration(r'D:\MyWorkspace\project\ppt2video\temp\audio') / 60 )