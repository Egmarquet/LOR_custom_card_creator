import sys
sys.path.append("..")

from PIL import Image, ImageDraw, ImageFont, ImageChops
from resources import fonts
from resources import colors
from resources.enums import RenderType
from resources import frames
from wand.font import Font
from wand.image import Image as WandImage
from wand.color import Color
from wand.drawing import Drawing
import numpy
import io

def process_img(img, pos, max_size):
    composite = Image.new('RGBA', max_size)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    composite.paste(img, pos, img)

    return composite

def render(layers, max_size):
    """
    Render the image in order of layers
    """
    composite = Image.new('RGBA', max_size)
    while layers:
        layer = layers.pop(0)
        for l in layer:
            img, pos = layer
            if img.size != composite.size or img.mode != 'RGBA':
                img = process_img(img, pos, composite.size)
            composite = Image.alpha_composite(img, max_size)
    return composite


def render_text(text, font, font_size, w, asc, desc, color):
    out = None
    with WandImage(width=w, height=asc+desc, background=None) as image:
        with Drawing() as draw:
            draw.font = font
            draw.font_size = font_size
            draw.fill_color = color
            draw.text(x=0,y=asc,body=text)
            draw(image)
        img_buffer = numpy.asarray(bytearray(image.make_blob(format='png')), dtype='uint8')
        bytesio = io.BytesIO(img_buffer)
        out = Image.open(bytesio)

    return out
        #metrics = draw.get_font_metrics(text,False)

if __name__ == '__main__':
    color = Color('rgb(0,0,0)')
    text = "Greetings!"
    fnt = ImageFont.truetype(fonts.BEAUFORT, 70)
    asc, desc = fnt.getmetrics()
    w = fnt.getsize(text)[0]
    #render(layers, border.size)\
    render_text(text, fonts.BEAUFORT, 70, w, asc, desc, color)
