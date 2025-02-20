from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.config  import change_settings

change_settings({'IMAGEMAGICK_BINARY': r'D:\workspace\pptflow\ImageMagick\magick.exe'})
print(TextClip.list("font"))

# 加载图片、音频和字幕
image_path = r'D:\workspace\pptflow\temp\image\test-P1.png'
audio_path = r'D:\workspace\pptflow\temp\audio\test-P1.mp3'
subtitles_path = r'D:\workspace\pptflow\temp\audio\test-P1.srt'

# 创建视频剪辑
image_clip = ImageClip(image_path).set_duration(AudioFileClip(audio_path).duration)

# 加载音频
audio_clip = AudioFileClip(audio_path)

# 将音频添加到视频剪辑
video_clip = image_clip.set_audio(audio_clip)

# 添加字幕
subtitles = SubtitlesClip(subtitles_path, lambda txt: TextClip(txt, font='Microsoft-YaHei-&-Microsoft-YaHei-UI', fontsize=24, color='white',stroke_color='black',stroke_width=0.5,method='caption',size=(video_clip.w*0.9, None)))
video_with_subtitles = CompositeVideoClip([video_clip, subtitles.set_position(('center', video_clip.h*0.85))])

# 导出最终视频
video_with_subtitles.write_videofile('output_video.mp4', fps=10)