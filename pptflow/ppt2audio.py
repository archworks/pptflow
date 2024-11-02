import re
from unittest import result
from pptx import Presentation
import os 
import re
from moviepy.editor import AudioFileClip,concatenate_audioclips

def tts_pause(index, length, text):
    result = text.strip()
    # 在换行符后增加停顿
    result = re.sub(r'(\r?\n)',r'\1[p1000]',result)
    # 在每一页的最后增加停顿
    result += '[p2000]'
    if index == 0:
        # 在最开头增加停顿
        result = '[p2000]' + result
    if index == length -1:
        # 在最后增加停顿
        result += '[p10000]'
    return result

def tts_pause2(page_index, page_length, text, segment_index, segment_length):
    return text
    result = text.strip()
    # 在每一个换行符前增加停顿
    result = re.sub(r'(\r?\n)',r'[p1000]\1',result)
    
    # 在每一页的最后增加停顿
    if segment_index == segment_length - 1:
        result += '[p2000]'
    
    # 在PPT第一页和最后一页额外增加停顿
    if page_index == 0 and segment_index == 0:
        # 在ppt最开头增加停顿
        result = '[p2000]' + result
    if page_index == page_length -1 and segment_index == segment_length - 1:
        # 在ppt最后增加停顿
        result += '[p10000]'
    return result

def tts_replace(text):
    result = text.replace('MySQL', 'My SQL[=si:kwl]') \
        .replace('负载均衡', '负载[=zai3]均衡')
    return result

def audio_file_do_replace_check(audio_file_path, note_text):
    note_text_path = audio_file_path.replace('.mp3', '.txt')
    if os.path.exists(audio_file_path) and os.path.exists(note_text_path):
        with open(note_text_path, 'r', encoding='utf-8') as note_file:
            old_note_text = note_file.read()
            if old_note_text == note_text:
                return False
    return True

def add_audio_file_text_cache(audio_file_path, note_text):
    note_text_path = audio_file_path.replace('.mp3', '.txt')
    with open(note_text_path, 'w', encoding='utf-8') as note_file:
        note_file.write(note_text)   

def del_file_text_del_cache(audio_file_path):
    note_text_path = audio_file_path.replace('.mp3', '.txt')
    if os.path.exists(note_text_path):
        os.remove(note_text_path)

def ppt_note_to_audio(tts, input_ppt_path, output_audio_dir_path, start_page_num = None, end_page_num=None, output_replace_check = True):
    try:
        presentation = Presentation(input_ppt_path)
        file_name_without_ext = os.path.basename(input_ppt_path).split('.')[0]

        # Create a dir to save the slides as images
        if not os.path.exists(output_audio_dir_path):
            os.makedirs(output_audio_dir_path)

        # 遍历每一张幻灯片
        for idx, slide in enumerate(presentation.slides):
            if start_page_num and idx + 1 < start_page_num:
                continue
            if end_page_num and idx + 1 > end_page_num:
                continue
            # 读取幻灯片的备注
            if slide.has_notes_slide:
                notes_slide = slide.notes_slide
                # 打印备注文本
                note_text = notes_slide.notes_text_frame.text
                generate_audio_and_subtitles(tts,output_audio_dir_path,note_text,len(presentation.slides), idx,\
                    file_name_without_ext, output_replace_check)
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e

def split_text(text, max_chars=50):
    delimiters = r'([,.;!?，。；！？\n]|\s{2,})'
    sentences = re.split(delimiters, text)
    sentences = [s.strip() for s in sentences if s.strip()]

    result = []
    current_segment = ""
    for sentence in sentences:
        if len(current_segment) + len(sentence) <= max_chars:
            current_segment += " " + sentence if current_segment else sentence
        else:
            if current_segment:
                result.append(current_segment)
            current_segment = sentence

    if current_segment:
        result.append(current_segment)

    return result

def generate_audio(tts, output_audio_dir_path, text, length, index, filename_prefix, output_replace_check):
    #print(note_text)
    # 预处理
    speech_text = tts_pause(index, length, text)
    speech_text = tts_replace(speech_text)

    audio_file_path = os.path.join(output_audio_dir_path, f"{filename_prefix}-P{index + 1}.mp3")
    if output_replace_check and not audio_file_do_replace_check(audio_file_path, speech_text):
        print(f'{audio_file_path}已存在且文本内容无变化，跳过')
        return 
    tts_re = tts(speech_text, audio_file_path)
    if tts_re:
        add_audio_file_text_cache(audio_file_path, speech_text)
    else:
        del_file_text_del_cache(audio_file_path)

def generate_audio_and_subtitles(tts, output_audio_dir_path, text, page_length, page_index, filename_prefix, output_replace_check):
    text_segments = split_text(text)
    
    audio_file_path = os.path.join(output_audio_dir_path, f"{filename_prefix}-P{page_index + 1}.mp3")
    subtitle_file_path = os.path.join(output_audio_dir_path,f'{filename_prefix}-P{page_index + 1}.srt')
    
    if output_replace_check and not audio_file_do_replace_check(audio_file_path, ''.join(text_segments)):
        print(f'{audio_file_path}已存在且文本内容无变化，跳过')
        return 
    
    try:
        audio_clips=[]
        subtitle_file = open(subtitle_file_path, 'w')
        current_time = 0
        for idx, segment_text in enumerate(text_segments):
            # 生成每个段落的语音
            segment_audio_file_path = os.path.join(output_audio_dir_path,f'{filename_prefix}-P{page_index+1}-S{idx+1}.mp3')
            # 预处理
            speech_text = tts_pause2(page_index, page_length, segment_text, idx, len(text_segments))
            speech_text = tts_replace(speech_text)
            tts_result = tts(speech_text, segment_audio_file_path)
            
            if not tts_result:
                del_file_text_del_cache(audio_file_path)
                raise RuntimeError('tts failed')
            # 读取生成的语音文件
            segment_audio = AudioFileClip(segment_audio_file_path)
            
            # 计算字幕时间
            start_time = current_time
            end_time = start_time + segment_audio.duration
            
            # 写入字幕
            subtitle_file.write(f"{idx+1}\n")
            subtitle_file.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            subtitle_file.write(f"{segment_text}\n\n")
            
            # 更新当前时间
            current_time = end_time
            
            # 将段落音频添加到完整音频中
            audio_clips.append(segment_audio)
        
        # 保存完整的音频文件
        final_audio = concatenate_audioclips(audio_clips)
        final_audio.write_audiofile(audio_file_path)
        # 生成音频处理记录缓存
        add_audio_file_text_cache(audio_file_path, ''.join(text_segments))
    finally:
        # 关闭字幕文件
        subtitle_file.close()
        # 关闭并删除临时音频文件
        for clip in audio_clips:
            clip.close()
        for i in range(len(text_segments)):
            segment_audio_file_path = os.path.join(output_audio_dir_path,f'{filename_prefix}-P{page_index+1}-S{i+1}.mp3')
            if os.path.exists(segment_audio_file_path):
                os.remove(segment_audio_file_path)

def format_time(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"