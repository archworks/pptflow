from pptx import Presentation
import os
import re
from moviepy import AudioFileClip
from moviepy.audio.AudioClip import concatenate_audioclips
from utils import mylogger
import asyncio

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)


def tts_pause(index, length, text):
    result = text.strip()
    # 在换行符后增加停顿
    result = re.sub(r'(\r?\n)', r'\1[p1000]', result)
    # 在每一页的最后增加停顿
    result += '[p2000]'
    if index == 0:
        # 在最开头增加停顿
        result = '[p2000]' + result
    if index == length - 1:
        # 在最后增加停顿
        result += '[p10000]'
    return result


def tts_pause2(page_index, page_length, text, segment_index, segment_length):
    return text
    result = text.strip()
    # 在每一个换行符前增加停顿
    result = re.sub(r'(\r?\n)', r'[p1000]\1', result)

    # 在每一页的最后增加停顿
    if segment_index == segment_length - 1:
        result += '[p2000]'

    # 在PPT第一页和最后一页额外增加停顿
    if page_index == 0 and segment_index == 0:
        # 在ppt最开头增加停顿
        result = '[p2000]' + result
    if page_index == page_length - 1 and segment_index == segment_length - 1:
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


def ppt_note_to_audio(tts, input_ppt_path, setting):
    try:
        presentation = Presentation(input_ppt_path)
        file_name_without_ext = os.path.basename(input_ppt_path).split('.')[0]

        # Create a dir to save the slides as images
        if not os.path.exists(setting.audio_dir_path):
            os.makedirs(setting.audio_dir_path)

        # Go through each slide
        for idx, slide in enumerate(presentation.slides):
            # Checks whether the current slide falls within the specified start and end page ranges
            if setting.start_page_num and idx + 1 < setting.start_page_num:
                continue
            if setting.end_page_num and idx + 1 > setting.end_page_num:
                continue
            # Check if the slide has a notes section. If it does, to generate audio and subtitles for it.
            if slide.has_notes_slide:
                notes_slide = slide.notes_slide
                # Get the text from the notes section
                note_text = notes_slide.notes_text_frame.text
                # Generate audio and subtitles
                generate_audio_and_subtitles(tts, note_text, len(presentation.slides), idx,
                                             file_name_without_ext, setting)
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        raise e


def split_text(text, max_chars=50):
    delimiters = r'([,.;!?，。；！？\n]|\s{2,})'
    sentences = re.split(delimiters, text)
    sentences = [s.strip() for s in sentences if s.strip()]

    result = []
    current_segment = ""
    # Iterate over each sentence to build segments that do not exceed the maximum character limit
    for sentence in sentences:
        # If adding the current sentence to the current segment does not exceed the maximum character limit
        if len(current_segment) + len(sentence) <= max_chars:
            # Append the current sentence to the current segment, adding a space if the segment is not empty
            current_segment += " " + sentence if current_segment else sentence
        else:
            # If the current segment is full, append it to the result list and start a new segment
            if current_segment:
                result.append(current_segment)
            current_segment = sentence

    # If there is any remaining segment that has not been added to the result list, append it
    if current_segment:
        result.append(current_segment)

    return result


def generate_audio(tts, output_audio_dir_path, text, length, index, filename_prefix, audio_local_cache_enabled):
    # logger.debug(note_text)
    # 预处理
    speech_text = tts_pause(index, length, text)
    speech_text = tts_replace(speech_text)

    audio_file_path = os.path.join(output_audio_dir_path, f"{filename_prefix}-P{index + 1}.mp3")
    if audio_local_cache_enabled and not audio_file_do_replace_check(audio_file_path, speech_text):
        logger.info(f'{audio_file_path} already exists and the text content does not change, then the step will be skipped.')
        return
    tts_re = tts(speech_text, audio_file_path)
    if tts_re:
        add_audio_file_text_cache(audio_file_path, speech_text)
    else:
        del_file_text_del_cache(audio_file_path)


def generate_audio_and_subtitles(tts, text, page_length, page_index, filename_prefix, setting):
    global subtitle_file, audio_clips
    text_segments = split_text(text)

    audio_file_path = os.path.join(setting.audio_dir_path, f"{filename_prefix}-P{page_index + 1}.mp3")
    subtitle_file_path = os.path.join(setting.audio_dir_path, f'{filename_prefix}-P{page_index + 1}.srt')

    # Check if the audio file already exists and has the same content as the current text
    if setting.audio_local_cache_enabled and not audio_file_do_replace_check(audio_file_path, ''.join(text_segments)):
        logger.info(f'{audio_file_path} already exists and the text content does not change, then skip this step.')
        return

    try:
        audio_clips = []
        subtitle_file = open(subtitle_file_path, 'w')
        current_time = 0
        for idx, segment_text in enumerate(text_segments):
            # file path to save the audio clip based on the current segment
            segment_audio_file_path = os.path.join(setting.audio_dir_path,
                                                   f'{filename_prefix}-P{page_index + 1}-S{idx + 1}.mp3')
            # Preprocess the text
            # Add pauses at the end of each slide, and at the beginning of the first one and the end of the last one
            speech_text = tts_pause2(page_index, page_length, segment_text, idx, len(text_segments))
            # Unify the pronunciation of specific words for each platform
            speech_text = tts_replace(speech_text)
            # Generate the audio clip via the tts engine at the specified path
            if setting.tts_service_provider == 'edge-tts':
                tts_result = asyncio.run(tts(speech_text, segment_audio_file_path, setting))
            else:
                tts_result = tts(speech_text, segment_audio_file_path, setting)

            # If the audio clip generation fails, delete the audio file and raise an exception
            if not tts_result:
                del_file_text_del_cache(audio_file_path)
                logger.error('tts failed')
                raise RuntimeError('tts failed')
            # Read the generated audio clip
            segment_audio = AudioFileClip(segment_audio_file_path)

            # Calculate the duration of the current audio clip
            start_time = current_time
            end_time = start_time + segment_audio.duration

            # Write the subtitle to the subtitle file
            subtitle_file.write(f"{idx + 1}\n")
            subtitle_file.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            subtitle_file.write(f"{segment_text}\n\n")

            # Update the current time
            current_time = end_time

            # Add the current audio clip to the list of audio clips
            audio_clips.append(segment_audio)

        # Save the final audio clip to the specified path
        final_audio = concatenate_audioclips(audio_clips)
        final_audio.write_audiofile(audio_file_path, logger=None)
        # Cache the audio file via saving the text content
        add_audio_file_text_cache(audio_file_path, ''.join(text_segments))
    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
    finally:
        # Close the subtitle file
        subtitle_file.close()
        # Close and remove the temporary audio clips
        for clip in audio_clips:
            clip.close()
        for i in range(len(text_segments)):
            segment_audio_file_path = os.path.join(setting.audio_dir_path,
                                                   f'{filename_prefix}-P{page_index + 1}-S{i + 1}.mp3')
            if os.path.exists(segment_audio_file_path):
                os.remove(segment_audio_file_path)


def format_time(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

