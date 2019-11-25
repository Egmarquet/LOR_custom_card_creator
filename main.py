import definitions
from src import image_tools

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
        (w,h), (offset_x, offset_y) = font.font.getsize(self.mana)
        pos = image_tools.center_align((0,0,w,h), definitions.POS_MANA, vertical=True)
        border_draw.text((pos[0],pos[1]-offset_y), self.mana, font=font, fill=definitions.OFF_WHITE)

        # Drawing health
        font = ImageFont.truetype(definitions.FONT_BEAUFORT, definitions.FONT_SZ_HPPWR)
        (w,h), (offset_x, offset_y) = font.font.getsize(self.hp)
        pos = image_tools.center_align((0,0,w,h), definitions.POS_HP, vertical=True)
        border_draw.text((pos[0],pos[1]-offset_y), self.hp, font=font, fill=definitions.OFF_WHITE)

        # Drawing power
        (w,h), (offset_x, offset_y) = font.font.getsize(self.pwr)
        pos = image_tools.center_align((0,0,w,h), definitions.POS_PWR, vertical=True)
        border_draw.text((pos[0],pos[1]-offset_y), self.pwr, font=font, fill=definitions.OFF_WHITE)

        # Drawing text:
        font = ImageFont.truetype(definitions.FONT_PADUK, definitions.FONT_SZ_DESCRIPTION)
        image_tools.compose_keyword(border, "Quick jAttack", font)

        print("Saving image")
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
    uc = UnitCard("179","10","10",definitions.FRAME_CHAMPION_BASE,"")
    uc.construct_card()
