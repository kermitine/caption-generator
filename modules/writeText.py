from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import os
import pysrt
from datetime import datetime as dt
from .videoSize import get_video_dimensions

os.environ["IMAGEIO_FFMPEG_EXE"] = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\ffmpeg.exe"

def add_caption_overlay(video_path, srt_path):
    video_filename = os.path.splitext(os.path.basename(video_path))[0]

    video = VideoFileClip(video_path)

    subs = pysrt.open(srt_path)

    reference_date = dt(1900, 1, 1)

    clips = []

    for caption in subs:
        start_time = dt.combine(reference_date, caption.start.to_time())
        start_time_float = (start_time - reference_date).total_seconds()
        end_time = dt.combine(reference_date, caption.end.to_time())
        caption_text = caption.text_without_tags

        duration_seconds = (end_time - start_time).total_seconds()

        screensize = get_video_dimensions(video_path)
        

        text = TextClip(text=caption_text, font_size=40, color='white', font='LibertinusMath.otf', method='caption', stroke_color='white', size=screensize, vertical_align='bottom', bg_color='white')

        text = text.with_position(lambda t: ('center', 120-t) ).with_start(start_time_float).with_duration(duration_seconds)

        clips.append(text)

    final_clip = CompositeVideoClip([video] + clips)
    final_clip = final_clip.with_duration(video.duration)
    final_clip.write_videofile(f'output/{video_filename}.mp4')

    