import sys, os
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates')
"""
Holds all paths to all card assets
"""

"""
------------
FRAMES PATHS
------------
"""
UNIT_FRAMES = os.path.join(TEMPLATES_DIR, 'unit_frames')
OTHER = os.path.join(TEMPLATES_DIR, 'other')
TRIBE = os.path.join(OTHER, 'tribe.png')
DARKNESS = os.path.join(OTHER, 'theencrouchingdarkness.png')
UNIT_FRAMES = {
    'unit_norare': os.path.join(UNIT_FRAMES, 'framegemless.png'),
    'unit_common': os.path.join(UNIT_FRAMES, 'framecommon.png'),
    'unit_rare': os.path.join(UNIT_FRAMES, 'framerare.png'),
    'unit_epic': os.path.join(UNIT_FRAMES, 'frameepic.png'),
    'unit_champion_base': os.path.join(UNIT_FRAMES, 'frame1gem.png'),
    'unit_champion_lvlup': os.path.join(UNIT_FRAMES, 'frame2gem.png')
}

"""
Regions
"""
REGION_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates','regions')
REGIONS = {
    'bandle city' : os.path.join(REGION_PATH, 'bandlecity.png'),
    'bilgewater' : os.path.join(REGION_PATH, 'bilgewater.png'),
    'demacia': os.path.join(REGION_PATH, 'demacia.png'),
    'freljord:': os.path.join(REGION_PATH, 'freljord.png'),
    'ionia' : os.path.join(REGION_PATH, 'ionia.png'),
    'noxus' : os.path.join(REGION_PATH, 'noxus.png'),
    'piltover zaun': os.path.join(REGION_PATH, 'piltoverzaun.png'),
    'runeterra' : os.path.join(REGION_PATH, 'runeterra.png'),
    'shadow isles' : os.path.join(REGION_PATH, 'shadowisles.png'),
    'shurima' : os.path.join(REGION_PATH, 'shurima.png'),
    'targon' : os.path.join(REGION_PATH, 'targon.png'),
    'void' : os.path.join(REGION_PATH, 'void.png')
}

"""
CARD KEYWORDS
"""
