# Author: Valley-e
# Date: 2025/2/27  
# Description:
import os
import pathlib
import sys
from dotenv import load_dotenv

load_dotenv()


def get_father_dir():
    home = pathlib.Path.home()
    system_paths = {
        'win32': home / 'AppData/Roaming',
        'linux': home / '.local/share',
        'darwin': home / 'Library/Application Support'
    }

    # 修改原来的data_path定义
    data_path = system_paths[sys.platform]
    if os.getenv('ENV') == 'dev':
        # father_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        father_dir = os.getcwd()
    else:
        father_dir = os.path.join(data_path, 'pptflow')
    return father_dir


def get_absolute_data_path(path_name: str):
    return os.path.join(get_father_dir(), path_name)


if __name__ == '__main__':
    print(get_absolute_data_path('log'))
