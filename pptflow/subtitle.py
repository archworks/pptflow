from gtts import gTTS
from pydub import AudioSegment
from moviepy.editor import *
import re
from .tts_azure import tts

def text_to_speech(text, output_file):
    # 将文字转换为语音
    tts(text, output_file)
    # tts = gTTS(text=text, lang='zh-cn')
    # tts.save(output_file)

def split_text(text, max_chars=20):
    # 将文本分割成小段
    sentences = re.split('([。！？])', text)
    sentences = [''.join(i) for i in zip(sentences[0::2], sentences[1::2])]
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chars:
            current_chunk += sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def create_subtitles(text_chunks, audio_duration):
    # 为每个文本块创建字幕
    subtitle_clips = []
    chunk_duration = audio_duration / len(text_chunks)
    
    for i, chunk in enumerate(text_chunks):
        start_time = i * chunk_duration
        subtitle = TextClip(chunk, fontsize=24, color='white', font='SimHei')
        subtitle = subtitle.set_pos('bottom').set_start(start_time).set_duration(chunk_duration)
        subtitle_clips.append(subtitle)
    
    return subtitle_clips

def create_video_with_subtitles(audio_file, text_chunks, output_file):
    # 创建带有音频和字幕的视频
    audio = AudioFileClip(audio_file)
    audio_duration = audio.duration
    
    # 创建一个纯色背景
    background = ColorClip(size=(640, 480), color=(0, 0, 0)).set_duration(audio_duration)
    
    # 创建字幕
    subtitle_clips = create_subtitles(text_chunks, audio_duration)
    
    # 将所有元素组合在一起
    final_clip = CompositeVideoClip([background] + subtitle_clips)
    final_clip = final_clip.set_audio(audio)
    
    # 输出视频文件
    final_clip.write_videofile(output_file, fps=24)


def main():
    # 主程序
    text = "这是一个示例文本，用于演示文字转语音和生成字幕。这个方法基于文本分割，不使用语音识别。它可以更准确地生成字幕，并且可以处理较长的文本。"
    audio_file = "output.mp3"
    output_video = "output_video_with_subtitles.mp4"

    # 文字转语音
    text_to_speech(text, audio_file)

    # 分割文本
    text_chunks = split_text(text)

    # 创建带有字幕的视频
    create_video_with_subtitles(audio_file, text_chunks, output_video)

    print("处理完成！")