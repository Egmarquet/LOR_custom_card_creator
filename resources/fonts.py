import os
from wand.image import Image
from wand.drawing import Drawing

FONTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),'fonts')
BEAUFORT = os.path.join(FONTS_DIR, "Beaufort for LOL Bold.ttf")
UNIVERSL = os.path.join(FONTS_DIR, "UniversLTStd-UltraCn.otf")
PADUK = os.path.join(FONTS_DIR, "padauk-book.ttf")
HR = os.path.join(FONTS_DIR, "HLR.ttf")
USM = os.path.join(FONTS_DIR, "ultimate-serial-medium.ttf")

# standard font sizes
FONT_SZ_MANA = 90
FONT_SZ_HPPWR = 70
FONT_SZ_TEXT = 37
FONT_SZ_NAME = 70 # need to look this oneup
FONT_SZ_KEYWORD = 40
FONT_SZ_TRIBE = 37

# colors
WHITE = 'rgb(255,255,255)'
OFF_WHITE = 'rgb(246,227,227)'
KEYWORD_GOLD = 'rgb(250,214,90)'
KEYWORD_BLUE = 'rgb(73,160,248)'
KEYWORD_YELLOW = 'rgb(240,204,112)'
GREY = 'rgb(225,238,236)'
TRIBE_GREY = 'rgb(173,168,157)'

# baseline font tuples
FONT_MANA = (BEAUFORT, FONT_SZ_MANA, OFF_WHITE)
FONT_HPPWR = (BEAUFORT, FONT_SZ_HPPWR, OFF_WHITE)
FONT_TEXT = (USM, FONT_SZ_TEXT, GREY)
FONT_KEYWORD = (FONT_TEXT[0], FONT_SZ_TEXT, KEYWORD_GOLD)
FONT_REF =  (FONT_TEXT[0], FONT_SZ_TEXT, KEYWORD_BLUE)
FONT_NAME = (BEAUFORT, FONT_SZ_NAME, WHITE)
FONT_KEYWORD_ICON = (BEAUFORT, FONT_SZ_KEYWORD, KEYWORD_YELLOW)
FONT_TRIBE = (UNIVERSL, FONT_SZ_TRIBE, TRIBE_GREY)

def get_metrics(font, size):
    temp = Image(height=1,width=1)
    metrics = None
    with temp:
        with Drawing() as draw:
            draw.font = font
            draw.font_size = size
            metrics = draw.get_font_metrics(temp, " ")
    return metrics
