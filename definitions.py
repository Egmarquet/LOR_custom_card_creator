import os
from PIL import Image
from PIL import ImageFont
import enum


# Root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(ROOT_DIR, 'templates', 'lor-template-pack')
FONTS_DIR = os.path.join(ROOT_DIR, 'fonts')

# fonts
FONT_BEAUFORT = os.path.join(FONTS_DIR, "Beaufort for LOL Bold.ttf")
FONT_UNIVERSL = os.path.join(FONTS_DIR, "UniversLTStd-UltraCn.otf")
FONT_PADUK = os.path.join(FONTS_DIR, "padauk-book.ttf")
FONT_PADUK_BOLD = os.path.join(FONTS_DIR, "padauk-bold.ttf")

# font sizes
FONT_SZ_MANA = 90
FONT_SZ_HPPWR = 70
FONT_SZ_DESCRIPTION = 41
FONT_SZ_KEYWORD = NotImplementedError()

# Static text positions
POS_MANA = (23,33,158,170)
POS_HP = (45, 881, 130, 944)
POS_PWR = (553, 881, 638, 944)
IMG_SIZE_CHAMPION = (623, 906)
IMG_PLACEMENT = (28,57)

# Text type enums
class TextType(enum.Enum):
    TEXT = 0
    KEYWORD = 1
    REF = 2

# Colors:
WHITE = (255,255,255)
OFF_WHITE = (246,227,227)
BLACK = (0,0,0)
KEYWORD_GOLD = (250,214,90)
KEYWORD_BLUE = (73,160,248)
DESCRIPTION_GREY = (225,238,236)

# Max widths:
CARD_WIDTH = 680
CARD_HEIGHT = 1024
MAX_WIDTH = 550
MAX_DEPTH = 860

# Champion Frames
FRAME_CHAMPION_BASE = os.path.join(TEMPLATE_DIR, 'lor-champion-large.mse-style', 'frame1gem.png')
FRAME_CHAMPION_LVLUP = os.path.join(TEMPLATE_DIR, 'lor-champion-large.mse-style', 'frame2gem.png')
BAR_CHAMPION_LVLUP = os.path.join(TEMPLATE_DIR, 'lor-champion-large.mse-style', 'levelupbar.png')

#
DARKNESS_PATH = os.path.join(TEMPLATE_DIR,'lor-champion-large.mse-style','theencrouchingdarkness.png')
# Champion card standards

# Follower Frames
FRAME_FOLLOWER_COMMON = os.path.join(TEMPLATE_DIR, 'lor-follower-large.mse-style', 'framecommon.png')
FRAME_FOLLOWER_RARE = os.path.join(TEMPLATE_DIR, 'lor-follower-large.mse-style', 'framerare.png')
FRAME_FOLLOWER_EPIC = os.path.join(TEMPLATE_DIR, 'lor-follower-large.mse-style', 'frameepic.png')
FRAME_FOLLOWER_NO_GEM = os.path.join(TEMPLATE_DIR, 'lor-follower-large.mse-style', 'framegemless.png')

# Keyword Symbols (for text)
KEYWORD_SYMBOL_STUN =  os.path.join(TEMPLATE_DIR, 'lor-symbol.mse-symbol-font', 'stun.png')
KEYWORD_SYMBOL_OVERWHELM = os.path.join(TEMPLATE_DIR, 'lor-symbol.mse-symbol-font', 'overwhelm.png')
KEYWORD_SYMBOL_LASTBREATH = os.path.join(TEMPLATE_DIR, 'lor-symbol.mse-symbol-font', 'lastbreath.png')
KEYWORD_SYMBOL_DOUBLEATTACK = os.path.join(TEMPLATE_DIR, 'lor-symbol.mse-symbol-font', 'doubleattack.png')
KEYWORD_SYMBOL_REGENERATION = os.path.join(TEMPLATE_DIR, 'lor-symbol.mse-symbol-font', 'regeneration.png')
KEYWORD_SYMBOL_TOUGH = os.path.join(TEMPLATE_DIR, 'lor-symbol.mse-symbol-font', 'tough.png')
KEYWORD_SYMBOL_FROSTBITE = os.path.join(TEMPLATE_DIR, 'lor-symbol.mse-symbol-font', 'frostbite.png')
KEYWORD_SYMBOL_ELUSIVE = os.path.join(TEMPLATE_DIR, 'lor-symbol.mse-symbol-font', 'elusive.png')
KEYWORD_SYMBOL_LIFESTEAL = os.path.join(TEMPLATE_DIR, 'lor-symbol.mse-symbol-font', 'lifesteal.png')
KEYWORD_SYMBOL_QUICKATTACK = os.path.join(TEMPLATE_DIR, 'lor-symbol.mse-symbol-font', 'quickattack.png')
KEYWORD_SYMBOL_BARRIER = os.path.join(TEMPLATE_DIR, 'lor-symbol.mse-symbol-font', 'barrier.png')
KEYWORD_SYMBOL_EPHEMERAL = os.path.join(TEMPLATE_DIR, 'lor-symbol.mse-symbol-font', 'ephemeral.png')
KEYWORD_SYMBOL_CHALLENGER = os.path.join(TEMPLATE_DIR, 'lor-symbol.mse-symbol-font', 'challenger.png')
KEYWORD_SYMBOL_FLEETING = os.path.join(TEMPLATE_DIR, 'lor-symbol.mse-symbol-font', 'fleeting.png')
KEYWORD_SYMBOL_FEARSOME = os.path.join(TEMPLATE_DIR, 'lor-symbol.mse-symbol-font', 'fearsome.png')

# If text is processed
keyword_symbols_map = {
 'stun': KEYWORD_SYMBOL_STUN,
 'overwhelm': KEYWORD_SYMBOL_OVERWHELM,
 'last breath': KEYWORD_SYMBOL_LASTBREATH,
 'double attack': KEYWORD_SYMBOL_DOUBLEATTACK,
 'regeneration': KEYWORD_SYMBOL_REGENERATION,
 'tough': KEYWORD_SYMBOL_TOUGH,
 'frostbite': KEYWORD_SYMBOL_FROSTBITE,
 'elusive': KEYWORD_SYMBOL_ELUSIVE,
 'lifesteal': KEYWORD_SYMBOL_LIFESTEAL,
 'quick attack': KEYWORD_SYMBOL_QUICKATTACK,
 'barrier': KEYWORD_SYMBOL_BARRIER,
 'ephemeral': KEYWORD_SYMBOL_EPHEMERAL,
 'challenger': KEYWORD_SYMBOL_CHALLENGER,
 'fleeting': KEYWORD_SYMBOL_FLEETING,
 'fearsome': KEYWORD_SYMBOL_FEARSOME
}

#Keyword Icons
