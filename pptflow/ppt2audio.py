import re
from unittest import result
from pptx import Presentation
import os 
import re


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
                #print(note_text)
                text = tts_pause(idx, len(presentation.slides), note_text)
                text = tts_replace(text)
                audio_file_path = os.path.join(output_audio_dir_path, f"{file_name_without_ext}-P{idx + 1}.mp3")
                if output_replace_check and not audio_file_do_replace_check(audio_file_path, text):
                    print(f'{audio_file_path}已存在且文本内容无变化，跳过')
                    continue
                tts_re = tts(text, audio_file_path)
                if tts_re:
                    add_audio_file_text_cache(audio_file_path, text)
                else:
                    del_file_text_del_cache(audio_file_path)
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e
