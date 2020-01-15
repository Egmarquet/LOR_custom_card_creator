import re, sys, os, time
sys.path.append('..')
from wand.font import Font
from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from wand.display import display

from src import tools
from resources import fonts, database
if __name__ == '__main__':
    print("Hello World")

    start_time = time.time()
    base = Image(height=1024, width=680)
    tools.draw_text_in_box(base, "2asdfasdkjfnaskldnjf0", fonts.FONT_MANA,  (23,33,158,170))
    print(time.time() - start_time)
