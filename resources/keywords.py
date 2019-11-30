import enum
import os

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates')
KEYWORD_ICONS = os.path.join(TEMPLATES_DIR,'keyword_icons')
KEYWORD_SYMBOLS = os.path.join(TEMPLATES_DIR,'keyword_symbols')

ICON_MINI = os.path.join(KEYWORD_ICONS,'keywordmini.png')
ICON_CENTER = os.path.join(KEYWORD_ICONS,'keywordmiddle.png')
ICON_LEFT = os.path.join(KEYWORD_ICONS,'keywordleft.png')
ICON_RIGHT = os.path.join(KEYWORD_ICONS,'keywordright.png')

class Keywords(enum.Enum):
    STUN = 0
    OVERWHELM = 1
    LAST_BREATH = 2
    DOUBLE_ATTACK = 3
    REGENERATION = 4
    TOUGH = 5
    FROSTBITE = 6
    ELUSIVE = 7
    LIFESTEAL = 8
    QUICK_ATTACK = 9
    BARRIER = 10
    EPHEMERAL = 11
    CHALLENGER = 12
    FLEETING = 13
    FEARSOME = 14
    CANT_BLOCK = 15
    BURST = 16
    FAST = 17
    SLOW = 18
    SKILL = 19

symbols = {
    Keywords.STUN : os.path.join(KEYWORD_SYMBOLS, 'stun.png'),
    Keywords.OVERWHELM: os.path.join(KEYWORD_SYMBOLS, 'overwhelm.png'),
    Keywords.LAST_BREATH: os.path.join(KEYWORD_SYMBOLS, 'lastbreath.png'),
    Keywords.DOUBLE_ATTACK: os.path.join(KEYWORD_SYMBOLS, 'doubleattack.png'),
    Keywords.REGENERATION: os.path.join(KEYWORD_SYMBOLS, 'regeneration.png'),
    Keywords.TOUGH: os.path.join(KEYWORD_SYMBOLS, 'tough.png'),
    Keywords.FROSTBITE: os.path.join(KEYWORD_SYMBOLS, 'frostbite.png'),
    Keywords.ELUSIVE: os.path.join(KEYWORD_SYMBOLS, 'elusive.png'),
    Keywords.LIFESTEAL: os.path.join(KEYWORD_SYMBOLS, 'lifesteal.png'),
    Keywords.QUICK_ATTACK: os.path.join(KEYWORD_SYMBOLS, 'quickattack.png'),
    Keywords.BARRIER: os.path.join(KEYWORD_SYMBOLS, 'barrier.png'),
    Keywords.EPHEMERAL: os.path.join(KEYWORD_SYMBOLS, 'ephemeral.png'),
    Keywords.CHALLENGER: os.path.join(KEYWORD_SYMBOLS, 'challenger.png'),
    Keywords.FLEETING: os.path.join(KEYWORD_SYMBOLS, 'fleeting.png'),
    Keywords.FEARSOME: os.path.join(KEYWORD_SYMBOLS, 'fearsome.png')
}

icons = {
    Keywords.OVERWHELM: os.path.join(KEYWORD_ICONS, 'keywordoverwhelm.png'),
    Keywords.DOUBLE_ATTACK: os.path.join(KEYWORD_ICONS, 'keyworddoubleattack.png'),
    Keywords.REGENERATION: os.path.join(KEYWORD_ICONS, 'keywordregeneration.png'),
    Keywords.TOUGH: os.path.join(KEYWORD_ICONS, 'keywordtough.png'),
    Keywords.ELUSIVE: os.path.join(KEYWORD_ICONS, 'keywordelusive.png'),
    Keywords.LIFESTEAL: os.path.join(KEYWORD_ICONS, 'keywordlifesteal.png'),
    Keywords.QUICK_ATTACK: os.path.join(KEYWORD_ICONS, 'keywordquickattack.png'),
    Keywords.BARRIER: os.path.join(KEYWORD_ICONS, 'keywordbarrier.png'),
    Keywords.EPHEMERAL: os.path.join(KEYWORD_ICONS, 'keywordephemeral.png'),
    Keywords.CHALLENGER: os.path.join(KEYWORD_ICONS, 'keywordchallenger.png'),
    Keywords.FLEETING: os.path.join(KEYWORD_ICONS, 'keywordfleeting.png'),
    Keywords.FEARSOME: os.path.join(KEYWORD_ICONS, 'keywordfearsome.png'),
    Keywords.CANT_BLOCK: os.path.join(KEYWORD_ICONS, 'keywordcantblock.png'),
    Keywords.BURST: os.path.join(KEYWORD_ICONS, 'keywordburst.png'),
    Keywords.FAST: os.path.join(KEYWORD_ICONS, 'keywordfast.png'),
    Keywords.SLOW: os.path.join(KEYWORD_ICONS, 'keywordslow.png')
}

symbols_map = {
 'stun': Keywords.STUN,
 'overwhelm': Keywords.OVERWHELM,
 'last breath': Keywords.LAST_BREATH,
 'double attack': Keywords.DOUBLE_ATTACK,
 'regeneration': Keywords.REGENERATION,
 'tough': Keywords.TOUGH,
 'frostbite': Keywords.FROSTBITE,
 'elusive': Keywords.ELUSIVE,
 'lifesteal': Keywords.LIFESTEAL,
 'quick attack': Keywords.QUICK_ATTACK,
 'barrier': Keywords.BARRIER,
 'ephemeral': Keywords.EPHEMERAL,
 'challenger': Keywords.CHALLENGER,
 'fleeting': Keywords.FLEETING,
 'fearsome': Keywords.FEARSOME,
 "can't block": Keywords.CANT_BLOCK,
 'burst': Keywords.BURST,
 'fast': Keywords.FAST,
 'slow': Keywords.SLOW
}
