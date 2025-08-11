from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import os, pysrt
from datetime import datetime as dt
from modules.videoSize import get_video_dimensions

os.environ["IMAGEIO_FFMPEG_EXE"] = r"C:\path\to\ffmpeg.exe"  # make sure this points to ffmpeg.exe

def add_caption_overlay(video_path, srt_path):
    video_filename = os.path.splitext(os.path.basename(video_path))[0]
    video = VideoFileClip(video_path)
    vw, vh = get_video_dimensions(video_path)

    subs = pysrt.open(srt_path)
    reference_date = dt(1900, 1, 1)

    clips = []
    margin = 80         # distance from bottom
    text_width = vw - 160  # leave side margins so wrapping looks good

    for caption in subs:
        start_dt = dt.combine(reference_date, caption.start.to_time())
        end_dt   = dt.combine(reference_date, caption.end.to_time())
        start_s  = (start_dt - reference_date).total_seconds()
        dur_s    = (end_dt - start_dt).total_seconds()

        caption_text = caption.text_without_tags.replace("\n"," ").strip()
        if not caption_text:
            continue

        txt = TextClip(
            text=caption_text,
            method="caption",           # wrap to width
            size=(text_width, None),    # width fixed, height auto
            font="fonts/LibertinusMath.otf",
            font_size=60,
            color="white",
            stroke_color="black",       # better readability
            stroke_width=2,
            bg_color="black",              # set to "black" if you want a strip behind text
            horizontal_align="center",
            vertical_align="center",
            margin=(None, 10)        # text alignment within the box
        )

        # EITHER: exact bottom with offset
        # pos = lambda t: ("center", vh - margin - txt.h)   # stable placement

        # OR: the built-in bottom anchor (simpler)
        pos = ("center", "bottom")

        margin=150
        txt = txt.with_position(lambda t: ("center", video.h - margin - txt.h)).with_start(start_s).with_duration(dur_s)
        clips.append(txt)

    final = CompositeVideoClip([video] + clips).with_duration(video.duration)
    final.write_videofile(f"output/{video_filename}.mp4")
