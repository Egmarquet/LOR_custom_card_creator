import sys
sys.path.append("..")

from PIL import Image, ImageDraw, ImageFont
import image_tools
from resources import colors, definitions, enums, fonts, frames, keywords

class UnitCard(object):
    def __init__(self, name, hp, mana, pwr, text, frame_path, img_path, size=definitions.CARD_SIZE):
        self.name = name
        self.mana = mana
        self.hp = hp
        self.pwr = pwr
        self.text = text
        self.frame_path = frame_path
        self.img_path = img_path
        self.size = size
        self.current_layer = []
        self.layers = []

    def construct(self):
        image = Image.open(self.img_path)

        # Adding base layers
        darkness = Image.open(frames.DARKNESS)
        darkness = image_tools.reduce_opacity(darkness, 0.6)
        frame = Image.open(self.frame_path)
        self.add_to_curr_layer(image, definitions.UNIT_IMG_PLACEMENT)
        self.append_curr_layer()
        self.add_to_curr_layer(darkness, (0,0))
        self.append_curr_layer()
        self.add_to_curr_layer(frame, (0,0))
        self.append_curr_layer()

        # Adding border text:
        if self.mana:
            img = image_tools.render_text(self.mana, fonts.FONT_MANA[0], fonts.FONT_MANA[1])
            if img.size[0] > image_tools.size(definitions.POS_MANA)[0]:
                img = image_tools.resize(img, definitions.POS_MANA)
            pos = image_tools.center_align((0,0,img.size[0],img.size[1]), definitions.POS_MANA, vertical=True)
            self.add_to_curr_layer(img, pos)

        # Adding hp and power values
        if self.hp:
            img = image_tools.render_text(self.hp, fonts.FONT_HPWPR[0], fonts.FONT_HPWPR[1])
            if img.size[0] > image_tools.size(definitions.POS_HP)[0]:
                img = image_tools.resize(img, definitions.POS_HP)
            pos = image_tools.center_align((0,0,img.size[0],img.size[1]), definitions.POS_HP, vertical=True)
            self.add_to_curr_layer(img, pos)

        if self.pwr:
            img = image_tools.render_text(self.hp, fonts.FONT_HPWPR[0], fonts.FONT_HPWPR[1])
            if img.size[0] > image_tools.size(definitions.POS_PWR)[0]:
                img = image_tools.resize(img, definitions.POS_PWR)
            pos = image_tools.center_align((0,0,img.size[0],img.size[1]), definitions.POS_PWR, vertical=True)
            self.add_to_curr_layer(img, pos)

        if self.text:
            # Adding text
            formatted_text = self.format_text(self.text)
            img = image_tools.render_text(self.text, fonts.FONT_KEYWORD[0], fonts.FONT_KEYWORD[1])
            pos = image_tools.center_align((0,0,img.size[0],img.size[1]), (0,0,definitions.CARD_SIZE[0], definitions.CARD_SIZE[1]),vertical=True)
            self.add_to_curr_layer(img, pos)

            print(formatted_text)

        self.append_curr_layer()
        return self.render()

    def add_to_curr_layer(self, image, pos):
        self.current_layer.append((image, pos))

    def append_curr_layer(self):
        self.layers.append(self.current_layer)
        self.current_layer = []

    def format_text(self, text):
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
                if out:
                    out.append((curr, enums.TextType.TEXT))
                curr = ""
            elif c == '>':
                out.append((curr, enums.TextType.KEYWORD))
                curr = ""
            elif c == '}':
                out.append((curr,enums.TextType.REF))
                curr = ""
            else:
                curr+=c
        if curr:
            out.append((curr, enums.TextType.TEXT))
        return out

    def format_description(self, formatted_text, max_width):
        lines = []
        curr_width = []
        for text, type in formatted_text:
            pass
            
    def render(self):
        """
        Render the image in order of layers
        """
        composite = Image.new('RGBA', self.size)
        for layer in self.layers:
            for l in layer:
                img, pos = l
                if img.size != composite.size or img.mode != 'RGBA':
                    img = image_tools.process_img(img, pos, composite.size)
                composite = Image.alpha_composite(composite, img)
        return composite

if __name__ == '__main__':
    name = "Hello world!"
    hp = "500"
    mp = "44"
    pwr = "500"
    text = "Allegiance: Grant all allies"
    frame_path = frames.UNIT_COMMON
    img_path = "..\\test\\test_images\\cow.jpg"
    uc = UnitCard(name, hp, mp, pwr, text, frame_path, img_path)
    img = uc.construct()
    img.save("..\\test\\test_images\\construct.png")
