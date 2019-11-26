import definitions
from src import image_tools
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class UnitCard(object):
    """
    All should be strings
    """
    def __init__(self, name, mana, hp, pwr, card_text, border_path, card_img_path):
        self.name = name
        self.mana = mana
        self.hp = hp
        self.pwr = pwr
        self.card_text = card_text
        self.border_path = border_path
        self.card_img_path = card_img_path

    def construct(self):
        composite = Image.new('RGBA', (definitions.CARD_WIDTH, definitions.CARD_HEIGHT))
        darkness = Image.open(definitions.DARKNESS_PATH)
        card_img = Image.open(self.card_img_path)
        border = self.construct_border()
        body = self.construct_body()

        # Building layers
        composite.paste(card_img, (28,57))
        composite = Image.alpha_composite(composite, darkness)
        composite = Image.alpha_composite(composite, border)
        center = int((definitions.CARD_WIDTH-body.size[0])/2.0)
        composite.paste(body,(center,definitions.MAX_DEPTH-body.size[1]),body)
        composite.save('final.png')

    def construct_border(self):
        border = Image.open(self.border_path)

        # Construct mana cost:
        font = ImageFont.truetype(definitions.FONT_BEAUFORT, definitions.FONT_SZ_MANA)
        img = self.construct_text(self.mana, font, definitions.POS_MANA[2]-definitions.POS_MANA[0], color=definitions.OFF_WHITE)
        pos = image_tools.center_align((0,0,img.size[0],img.size[1]), definitions.POS_MANA, vertical=True)
        border.paste(img, pos, img)

        # Drawing health
        font = ImageFont.truetype(definitions.FONT_BEAUFORT, definitions.FONT_SZ_HPPWR)
        img = self.construct_text(self.hp, font, definitions.POS_HP[2]-definitions.POS_HP[0], color=definitions.OFF_WHITE)
        pos = image_tools.center_align((0,0,img.size[0],img.size[1]), definitions.POS_HP, vertical=True)
        border.paste(img, pos, img)

        # Drawing power
        img = self.construct_text(self.pwr, font, definitions.POS_PWR[2]-definitions.POS_PWR[0], color=definitions.OFF_WHITE)
        pos = image_tools.center_align((0,0,img.size[0],img.size[1]), definitions.POS_PWR, vertical=True)
        border.paste(img, pos, img)

        return border

    def construct_body(self):
        """
        Layering is different for each cart type
        """
        center_text_elements = []
        # Drawing title
        font = ImageFont.truetype(definitions.FONT_BEAUFORT, definitions.FONT_SZ_HPPWR)
        img = self.construct_text(self.name, font, definitions.MAX_WIDTH, color=(255,555,255))
        center_text_elements.append(img)

        # Gathering images for Name, power, etc
        # Drawing text:
        font = ImageFont.truetype(definitions.FONT_PADUK, definitions.FONT_SZ_DESCRIPTION)
        img = self.construct_card_text(font)
        center_text_elements.append(img)
        body = image_tools.stitch_images_vertical(center_text_elements, definitions.MAX_WIDTH)

        return body

    def construct_text(self, text, font, max_width, color):
        """
        Construct a line of text such that it is rescaled to fit inside
        of a text box. This does not take font size into consideration
        """
        img = image_tools.compose_word(text, font, color)
        if img.size[0] > max_width:
            scale = float(max_width)/img.size[0]
            img = img.resize((int(img.size[0]*scale), int(img.size[1]*scale)))
        return img

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

        composite = image_tools.compose_image_block_centered(images, definitions.MAX_WIDTH, asc+desc, y_padding=-18, x_spacing=7)

        return composite

    def format_line(self, text):
        """
        Separate non key words from key-words, in order
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

if __name__ == '__main__':
    card_text = "<Support:> Give my supported ally +5|+5 and <Stun> all enemies with my epic dab lmao gottem."
    uc = UnitCard("JONAH OF THE BEACH","7","4","4",card_text,definitions.FRAME_CHAMPION_LVLUP,".\\test_images\\test_dab.png")
    uc.construct()
