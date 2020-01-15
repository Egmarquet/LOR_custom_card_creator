import sys, os, re, time
sys.path.append("..")
from wand.font import Font
from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from wand.display import display
from resources import database, assets, fonts
import image_tools

"""
Note all bounding positions are in the format
(x, y, w, h)
"""
class Card(object):
    def __init__(self, session_id, card_id):
        self.session_id = session_id
        self.card_id = card_id
        self.CARD_SIZE = (680, 1024)
        self.POS_MANA = (23, 33, 135, 137)

    def compose_text_body(self, text):
        """
        Return a list of tuples:
        [(text, Font, symbol if applicable)]

        Text tags should be in the form:
            <k> text </k> for keywords
            <b> text </b> for unit references
        """

        kb = re.compile('(\<k\>.+\</k\>)|(\<b\>.+\</b\>)')
        split = [i for i in re.split(kb, text) if i]
        out = []

        for substring in split:
            k = re.match('\<k\>(.+)\</k\>', substring)
            b = re.match('\<b\>(.+)\</b\>', substring)
            if k:
                out.append(('keyword', k.group(1)))
            elif b:
                out.append(('reference', b.group(1)))
            else:
                out.append((None, substring))

        return out

class UnitCard(Card):
    def __init__(self, session_id, card_id):
        super().__init__(session_id, card_id)
        self.POS_HP = (45, 881, 85, 63)
        self.POS_PWR = (553, 881, 85, 63)
        self.POS_TRIBE = (245, 35, 210, 49)
        # For some reason the font height for tribes doesn't work correctly,
        # therefore the bounding box is shifted down slighty from y=28 to y=35

    def construct(self):
        card = database.get_card(self.session_id, self.card_id)
        session_id, card_id, card_type, name, hp, mana, pwr, card_text, lvl_up_text, tribe, region, img_path = card[0]

        base = Image(width=self.CARD_SIZE[0], height=self.CARD_SIZE[1])

        # Adding base image

        # Adding Frame
        with Image(filename=assets.UNIT_FRAMES[card_type]) as frame:
            base.composite(frame)

        #
        # Adding static position text:
        # mana, hp, pwr, tribe text
        #
        if mana:
            image_tools.composite_text(base, mana, fonts.FONT_MANA, self.POS_MANA)
        if hp:
            image_tools.composite_text(base, hp, fonts.FONT_HPPWR, self.POS_HP)
        if pwr:
            image_tools.composite_text(base, pwr, fonts.FONT_HPPWR, self.POS_PWR)
        if tribe:
            with Image(filename=assets.TRIBE) as tribe_base:
                center = image_tools.center_align((0,0,tribe_base.width, tribe_base.height),(0,0,self.CARD_SIZE[0],self.CARD_SIZE[1]))
                base.composite(tribe_base, left=center[0], top=11)
                image_tools.composite_text(base, tribe.upper(), fonts.FONT_TRIBE, self.POS_TRIBE, kerning=3)

        # Composing inner text elements

        # Inner text, Keyword icons, and 
        display(base)


if __name__ == '__main__':
    card = UnitCard(13, 3)
    s = time.time()
    card.construct()
    print(time.time() - s)
