# tiktok-caption-generator-fix
improved version of of lernEarnBern's Tiktok-Caption-Generator

# usage
import caption_generator.py, and create an instance of Caption_Generator(). Example code below.

the add_captions() method only takes 2 arguments. The path of the file you want to add captions to, and the name of the file (used for exporting.) That's it!

```
from folder.caption_generator import caption_generator
Caption_Generator = Caption_Generator()
Caption_Generator.add_captions('input/test_clip_shortened.mp4', 'test_clip_shortened')
```
