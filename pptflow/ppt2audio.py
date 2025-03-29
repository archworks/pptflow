from pptx import Presentation
import os
import re
from moviepy import AudioFileClip
from moviepy.audio.AudioClip import concatenate_audioclips
from pptflow.config.setting import Setting
from pptflow.utils import mylogger
import asyncio

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)


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


async def ppt_note_to_audio(tts, input_path, setting, progress_tracker=None):
    try:
        # 获取基础文件名（来自PPT文件或用户指定）
        file_name = os.path.basename(input_path).split('.')[0]
        # Create a dir to save the slides as images
        if not os.path.exists(setting.audio_dir_path):
            os.makedirs(setting.audio_dir_path)
        # 判断输入类型（PPT文件或图片目录）
        if input_path.lower().endswith('.pptx'):
            pages = process_pptx(input_path, setting)
        elif input_path.lower().endswith('.pdf'):
            pages = process_image_dir(setting.image_dir_path, file_name)
        else:
            raise ValueError("Unsupported file type")

        processed_count = 0
        logger.info(f"notes_file: {setting.external_notes_path}")

        for page in pages:
            if setting.start_page_num and page['number'] < setting.start_page_num:
                continue
            if setting.end_page_num and page['number'] > setting.end_page_num:
                continue

            note_text = get_note_text(page, setting)
            logger.info(f"Processing page {page['number']}: {note_text}")
            if note_text:
                await process_page(
                    tts=tts,
                    page=page,
                    note_text=note_text,
                    filename_prefix=file_name,
                    setting=setting
                )

            processed_count += 1
            if progress_tracker:
                progress = processed_count / len(pages)
                progress_tracker.update_step(progress)

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        raise e


def process_pptx(ppt_path, setting):
    """处理PPT文件"""
    presentation = Presentation(ppt_path)
    return [{
        'number': idx + 1,
        'slide': slide,
        'type': 'pptx'
    } for idx, slide in enumerate(presentation.slides)]


def process_image_dir(img_dir, filename_prefix):
    """处理图片目录"""
    # 使用正则表达式严格匹配文件名格式
    pattern = re.compile(
        r"^{prefix}-P(\d+)\.(?:png|jpg|jpeg)$".format(
            prefix=re.escape(filename_prefix)  # 转义特殊字符
        ),
        re.IGNORECASE  # 忽略大小写
    )

    images = []
    for fname in os.listdir(img_dir):
        match = pattern.match(fname)
        if match:
            images.append({
                'path': os.path.join(img_dir, fname),
                'number': int(match.group(1)),  # 提取页码
                'type': 'pdf'
            })

    # 按页码排序并验证连续性
    images.sort(key=lambda x: x['number'])
    validate_page_continuity(images, filename_prefix)
    if not images:
        raise ValueError(f"No images found in {img_dir}")
    logger.info(f"Found {len(images)} image files")

    return images


def validate_page_continuity(images, prefix):
    """验证页码连续性"""
    expected = 1
    for img in images:
        if img['number'] != expected:
            raise ValueError(
                f"Missing page {expected} for {prefix}. "
                f"Found page {img['number']} instead."
            )
        expected += 1


def get_note_text(page, setting):
    """统一获取备注文本"""
    if setting.has_notes:
        return page['slide'].notes_slide.notes_text_frame.text
    else:
        return parse_external_notes(setting.external_notes_path).get(page['number'], "")


async def process_page(tts, page, note_text, filename_prefix, setting):
    """统一处理单页"""
    await generate_audio_and_subtitles(
        tts=tts,
        text=note_text,
        page_number=page['number'],  # 修改参数为page_number
        filename_prefix=filename_prefix,
        setting=setting
    )


def parse_external_notes(file_path):
    """解析外部笔记文件"""
    notes = {}
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"External notes file not found: {file_path}")

        # 解析不同文件格式
        if file_path.endswith('.txt'):
            logger.info(f"Parsing external notes from .txt file")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        elif file_path.endswith('.docx'):
            logger.info(f"Parsing external notes from .docx file")
            from docx import Document
            doc = Document(file_path)
            content = "\n".join([para.text for para in doc.paragraphs])
        else:
            raise ValueError("Unsupported file format")

        # 使用正则表达式匹配页码
        pattern = r'第\s*(\d+)\s*页[：:]?\s*(.*?)(?=\n第|\Z)'
        matches = re.findall(pattern, content, re.DOTALL)

        for match in matches:
            page_num = int(match[0])
            page_content = match[1].strip()
            notes[page_num] = page_content

        return notes
    except Exception as e:
        logger.error(f"Failed to parse external notes: {e}")
        raise


def get_default_max_chars(language):
    defaults = {
        "zh": 20,
        "en": 50
    }
    return defaults.get(language, None)


def get_default_max_segment_chars(language):
    defaults = {
        "zh": 35,  # 中文每段字幕最大字符数
        "en": 80  # 英文每段字幕最大字符数
    }
    return defaults.get(language, None)


