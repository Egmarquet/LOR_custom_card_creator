"""
Card templates
"""
SPELL_SLOW_COMMON = None
SPELL_SLOW_RARE = None
SPELL_SLOW_EPIC = None
SPELL_SLOW_NR = None

"""
Spell fonts and sizes

The user editable SPELL_TEXT space is the sum of the three:

SPELL_NAME
+ PADDING_0
+ KEYWORD_ICONS (one large or multiple small)
+ PADDING_1
+ SPELL DESCRIPTION

The constraining height and width ar
"""
# Fonts
SPELL_NAME_FONT = None
SPELL_DESCRIPTION_FONT = "./templates/fonts/Padauk/Fonts/padauk-book.ttf"

# Boundries
SPELL_TEXT_MAX_HEIGHT = 310
SPELL_TEXT_MAX_WIDTH = 500

# Font sizes
SPELL_DESCRIPTION_MAX_FONT_SIZE = 36
SPELL_DESCRIPTION_MIN_FONT_SIZE = 10
SPELL_NAME_MAX_FONT_SIZE = None
SPELL_NAME_MIN_FONT_SIZE = None
SPELL_MANA_COST_FONT_SIZE = None

"""
Spell Image positions
"""
SPELL_IMG_SIZE = (463,463)
SPELL_IMG_POS = (106,61)
#mana cost positions for single and double digits
SPELL_MANA_POS_SD = (0,0)
SPELL_MANA_POS_DD = (0,0)
