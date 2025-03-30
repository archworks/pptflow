from moviepy import AudioFileClip
import os
from pptflow.utils import mylogger

logger = mylogger.get_logger(__name__)


def get_audio_total_duration(input_audio_dir_path, filename_prefix):
    total_duration = 0
    audio_list = []
    for file_name in os.listdir(input_audio_dir_path):
        if not file_name.endswith(".mp3") or not file_name.startswith(filename_prefix):
            continue
        audio_file_path = os.path.join(input_audio_dir_path, file_name)
        audio_list.append(audio_file_path)
    audio_list = sorted(audio_list, key=lambda x: int(x.split('.')[0].split('-P')[1]))
    for audio_path in audio_list:
        audio = AudioFileClip(audio_path)
        # logger.info(f'audio_path: {os.path.basename(audio_path)}, duration: {audio.duration: .2f}s')
        total_duration += audio.duration
        audio.close()
    logger.info(f'total_duration: {total_duration: .2f}s, {total_duration / 60: .2f}min')
    return total_duration


if __name__ == '__main__':
    total_duration = get_audio_total_duration(r'C:\Users\19622\AppData\Roaming\pptflow\temp\audio', '国科恒泰内幕信息培训演示文稿') / 60