def set_defaults(max_chars, max_segment_chars, language):
    if max_chars is None:
        max_chars = get_default_max_chars(language)
        if max_chars is None:
            raise ValueError(f"Unsupported language: {language}")

    if max_segment_chars is None:
        max_segment_chars = get_default_max_segment_chars(language)
        if max_segment_chars is None:
            raise ValueError(f"Unsupported language: {language}")

    return max_chars, max_segment_chars


def split_text(text, language="en", max_chars=None, max_segment_chars=None):
    # 根据语言自动设置 max_chars
    max_chars, max_segment_chars = set_defaults(max_chars, max_segment_chars, language)
    logger.info(f"Splitting text into segments with max_chars={max_chars} and max_segment_chars={max_segment_chars}")

    # 根据语言设置分隔符
    if language == "zh":
        # 中文分隔符：，。；：！？、和换行
        delimiters = r'([，。；：！？\n])'
        text = text.replace("'", "’").replace("\"", "“").replace(";", "；")
    elif language == "en":
        # 英文分隔符：,.!?:;和换行
        delimiters = r'([,.!?:;\n])'
        text = text.replace("‘", "'").replace("“", "\"").replace("；", ";")
    else:
        # 默认保留原有分隔符集合
        delimiters = r'([,.;:!?，。；：！？\n])'

    # 按标点拆分并保留分隔符
    sentences = re.split(delimiters, text)

    # 重新组合，使分隔符紧跟前一句
    merged_sentences = []
    temp_sentence = ""

    for part in sentences:
        if re.match(delimiters, part):  # 这是标点，拼接到前面
            temp_sentence += part
        elif temp_sentence:  # 如果当前有缓存的部分，则将完整句子加入列表
            if temp_sentence.strip():
                merged_sentences.append(temp_sentence.strip())
            temp_sentence = part
        else:  # 否则开始新的句子
            temp_sentence = part
    if temp_sentence:
        stripped = temp_sentence.strip()
        if stripped:  # 新增最终过滤
            merged_sentences.append(stripped)

    # 结果分段
    result = []
    current_segment = ""

    for sentence in merged_sentences:
        if not sentence:  # 新增空字符串检查
            continue
        if len(sentence) > max_chars:
            # 需要对过长的句子进行进一步拆分
            sub_sentences = split_long_sentence(sentence, max_segment_chars)
            for sub in sub_sentences:
                if len(current_segment) + len(sub) + 1 <= max_segment_chars:
                    if current_segment:
                        current_segment += " "
                    current_segment += sub
                else:
                    result.append(current_segment)
                    current_segment = sub
        else:
            # 判断是否可以加入当前分段
            if len(current_segment) + len(sentence) + 1 <= max_segment_chars:
                if len(current_segment) + len(sentence) + 1 <= max_chars:
                    if current_segment:
                        current_segment += " "
                    current_segment += sentence
                else:
                    result.append(current_segment)
                    current_segment = sentence
            else:
                result.append(current_segment)
                current_segment = sentence

    if current_segment and current_segment.strip():
        result.append(current_segment.strip())

    return result


def split_long_sentence(sentence, max_segment_chars):
    """
    将过长的句子按空格或合适位置拆分，避免影响语义。
    增加了对连词、引导词和介词的特殊处理，避免拆分不必要的部分。
    优先考虑句末或句首特殊词汇进行拆分。
    """

    # 定义连词、引导词、介词的词表（可以根据需要扩展）
    conjunctions = ["and", "or", "but", "so", "yet", "for", "nor"]
    prepositions = ["by", "on", "at", "in", "with", "about", "to", "from", "of"]
    relative_pronouns = ["who", "which", "that", "whom"]
    adverbs = ["when", "why", "where", "how", "what"]

    # 将句子按空格分割成单词
    words = sentence.split(" ")

    # 如果句子没有超过最大字符数，直接返回原句
    if len(sentence) <= max_segment_chars:
        return [sentence]  # 如果没有超过限制，直接返回原句子

    # 如果超过最大字符限制，尝试按语义合理拆分
    result = []
    current_part = ""
    special_word_found = False  # 用于标记是否遇到特殊词汇

    # 遍历单词，尽量在连词、介词或引导词处拆分
    for word in words:
        # 如果当前部分加上单词不会超过最大字符数，继续拼接
        if len(current_part) + len(word) + 1 <= max_segment_chars:
            if current_part:
                current_part += " "
            current_part += word
        else:
            # 如果当前部分已经达到限制，检查是否遇到特殊词汇
            if not special_word_found:
                # 如果没有找到特殊词汇，直接拼接当前部分（避免不必要拆分）
                current_part += " " + word
            else:
                # 优先考虑在连词、介词、引导词处拆分
                if any(conj in word.lower() for conj in conjunctions) or \
                        any(prep in word.lower() for prep in prepositions) or \
                        any(rel in word.lower() for rel in relative_pronouns) or \
                        any(adv in word.lower() for adv in adverbs):
                    # 如果是句末或句首的特殊词汇，合并
                    if words.index(word) == len(words) - 1 or words.index(word) == 0:
                        current_part += " " + word
                    else:
                        if current_part:
                            result.append(current_part)
                        current_part = word
                else:
                    # 如果没有找到特殊词汇，继续拼接
                    current_part += " " + word

            # 如果遇到特殊词汇，标记为已找到
            if any(conj in word.lower() for conj in conjunctions) or \
                    any(prep in word.lower() for prep in prepositions) or \
                    any(rel in word.lower() for rel in relative_pronouns) or \
                    any(adv in word.lower() for adv in adverbs):
                special_word_found = True

    # 最后处理剩余的部分
    if current_part:
        result.append(current_part)

    return result


