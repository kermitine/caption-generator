from .modules.captions import transcribe_audio
from .modules.writeText import add_caption_overlay
from pathlib import Path

class Caption_Generator:
    def add_captions(self, file_path, file_name):
        # Anchor SrtFiles to this package directory: .../caption_generator/SrtFiles
        pkg_dir = Path(__file__).resolve().parent
        srt_dir = pkg_dir / "SrtFiles"
        srt_dir.mkdir(parents=True, exist_ok=True)

        # 1) Transcribe and try to use the exact path returned
        srt_path = Path(transcribe_audio(file_path))  # transcribe_audio should return the written path

        # If transcribe_audio returned a relative path, anchor it to pkg_dir
        if not srt_path.is_absolute():
            srt_path = (pkg_dir / srt_path).resolve()

        # 2) Fallback: derive from the provided file_name (use stem, not full name)
        if not srt_path.exists():
            clip_stem = Path(file_name).stem  # "clip_1_done" from "clip_1_done.mp4"
            srt_path = srt_dir / f"{clip_stem}.srt"

        if not srt_path.exists():
            raise FileNotFoundError(f"SRT not found at {srt_path}")

        # 3) Apply captions
        add_caption_overlay(file_path, str(srt_path))

        print("\n\nVideo Complete")