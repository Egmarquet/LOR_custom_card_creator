from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import re
import definitions
import sys
# Runeterra spell font:
# 36 point
# Good min font size?


def get_text_center(width_outer, width_inner, offset = 0):
    """
    Returns x position of text image centered on img
    """
    pos_x = int((w_outer - w_inner)/2.0)
    return pos_x + offset

def center_align(bounds_inner, bounds_outer, horizontal=True, vertical=False):
    """
    Given a bounding box of (topleft_x, topleft_y, botright_x, botright_y)
    Return a bounding box centered the center of bounds_outer
    """
    bounds = list(bounds_inner)

    if horizontal:
        w_inner = bounds_inner[2] - bounds_inner[0]
        w_outer = bounds_outer[2] - bounds_outer[0]
        topleft_x = bounds_outer[0] + int((w_outer - w_inner)/2.0)
        bounds = [topleft_x, bounds_inner[1], topleft_x+w_inner, bounds_inner[3]]

    if vertical:
        h_inner = bounds_inner[3] - bounds_inner[1]
        h_outer = bounds_outer[3] - bounds_outer[1]
        topleft_y = bounds_outer[1] + int((h_outer - h_inner)/2.0)
        bounds[1] = topleft_y
        bounds[3] = topleft_y + h_inner

    return bounds

def draw_text_block(img, lines, font, x_offset=0, y_offset=0, padding=0, color=(0,0,0,255)):
    """
    Given a list of lines with dimensions, draw them onto the image, beginning
    at x,y and decending downwards
    This will auto center the text, however the y offset should be configured to
    place the text at the correct height on the image

    Args:
        img (PIL.Image):
        lines List:[Tuple:(String,Tuple(int,int))]:
        font (PIL.ImageFont):
    """
    draw = ImageDraw.Draw(img)
    for line in lines:
        text, (w, h) = line
        center_pos = get_text_center(img.width, w)
        draw.text((center_pos,y_offset),text, font=font, fill=color)
        y_offset += h + padding

    img.save("./test/test.png")

def break_text(text, font, max_width):
    """
    Breaks text into a list of lines such that the width of each line
    does not exceed a maximum width

    Returns:
        A list of tuples : List:(List:String,(int,int))). Each entry is a different
        line, with contents at tup[0] and text dimensions tup[1]: (width, height)

    Raises:
        RuntimeError: If a paricular words width exceeds the max width
    """
    out = []
    line_stack = list(reversed(text.split("\n")))
    line_stack = [s.split(" ") for s in line_stack]

    while line_stack:
        line = line_stack.pop(-1)
        line_text = ""
        curr_width = 0
        curr_height = 0
        for i,word in enumerate(line):
            # first word case
            if i == 0:
                w,h = font.getsize(word)
                if w < max_width:
                    line_text+=word
                    curr_width = w
                    curr_height = h
                else:
                    line_stack.append(line[i:]) #If a new line is needed, append it to the stack
                    break
            # Adding spaces between words in non-first word
            else:
                w,h = font.getsize(line_text + " " + word)
                if w < max_width:
                    line_text += " " + word
                    curr_width = w
                    curr_height = h
                else:
                    line_stack.append(line[i:])
                    break

        # If the width of a single word exceeds the max_width
        if not line_text:
            raise RuntimeError("Width of word exceeds max width")

        out.append((line_text, (curr_width,curr_height)))

    return out

def compose_keyword(img, keyword, font):
    symbol = None
    symbol_sz = (0,0)
    right_padding = 3

    if keyword.lower() in definitions.keyword_symbols_map:
        symbol = Image.open(definitions.keyword_symbols_map[keyword.lower()])
        symbol_sz = symbol.size

    _,h = font.getsize(keyword)
    (w,base), (offset_x, offset_y) = font.font.getsize(keyword)

    composite = Image.new('RGBA', (symbol_sz[0]+w+right_padding, h))
    draw = ImageDraw.Draw(composite)
    if symbol:
        composite.paste(symbol,(0,h-symbol.size[1]))

    draw.text((symbol_sz[0]+right_padding, 0), keyword, font=font, fill=definitions.KEYWORD_SYMBOL_COLOR)
    composite.save("elusive.png")

def compose_line(text, font, keyword_font):
    keyword_break = [""]


if __name__ == '__main__':
    font = ImageFont.truetype("./templates/fonts/Padauk/Fonts/padauk-book.ttf", 36)
    text = "If you've played 39 cards with different names this game, summon an amazing thing and win the game"
    img = Image.open("./templates/spells/slow/slow_rare.png")
    draw = ImageDraw.Draw(img)
    color = (0,0,0,255)

    #img.show()
    draw_text_block(img,break_text(text, font, 500),font, y_offset=600)
