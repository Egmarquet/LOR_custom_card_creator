import sys
sys.path.append("..")

from PIL import ImageDraw, ImageFont
from PIL import Image as PILImage
import tools
from resources import definitions, enums, fonts, frames, keywords, regions
from wand.font import Font
from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from wand.display import display
import time

class UnitCard(object):
    def __init__(self,  frame_path,
                        name=None,
                        hp=None,
                        mana=None,
                        pwr=None,
                        text=None,
                        tribe=None,
                        region=None,
                        img_path=None,
                        kws=None,
                        darkness_alpha=0.35,
                        blur=True):

        self.frame_path = frame_path
        self.img_path = img_path
        self.name = name
        self.mana = mana
        self.hp = hp
        self.pwr = pwr
        self.text = text
        self.tribe = tribe
        self.text = text
        self.region= region
        self.kws = kws

        # Darkness
        self.darkness_alpha = darkness_alpha
        self.blur = True

        # Private image layers
        self.__frame = Image(filename=self.frame_path)
        self.__body = None
        self.__image = None
        self.__body_y_pos = 0

        self.out = None

    def render_frame(self):
        """
        Renders all elements that can sit on the frame of the image
        """
        self.__frame = Image(filename=self.frame_path)
        if self.mana:
            tools.draw_text_in_box(self.__frame, self.mana, fonts.FONT_MANA, definitions.POS_MANA)
        if self.hp:
            tools.draw_text_in_box(self.__frame, self.hp, fonts.FONT_HPPWR, definitions.POS_HP)
        if self.pwr:
            tools.draw_text_in_box(self.__frame, self.pwr, fonts.FONT_HPPWR, definitions.POS_PWR)
        if self.tribe:
            tribe_img = Image(filename=frames.TRIBE)
            center = int((definitions.CARD_SIZE[0] - tribe_img.width)/2.0)
            with tribe_img:
                self.__frame.composite(tribe_img, top=11, left=center)
                tools.draw_text_in_box(self.__frame, self.tribe.upper(), fonts.FONT_TRIBE, definitions.POS_TRIBE, kerning=3)
        if self.region in regions.map:
            region_img = Image(filename=regions.map[self.region])
            center = int((definitions.CARD_SIZE[0] - region_img.width)/2.0)
            with region_img:
                self.__frame.watermark(region_img, transparency=0.65, top=870, left=center)

    def render_body(self):
        """
        Rendering any text that goes in the body of the image
        All the positioning for the body is relative to the card positioning
        """
        self.__body = Image(width=definitions.CARD_SIZE[0],height=definitions.CARD_SIZE[1])
        body = []

        if self.name:
            name_img = tools.text_to_image(self.name.upper(), fonts.FONT_NAME)
            if name_img.width > definitions.UNIT_TEXT_MAX_WIDTH:
                scale = definitions.UNIT_TEXT_MAX_WIDTH/name_img.width
                name_img.resize(int(scale*name_img.width), int(scale*name_img.height))
            body.append(name_img)

        if self.kws:
            body.append(self.compose_keywords())

        # Adding text body
        if self.text:
            metrics = fonts.get_metrics(fonts.FONT_TEXT[0],fonts.FONT_TEXT[1])
            ft = self.format_text(self.text)
            word_images = []
            for word, font_tup, icon in ft:
                word_images.append(tools.text_to_image(word, font_tup, icon))

            if word_images:
                text_img = tools.compose_image_block_centered(  word_images,
                                                                definitions.UNIT_TEXT_MAX_WIDTH,
                                                                word_images[0].height,
                                                                x_spacing=metrics.text_width)
                body.append(text_img)

        # compositing body
        if body:
            body_img = tools.stitch_images_vertical(body, definitions.UNIT_TEXT_MAX_WIDTH)
            x = int((definitions.CARD_SIZE[0] - definitions.UNIT_TEXT_MAX_WIDTH)/2.0)
            y = definitions.UNIT_TEXT_MAX_DEPTH - body_img.height
            self.__body_y_pos = y
            with body_img:
                self.__body.composite(body_img, left=x, top=y)

    def render_image(self):
        base = Image(width=definitions.CARD_SIZE[0],height=definitions.CARD_SIZE[1])
        l, t = definitions.POS_UNIT_IMG
        print(self.__body_y_pos)

        if self.img_path:
            with Image(filename=self.img_path) as img:
                base.composite(img, left=l, top=t)
                if self.blur and self.__body_y_pos:
                    new = Image(width=definitions.CARD_SIZE[0],height=definitions.CARD_SIZE[1])
                    slice_upper = base.clone()[0:base.width,0:self.__body_y_pos]
                    with base[0:base.width,self.__body_y_pos:base.height] as slice_lower:
                        slice_lower.blur(sigma=9)
                        new.composite(slice_lower,top=self.__body_y_pos)
                    new.composite(slice_upper)
                    base = new
            with Image(filename=frames.DARKNESS) as dark:
                base.watermark(dark, transparency=self.darkness_alpha)

        self.__image = base

    def render(self):
        base = Image(width=definitions.CARD_SIZE[0],height=definitions.CARD_SIZE[1])
        self.render_frame()
        self.render_body()
        self.render_image()
        if self.__image:
            base.composite(self.__image)
        if self.__frame:
            base.composite(self.__frame)
        if self.__body:
            base.composite(self.__body)

        self.out = base

    def compose_keywords(self):
        out = None

        if len(self.kws) < 1:
            return None

        elif len(self.kws) == 1:
            kw = self.kws[0]
            kw_icon = keywords.icons[keywords.symbols_map[kw.lower()]]
            kw_text = kw.upper()
            kw_img = tools.text_to_image(kw_text, fonts.FONT_KEYWORD_ICON, kw_icon)
            left, center, right =  (Image(filename=keywords.ICON_LEFT),Image(filename=keywords.ICON_CENTER),Image(filename=keywords.ICON_RIGHT))
            if kw_img.width > center.width:
                scale = kw_img.width/center.width
                center.resize(int(center.width*scale),center.height)
            kw_background = tools.stitch_images_horizontal((left,center,right),left.height)
            l,t,_,_ = tools.center_align((0,0,kw_img.width,kw_img.height),(0,0,kw_background.width,kw_background.height), vertical=True)
            kw_background.composite(kw_img, left=l, top=t)

            return kw_background

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
            out = tools.stitch_images_horizontal(kw_dock,kw_mini.height,x_spacing=20)

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
    hp = "4"
    pwr = "3"
    mp = "3"
    text = "<Quick Attack>: I attack the enemy nexus and summmon 3 [Small Cows] with <fearsome>"
    frame_path = frames.UNIT_COMMON
    img_path = "..\\test\\test_images\\test_dab.png"
    kws = ['barrier']
    tribe = "Elite"
    region = "noxus"
    uc = UnitCard(frame_path)
    uc.name = name
    uc.img_path = img_path
    uc.tribe = tribe
    uc.mana = "1"
    uc.hp = "10"
    uc.text = text
    uc.img_path = img_path
    # adds .15 seconds to execution
    start = time.time()
    uc.render()
    end = time.time()
    print(end - start)
    display(uc.out)
