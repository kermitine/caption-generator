from .modules.captions import transcribe_audio
from .modules.writeText import add_caption_overlay


class Caption_Generator():
    def add_captions(self, file_path, file_name):

        file_name = file_name
        file_path = file_path

        transcribe_audio(file_path)
        add_caption_overlay(file_path, f'srtFiles/{file_name}.srt')

        print('\n\nVideo Complete')
