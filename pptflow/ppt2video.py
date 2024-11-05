from dotenv import load_dotenv

load_dotenv()

import os, re, platform, time
from .ppt2audio import ppt_note_to_audio
from .clip2video import create_video_from_images_and_audio

## import tts module according to service provider
tts_service_provider = os.environ.get("TTS_SERVICE_PROVIDER")
if not tts_service_provider:
    raise NotImplementedError(f"tts服务未配置")
if tts_service_provider.lower() == "azure":
    from .tts_azure import tts
elif tts_service_provider.lower() == "xunfei":
    from .tts_xunfei import tts
else:
    raise NotImplementedError(f"不支持的tts: {tts_service_provider}")

## import ppt to image module according to os platform
os_name = platform.system()
if os_name == "Windows":
    from .ppt2image_win import ppt_to_image
elif os_name == "Linux":
    from .ppt2image_linux import ppt_to_image
elif os_name == "Darwin":  # macOS
    from .ppt2image_mac import ppt_to_image
else:
    raise NotImplementedError(f"不支持的操作系统: {os_name}")


# https://github.com/scliubit/
# azure tts quick start:https://learn.microsoft.com/zh-cn/azure/ai-services/speech-service/get-started-text-to-speech?tabs=macos%2Cterminal&pivots=programming-language-python
# azure tts sample: https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/python/console/speech_synthesis_sample.py
# How to export pptx to image (png, jpeg) in Python? https://stackoverflow.com/questions/61815883/how-to-export-pptx-to-image-png-jpeg-in-python


def process(ppt_path, video_path=None, start_page_num=None, end_page_num=None):
    start_time = time.time()
    # Specify the full path to the PowerPoint presentation
    temp_dir = os.path.join(os.getcwd(), "temp")
    image_dir_path = os.path.join(temp_dir, "image")
    audio_dir_path = os.path.join(temp_dir, "audio")

    if video_path == None:
        video_path = re.sub(r"pptx?$", "mp4", ppt_path)
        print(f'video_path:{video_path}')
    ppt_to_image(ppt_path, image_dir_path, start_page_num, end_page_num)
    ppt_note_to_audio(tts, ppt_path, audio_dir_path, start_page_num, end_page_num)
    create_video_from_images_and_audio(
        image_dir_path,
        audio_dir_path,
        ppt_path,
        video_path,
        start_page_num,
        end_page_num,
    )
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"运行时间:{elapsed_time:.2f}秒")
