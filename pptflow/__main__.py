import sys

from pptflow.ppt2video import ppt_to_video

if __name__ == "__main__":
    # 获取命令行参数
    args = sys.argv[1:]  # 忽略第一个参数（脚本名称）
    if not args:
        print("请提供参数。")
        exit
    ppt_to_video(args[0], args[1])