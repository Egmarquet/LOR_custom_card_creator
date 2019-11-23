from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import sys
# Runeterra spell font:
# 36 point
# Good min font size?


def get_text_center(outer_width, inner_width):
    """
    Returns x position of text image centered on img
    """
    center = int(outer_width/2.0 - inner_width/2.0)
    return center

def draw_text(img, text, font, pos, color=(0,0,0,255)):
    draw = ImageDraw.Draw(img)
    draw.text((center_pos,y_offset),text, font=font, fill=color)

    return img

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

if __name__ == '__main__':
    font = ImageFont.truetype("./templates/fonts/Padauk/Fonts/padauk-book.ttf", 36)
    text = "If you've played 39 cards with different names this game, summon an amazing thing and win the game"
    img = Image.open("./templates/spells/slow/slow_rare.png")
    draw = ImageDraw.Draw(img)
    color = (0,0,0,255)

    #img.show()
    draw_text_block(img,break_text(text, font, 500),font, y_offset=600)