async def generate_audio_and_subtitles(tts, text, page_number, filename_prefix, setting):
    subtitle_file, audio_clips = None, []
    if setting.subtitle_polishing_enabled:
        from pptflow.utils.text_polishing import get_polishing_text
        text_segments = get_polishing_text(text, setting)
    else:
        text_segments = split_text(text, language=setting.language, max_chars=setting.subtitle_length)
    text_segments = [segment for segment in text_segments if segment.strip()]
    logger.info(f'text_segments: {text_segments}')

    audio_file_path = os.path.join(setting.audio_dir_path, f"{filename_prefix}-P{page_number}.mp3")
    subtitle_file_path = os.path.join(setting.audio_dir_path, f'{filename_prefix}-P{page_number}.srt')

    # Check if the audio file already exists and has the same content as the current text
    if setting.audio_local_cache_enabled and not audio_file_do_replace_check(audio_file_path, ''.join(text_segments)):
        logger.info(f'{audio_file_path} already exists and the text content does not change, then skip this step.')
        return

    try:
        subtitle_file = open(subtitle_file_path, 'w')
        current_time = 0
        tasks = []  # List to hold tasks for concurrent execution

        for idx, segment_text in enumerate(text_segments):
            # file path to save the audio clip based on the current segment
            segment_audio_file_path = os.path.join(setting.audio_dir_path,
                                                   f'{filename_prefix}-P{page_number}-S{idx + 1}.mp3')
            # Add the task to the list
            tasks.append(
                generate_audio_clip(tts, segment_text, segment_audio_file_path, setting)
            )

        # Run the tasks concurrently
        results = await asyncio.gather(*tasks)

        # Process the results
        for idx, result in enumerate(results):
            if not result:
                logger.error(f"Error generating audio for segment {idx + 1}")
                continue
            segment_audio = AudioFileClip(result)
            start_time = current_time
            end_time = start_time + segment_audio.duration
            subtitle_file.write(f"{idx + 1}\n")
            subtitle_file.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            subtitle_file.write(f"{text_segments[idx]}\n\n")
            current_time = end_time
            audio_clips.append(segment_audio)

        # Save the final audio clip to the specified path
        final_audio = concatenate_audioclips(audio_clips)
        final_audio.write_audiofile(audio_file_path, logger=None)
        add_audio_file_text_cache(audio_file_path, ''.join(text_segments))

    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
    finally:
        if subtitle_file:
            subtitle_file.close()
        for clip in audio_clips:
            clip.close()
        # Clean up temporary files
        for i in range(len(text_segments)):
            segment_audio_file_path = os.path.join(setting.audio_dir_path,
                                                   f'{filename_prefix}-P{page_number}-S{i + 1}.mp3')
            if os.path.exists(segment_audio_file_path):
                os.remove(segment_audio_file_path)


async def generate_audio_clip(tts, text, output_file, setting):
    try:
        await tts(text, output_file, setting)
        return output_file  # Return the path of the generated file
    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
        return None


def format_time(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


if __name__ == '__main__':
    text = "So what's beneath this surface? For me, it's about connection, comfort, and even quiet rebellion. Eating " \
           "at 1 a.m. when others sleep breaks the rules—but gently. It creates space for real talk, laughter, " \
           "or silence. It's a place where we can feel warmth—through the food, through the company, through the " \
           "familiarity. This is deep culture. It's not seen—but it's felt. "
    print(split_text(text, language='en', max_chars=30))
    # setting = Setting()
    # setting.external_notes_path = "D:/workspace/ppt/《坏情绪也没关系》于曈.docx"
    # # images = process_image_dir("C:/Users/19622/AppData/Roaming/pptflow/temp/image", "孩子如何合理使用DeepSeek")
    # # for image in images:
    # #     print(image)
    # asyncio.run(ppt_note_to_audio(tts=None, input_path="D:/workspace/ppt/《坏情绪也没关系》于曈.pptx", setting=setting))
