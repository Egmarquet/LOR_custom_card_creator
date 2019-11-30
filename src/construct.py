import sys
sys.path.append("..")

from PIL import ImageDraw, ImageFont
from PIL import Image as PILImage
import tools
from resources import definitions, enums, fonts, frames, keywords
from wand.font import Font
from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from wand.display import display

class UnitCard(object):
    def __init__(self, name, hp, mana, pwr, text, frame_path, img_path, kws=None, size=definitions.CARD_SIZE):
        self.name = name
        self.mana = mana
        self.hp = hp
        self.pwr = pwr
        self.text = text
        self.frame_path = frame_path
        self.img_path = img_path
        self.kws = kws
        self.size = size
        self.current_layer = []
        self.layers = []

    def construct(self):
        w,h = definitions.CARD_SIZE
        base = Image(width=w,height=h)
        base = tools.to_layer(Image(filename=self.img_path), definitions.CARD_SIZE, definitions.POS_UNIT_IMG)
        base.composite(Image(filename=frames.DARKNESS))
        base.composite(Image(filename=self.frame_path))

        if self.mana:
            base = tools.draw_text_in_box(base, self.hp, fonts.FONT_MANA, definitions.POS_MANA)
        if self.hp:
            base = tools.draw_text_in_box(base, self.hp, fonts.FONT_HPPWR, definitions.POS_HP)
        if self.pwr:
            base = tools.draw_text_in_box(base, self.hp, fonts.FONT_HPPWR, definitions.POS_PWR)

        # Making body text
        body = []
        if self.name:
            name_img = tools.text_to_image(self.name.upper(), fonts.FONT_NAME)
            if name_img.width > definitions.UNIT_TEXT_MAX_WIDTH:
                scale = definitions.UNIT_TEXT_MAX_WIDTH/name_img.width
                name_img.resize(int(scale*name_img.width), int(scale*name_img.height))
            body.append(name_img)

        if self.kws:
            body.append(self.compose_keywords())

        if self.text:
            metrics = fonts.get_metrics(fonts.FONT_TEXT[0],fonts.FONT_TEXT[1])
            ft = self.format_text(self.text)
            word_images = []
            for word, font_tup, icon in ft:
                word_images.append(tools.text_to_image(word, font_tup, icon))
            if word_images:
                text_img = tools.compose_image_block_centered(word_images, definitions.UNIT_TEXT_MAX_WIDTH, word_images[0].height, x_spacing=metrics.text_width)
                body.append(text_img)

        # compositing body
        if body:
            body_img = tools.stitch_images_vertical(body, definitions.UNIT_TEXT_MAX_WIDTH)
            x = int((definitions.CARD_SIZE[0] - definitions.UNIT_TEXT_MAX_WIDTH)/2.0)
            y = definitions.UNIT_TEXT_MAX_DEPTH - body_img.height
            base.composite(body_img, left=x, top=y)

        display(base)

    def compose_keywords(self):
        out = None

        if len(self.kws) < 1:
            return None
        elif len(self.kws) == 1:
            pass
        elif len(self.kws) <= 5 and len(self.kws) >= 1:
            kw_mini = Image(filename=keywords.ICON_MINI)
            kw_dock = []
            for kw in self.kws:
                img_path = keywords.icons[keywords.symbols_map[kw.lower()]]
                kw_icon = Image(filename=img_path)
                kw_copy = kw_mini.clone()
                l,t,_,_ = tools.center_align((0,0,kw_icon.width,kw_icon.height),(0,0,kw_copy.width,kw_copy.height),vertical=True)
                kw_copy.composite(kw_icon, left=l, top=t)
                kw_dock.append(kw_copy)
            out= tools.stitch_images_horizontal(kw_dock,kw_mini.height,x_spacing=20)

        return out

    def format_text(self, text):
        """
        Separate non key words from key-words, in order
        """
        # First sanity check.
        # If there are brackets without partners or nested brackets,
        # throw an error
        stack = []
        for i, c in enumerate(text):
            if c == '<' or c == '[':
                if stack:
                    raise ValueError("Cannot nest keywords")
                else:
                    stack.append(c)

            if c == '>':
                if not stack:
                    raise ValueError("Keywords not well formed, missing opening <")
                elif stack[0] == '[':
                    raise ValueError("Keywords not well formed")
                elif stack[0] == '<':
                    stack.pop()

            elif c == ']':
                if not stack:
                    raise ValueError("Keywords not well formed, missing opening {")
                elif stack[0] == '[':
                    stack.pop()
                elif stack[0] == '<':
                    raise ValueError("Keywords not well formed")

        # If the check is good, then this can easily be split
        cata = []
        curr = ""
        for c in text:
            if c == '<' or c == '[':
                if curr:
                    cata.append((curr, enums.TextType.TEXT))
                curr = ""
            elif c == '>':
                cata.append((curr, enums.TextType.KEYWORD))
                curr = ""
            elif c == ']':
                cata.append((curr,enums.TextType.REF))
                curr = ""
            else:
                curr+=c
        if curr:
            cata.append((curr, enums.TextType.TEXT))

        out = []
        for text, type in cata:
            path = None
            words = [w for w in text.split(" ") if w]
            for i, w in enumerate(words):
                if type == enums.TextType.KEYWORD:
                    if text.lower() in keywords.symbols_map and i == 0:
                        path = keywords.symbols[keywords.symbols_map[text.lower()]]
                        out.append((w.capitalize(), fonts.FONT_KEYWORD, path))
                    else:
                        out.append((w.capitalize(), fonts.FONT_KEYWORD, None))
                elif type == enums.TextType.TEXT:
                    out.append((w, fonts.FONT_TEXT, None))
                elif type == enums.TextType.REF:
                    out.append((w.capitalize(), fonts.FONT_REF, None))
            path = None

        return out

if __name__ == '__main__':
    name = "Maximum Cow"
    hp = "10"
    pwr = "10"
    mp = "44"
    text = "<Quick Attack>: I attack the enemy nexus and summmon 3 [Small Cows] with <fearsome>"
    frame_path = frames.UNIT_COMMON
    img_path = "..\\test\\test_images\\cow.jpg"
    kws = ['barrier', 'elusive']
    uc = UnitCard(name, hp, mp, pwr, text, frame_path, img_path, kws=kws)
    img = uc.construct()
