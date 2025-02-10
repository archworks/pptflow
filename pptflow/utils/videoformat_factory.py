# Author: Valley-e
# Date: 2025/2/9  
# Description:
import subprocess


def convert_video_with_audio(input_mp4, output_file, video_codec='libx264', audio_codec='aac'):
    """
    将 MP4 转换为其他格式的视频（保留音频）

    参数：
    - input_mp4: 输入 MP4 文件路径
    - output_file: 输出文件路径（扩展名决定格式，如 .mkv, .avi）
    - video_codec: 视频编码器（默认 libx264）
    - audio_codec: 音频编码器（默认 aac）
    """
    try:
        command = [
            'ffmpeg',
            '-i', input_mp4,
            '-c:v', video_codec,  # 指定视频编码器
            '-c:a', audio_codec,  # 指定音频编码器
            '-strict', 'experimental',  # 某些编码器需要此参数（如早期 AAC）
            '-y',  # 覆盖输出文件（可选）
            output_file
        ]
        subprocess.run(command, check=True)
        print(f"转换成功: {input_mp4} -> {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"转换失败: {e}")
    except FileNotFoundError:
        print("请确保已安装 FFmpeg 并添加到系统路径！")


if __name__ == '__main__':
    # 示例：将 input.mp4 转换为 output.mkv（使用默认编码器）
    convert_video_with_audio("test.mp4", "output.avi")
