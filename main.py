import definitions
from src import image_tools

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class UnitCard(object):
    """
    All should be strings
    """
    def __init__(self, mana, hp, pwr, card_text, border_path, img_path):
        self.mana = mana
        self.hp = hp
        self.pwr = pwr
        self.card_text = card_text
        self.border_path = border_path
        self.img_path = img_path

    def format_line(self, text):
        """
        Separate non-key words from key-words, in order
        """
        # First sanity check.
        # If there are brackets without partners or nested brackets,
        # throw an error
        stack = []
        for i, c in enumerate(text):
            if c == '<' or c == '{':
                if stack:
                    raise ValueError("Cannot nest keywords")
                else:
                    stack.append(c)

            if c == '>':
                if not stack:
                    raise ValueError("Keywords not well formed, missing opening <")
                elif stack[0] == '{':
                    raise ValueError("Keywords not well formed")
                elif stack[0] == '<':
                    stack.pop()

            elif c == '}':
                if not stack:
                    raise ValueError("Keywords not well formed, missing opening {")
                elif stack[0] == '{':
                    stack.pop()
                elif stack[0] == '<':
                    raise ValueError("Keywords not well formed")

        # If the check is good, then this can easily be split
        out = []
        curr = ""
        for c in text:
            if c == '<' or c == '{':
                out.append((curr, definitions.TextType.TEXT))
                curr = ""
            elif c == '>':
                out.append((curr, definitions.TextType.KEYWORD))
                curr = ""
            elif c == '}':
                out.append((curr,definitions.TextType.REF))
                curr = ""
            else:
                curr+=c
        if curr:
            out.append((curr, definitions.TextType.TEXT))
        return out

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
        card_text = construct_card_text(font)
        
        #line = image_tools.compose_line("<Play:> If I attack, grant me <overwhelm> this turn, <Elusive> or <Quick Attack>", font)
        print(format_line(sentence))

    def construct_card_text(self, font):
        images = []
        blocks = self.format_line(self.card_text)
        asc, desc = font.getmetrics()
        for text, type in blocks:
            if text:
                if type is definitions.TextType.KEYWORD:
                    images.append(image_tools.compose_keyword(text, font, x_spacing=7))
                elif type is definitions.TextType.REF:
                    images.extend([image_tools.compose_word(t, font, color=definitions.KEYWORD_BLUE) for t in text.split(" ")])
                else:
                    images.extend([image_tools.compose_word(t, font, color=definitions.DESCRIPTION_GREY) for t in text.split(" ")])

        out = image_tools.compose_image_block_centered(images, definitions.MAX_WIDTH, asc+desc, y_padding=-18, x_spacing=7)

        return out

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
    card_text = "<Play:> This unit gains <Elusive> this turn and adds a {Mystic Shot} to the hand"
    ezreal_card = "<Nexus Strike:> Create a <Fleeting> 0 cost {Mystic Shot}"
    card_text = "<Support:> Give my supported ally +3|+0 and <overwhelm> this roujgnd."
    uc = UnitCard("179","10","10",card_text,definitions.FRAME_CHAMPION_BASE,"")
    uc.construct_card_text()
