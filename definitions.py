import os
from PIL import Image
from PIL import ImageFont

# Root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(ROOT_DIR, 'templates', 'lor-template-pack')
FONTS_DIR = os.path.join(ROOT_DIR, 'fonts')

# fonts
FONT_BEAUFORT = os.path.join(FONTS_DIR, "Beaufort for LOL Bold.ttf")
FONT_UNIVERSL = os.path.join(FONTS_DIR, "UniverseLSTStd-UltraCn.ttf")

# font sizes
FONT_SZ_MANA = 90
FONT_SZ_HPPWR = 70
FONT_SZ_DESCRIPTION = 32
FONT_SZ_KEYWORD = NotImplementedError()

# Static text positions
#SD is single digit, DD is double digit
POS_MANA_SD = (66,38)
POS_MANA_DD = (36,38)
POS_HP_SD = (72, 865)
POS_HP_DD = (36, 850)

# Colors:
WHITE = (255,255,255)
OFF_WHITE = (246,227,227)
BLACK = (0,0,0)

# Champion Frames
FRAME_CHAMPION_BASE = os.path.join(TEMPLATE_DIR, 'lor-champion-large.mse-style', 'frame1gem.png')
FRAME_CHAMPION_LVLUP = os.path.join(TEMPLATE_DIR, 'lor-champion-large.mse-style', 'frame2gem.png')
BAR_CHAMPION_LVLUP = os.path.join(TEMPLATE_DIR, 'lor-champion-large.mse-style', 'levelupbar.png')

# Champion card standards
IMG_SIZE_CHAMPION = (623, 906)
IMG_PLACEMENT = (28,57)

# Follower Frames
FRAME_FOLLOWER_COMMON = os.path.join(TEMPLATE_DIR, 'lor-follower-large.mse-style', 'framecommon.png')
FRAME_FOLLOWER_RARE = os.path.join(TEMPLATE_DIR, 'lor-follower-large.mse-style', 'framerare.png')
FRAME_FOLLOWER_EPIC = os.path.join(TEMPLATE_DIR, 'lor-follower-large.mse-style', 'frameepic.png')
FRAME_FOLLOWER_NO_GEM = os.path.join(TEMPLATE_DIR, 'lor-follower-large.mse-style', 'framegemless.png')
