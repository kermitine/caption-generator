import os
import math
import whisper
from datetime import datetime, timedelta

def _chunks_by_words(words, max_words):
    for i in range(0, len(words), max_words):
        yield words[i:i+max_words]

def _format_srt_time(seconds_float: float) -> str:
    if seconds_float < 0:
        seconds_float = 0.0
    td = timedelta(seconds=seconds_float)
    base = datetime(1, 1, 1) + td
    return base.strftime("%H:%M:%S,%f")[:-3]

def transcribe_audio(
    path,
    model_size="small",
    max_words_per_caption=7,
    min_chunk_dur=1.2,
    max_chunk_dur=4.0,
    srt_dir="./SrtFiles"
):
    """
    Create an SRT with shorter, faster-updating captions by splitting each Whisper segment
    into word-limited chunks and distributing the segment's time window across those chunks.
    """
    # Load whisper
    model = whisper.load_model(model_size)
    print("Whisper model loaded.")

    # Transcribe
    result = model.transcribe(audio=path)
    segments = result.get("segments", [])

    video_filename = os.path.splitext(os.path.basename(path))[0]
    os.makedirs(srt_dir, exist_ok=True)
    srt_filename = os.path.join(srt_dir, f"{video_filename}.srt")

    # Overwrite existing file
    with open(srt_filename, "w", encoding="utf-8") as srt_file:
        srt_id = 1

        for seg in segments:
            text = (seg.get("text") or "").replace("\n", " ").strip()
            if not text:
                continue

            start = float(seg.get("start", 0.0))
            end   = float(seg.get("end", start))
            total_dur = max(0.0, end - start)
            if total_dur == 0.0:
                continue

            # Split text into word chunks
            words = text.split()
            chunk_words = list(_chunks_by_words(words, max_words_per_caption))

            # If there's just one short chunk, write it directly
            if len(chunk_words) == 1:
                st = start
                et = end
                line = " ".join(chunk_words[0]).strip()
                srt_file.write(f"{srt_id}\n{_format_srt_time(st)} --> {_format_srt_time(et)}\n{line}\n\n")
                srt_id += 1
                continue

            # Assign durations proportional to chunk word counts
            word_counts = [max(1, len(cw)) for cw in chunk_words]
            total_words = sum(word_counts)
            raw_durs = [total_dur * (wc / total_words) for wc in word_counts]

            # Clamp to min/max while keeping total_dur by rescaling
            clamped = [min(max(d, min_chunk_dur), max_chunk_dur) for d in raw_durs]
            sum_clamped = sum(clamped)
            if sum_clamped > 0:
                scale = total_dur / sum_clamped
            else:
                scale = 1.0
            durs = [d * scale for d in clamped]

            # To avoid rounding drift, ensure last end == end
            t_cursor = start
            for i, (cw, dur) in enumerate(zip(chunk_words, durs)):
                if i == len(chunk_words) - 1:
                    st = t_cursor
                    et = end
                else:
                    st = t_cursor
                    et = st + dur
                line = " ".join(cw).strip()
                srt_file.write(f"{srt_id}\n{_format_srt_time(st)} --> {_format_srt_time(et)}\n{line}\n\n")
                srt_id += 1
                t_cursor = et

    print("SRT generated:", srt_filename)
    return srt_filename
