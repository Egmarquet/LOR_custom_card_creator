"""
New implementation of image tools using Wand as opposed to PIL
"""
import re
import sys
sys.path.append("..")
from wand.font import Font
from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from wand.display import display
from resources import frames, fonts

def center_align(bounds_inner, bounds_outer, horizontal=True, vertical=False):
    """
    Given a bounding box of (topleft_x, topleft_y, botright_x, botright_y)
    Return a bounding box equal to the size of bounds_inner, centered within
    the bounds_outer box
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

def get_scale(size_1, size_2):
    """
    Returns the relative scaling of size_1 to size_2 of the height and width
    """
    return (float(size_1[1])/size_2[1],float(size_1[1])/size_2[1])

def draw_text_in_box(base, text, font_tup, bounds, kerning=0):
    """
    Draws a single line of text such that it does not exceed bounds

    Returns a mutated img
    """
    with Drawing() as draw:
        font_path, font_size, color = font_tup
        draw.font = font_path
        draw.font_size = font_size
        draw.fill_color = color
        draw.text_kerning = kerning
        metrics = draw.get_font_metrics(base, text)
        scale = (bounds[3]-bounds[1])/metrics.text_width
        # If the image is too wide for the bounding box
        if scale < 1.0:
            draw.font_size = int(font_size*scale)
            metrics = draw.get_font_metrics(base, text)
        # Centering and drawing
        asc = int(metrics.ascender)
        desc = int(-1*metrics.descender)
        center = center_align((0,0,metrics.text_width, asc+desc),bounds, vertical=True)
        draw.text(x=center[0],y=center[1]+asc,body=text)
        draw(base)

    return base

def text_to_image(text, font_tup, icon=None, kerning=0):
    out = Image(height=1,width=1)
    with Drawing() as draw:
        font_path, font_size, color = font_tup
        draw.font = font_path
        draw.font_size = font_size
        draw.fill_color = color
        draw.text_kerning = kerning

        metrics = draw.get_font_metrics(out, text)
        asc = int(metrics.ascender)
        desc = int(-1*metrics.descender)
        width = metrics.text_width + max(metrics.x1, -1*metrics.x1)
        offset = 0
        if icon:
            # scaling icon
            icon_img = Image(filename=icon)
            with icon_img:
                scale = (asc+desc)/icon_img.height
                icon_img.resize(int(scale*icon_img.width), int(scale*icon_img.height))

                #compositing
                offset = icon_img.width
                out.resize(int(icon_img.width+width),int(asc+desc))
                out.composite(icon_img)
        else:
            out.resize(int(width),int(asc+desc))

        draw.text(x=offset,y=asc,body=text)
        draw(out)
    return out

def compose_image_block_centered(images, max_width, height, x_spacing=0, y_padding=0, strict=False):
    """
    Given a series of images, attempt stitch them left to right such that
    appending new images does not exceed max_width. If a particular image does
    exceed it, start a new line. The rendered output will try to center each line

    If strict==False, then a single image that exceeds max_width can be placed
    on its own line. If strict is True, then this method will throw a ValueError()

    Args:
        images (List): List of wand Image objects
        max_width (int): Max width of a line in px
        height (int): Height of each line
        x_spacing (int): The right spacing between each image
        y_padding (int): Padding added to the bottom of each image, increasing total height
        strict (bool): See above
    """
    lines = [] # Will be a list of list of images on each line
    curr = []
    width = -x_spacing
    for img in images:
        w = img.size[0]
        if strict and w > max_width:
            raise ValueError("Single image exceeds max width of line")
        if width + w <= max_width:
            curr.append(img)
            width += w + x_spacing
        else:
            if curr:
                lines.append(curr)
            curr = []
            curr.append(img)
            width = w + x_spacing
    #cleanup
    if curr:
        lines.append(curr)

    # Stitching
    lines = [stitch_images_horizontal(line, height, x_spacing=x_spacing) for line in lines]
    return stitch_images_vertical(lines, max_width)

def stitch_images_horizontal(images, height, x_spacing=0):
    """
    Stitch a list images from left to right. This will attempt
    to vertically center all images
    """
    total_width = -1*x_spacing # don't pad out left most
    for img in images:
        total_width+=img.width + x_spacing

    composite = Image(width=int(total_width), height=int(height))
    offset = 0

    for img in images:
        with img:
            composite.composite(img, left=int(offset), top=0)
            offset += img.size[0] + x_spacing

    return composite

def stitch_images_vertical(images, width, y_spacing=0):
    """
    Stitch images in a collumn. This will attempt to horizontally center
    all the stitched images. Images are stiched top to bottom in order
    that they appear in the list
    """
    max_height = -1*y_spacing
    for img in images:
        max_height += img.size[1] + y_spacing

    y_offset = 0
    composite = Image(width=width, height=max_height)
    for img in images:
        with img:
            center = int((width - img.width)/2.0)
            composite.composite(img, left=center, top=y_offset)
            y_offset += img.size[1] + y_spacing

    return composite

def to_layer(img, size, pos):
    """
    Return a layered image
    """
    base = Image(width=size[0],height=size[1])
    with img:
        base.composite(img, left=pos[0], top=pos[1])
    return base

def layer(base, layer):
    """
    Copy and layer two Image objects
    """
    if layer.size != base.size:
        raise ValueError("Layers must be the same size")
    b = base.clone()
    with layer as l:
        b.composite(l)
    return b

if __name__ == '__main__':
    img = Image(filename="..\\test\\test_images\\test_dab.png")
    frame = Image(filename=frames.UNIT_COMMON)
    a  = to_layer(img, (680, 1024), (28,57))
    b = layer(a, frame)
    text = "1000000"
    c = draw_text_in_box(b, text, fonts.FONT_MANA, (23,33,158,170))
    d = draw_text_in_box(c, text, fonts.FONT_MANA, (300,300,40,400))
