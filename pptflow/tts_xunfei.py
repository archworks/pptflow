# coding=UTF-8
import subprocess

def tts(text, output_audio_filename):
    result = subprocess.run(["java", "-Dfile.encoding=UTF-8","-jar", "java/iflytek-tts.jar", text, output_audio_filename], 
        check=True)
    if result.returncode != 0:
        return False
    return True

if __name__ == "__main__":
    tts("落霞与孤鹜齐飞，秋水共长天一色", "D:\\test.mp3")