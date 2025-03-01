# Author: Valley-e
# Date: 2025/2/28  
# Description:
from pptflow.config.setting import Setting
import os
from pptflow.utils import mylogger
from pptflow.utils.datapath import resource_path
logger = mylogger.get_logger(__name__)

setting = Setting()


def check_and_download(filepath, filename):
    """检查并下载文件的通用方法"""
    if os.path.exists(filepath):
        return True

    url = f"https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/{filename}"

    try:
        from tqdm import tqdm
        import requests

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))

            with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"下载 {filename}") as pbar:
                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
        return True
    except Exception as e:
        logger.error(f"下载失败: {str(e)}")
        if os.path.exists(filepath):
            os.remove(filepath)
        return False


model_path = os.path.join(resource_path("model"), setting.kokoro_module)
voice_path = os.path.join(resource_path("model"), setting.kokoro_voice_file)
check_and_download(model_path, setting.kokoro_module)
check_and_download(voice_path, setting.kokoro_voice_file)
logger.info(f"KokoroTtsService initialized with model_path={model_path}, voice_path={voice_path}")

