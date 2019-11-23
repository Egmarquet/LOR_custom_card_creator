import definitions

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class UnitCard(object):
    """
    All should be strings
    """
    def __init__(self, mana, hp, pwr, border_path, img_path):
        self.mana = mana
        self.hp = hp
        self.pwr = pwr
        self.border_path = border_path
        self.img_path = img_path

    def construct_card(self):
        border = Image.open(self.border_path)
        border_draw = ImageDraw.Draw(border)
        # Construct mana cost:
        font = ImageFont.truetype(definitions.FONT_BEAUFORT, definitions.FONT_SZ_MANA)

        # Drawing mana
        if len(self.mana) == 1:
            border_draw.text(definitions.POS_MANA_SD, self.mana, font=font, fill=definitions.OFF_WHITE)
        elif len(self.mana) == 2:
            border_draw.text(definitions.POS_MANA_DD, self.mana, font=font, fill=definitions.OFF_WHITE)

        # Drawing health
        font = ImageFont.truetype(definitions.FONT_BEAUFORT, definitions.FONT_SZ_HPPWR)
        if len(self.hp) == 1:
            border_draw.text(definitions.POS_HP_SD, self.hp, font=font, fill=definitions.OFF_WHITE)
        if len(self.hp) == 2:
            raise NotImplementedError()
            
        border.save("./test.png")

    def construct_card_tester(self):

        border = Image.open(self.border_path)
        border_draw = ImageDraw.Draw(border)
        # Construct mana cost:
        font = ImageFont.truetype(definitions.FONT_BEAUFORT, definitions.FONT_SZ_MANA)

        for i in range(10,20):
            copy = border.copy()
            copy_draw = ImageDraw.Draw(copy)
            copy_draw.text(definitions.POS_MANA_DD, str(i), font=font, fill=(255,255,255))
            copy.save(f"test_{i}.png")



if __name__ == '__main__':
    uc = UnitCard("4","3","3",definitions.FRAME_CHAMPION_LVLUP,"")
    uc.construct_card()
