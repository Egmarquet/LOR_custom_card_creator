import sys
sys.path.append("..")
import tools
from resources import definitions, enums, fonts, frames, keywords, regions
from wand.font import Font
from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from wand.display import display
from resources.definitions import CARD_SIZE

def draw_mana(mana):
    base = Image(width=CARD_SIZE[0], height=CARD_SIZE[1])
    tools.draw_text_in_box(base, mana, fonts.FONT_MANA, definitions.POS_MANA)
    return base

def draw_hp(hp):
    base = Image(width=CARD_SIZE[0], height=CARD_SIZE[1])
    tools.draw_text_in_box(base, hp, fonts.FONT_HPPWR, definitions.POS_HP)
    return base

def draw_pwr(pwr):
    base = Image(width=CARD_SIZE[0], height=CARD_SIZE[1])
    tools.draw_text_in_box(base, hp, fonts.FONT_HPPWR, definitions.POS_PWR)
    return base

def draw_tribe(tribe_text):
    base = Image(width=CARD_SIZE[0], height=CARD_SIZE[1])
    tribe_base = Image(filename=frames.TRIBE)
    center = int((CARD_SIZE[0] - tribe_base.width)/2.0)
    with tribe_base:
        base.composite(tribe_base, top=11, left=center)
        tools.draw_text_in_box(base, tribe_text.upper(), fonts.FONT_TRIBE, definitions.POS_TRIBE, kerning=3)
    return base

def draw_region(region):
    base = Image(width=CARD_SIZE[0], height=CARD_SIZE[1])
    if region in regions.map:
        region_img = Image(filename=regions.map[region])
        center = int((CARD_SIZE[0] - region_img.width)/2.0)
        with region_img:
            base.watermark(region_img, transparency=0.65, top=870, left=center)
    return base

img = draw_tribe('Elite')
img.save(filename="coolimg.png")
