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
from resources import fonts

def center_align(bounds_inner, bounds_outer, horizontal=True, vertical=False):
    """
    Given a bounding box of (x, y, w, h)
    Return a bounding box equal to the size of bounds_inner, centered within
    the bounds_outer box
    """
    if horizontal:
        topleft_x = bounds_outer[0] + int((bounds_outer[2] - bounds_inner[2])/2.0)
        bounds = [topleft_x, bounds_inner[1], bounds_inner[2], bounds_inner[3]]

    if vertical:
        topleft_y = bounds_outer[1] + int((bounds_outer[3] - bounds_inner[3])/2.0)
        bounds[1] = topleft_y

    return bounds

def composite_text(base, text, font_tup, bounds, kerning=0):
    """
    Compose a block of text centered within a bounding box
    This will scale the bounding image to not exceed the width of the bounds
    Mutates the base image
    """
    img = text_to_image(text, font_tup, kerning=kerning)
    if img.width > bounds[2]:
        scale = bounds[2]/img.width
        img.resize(int(img.width*scale),int(img.height*scale))
    center = center_align((0,0,img.width,img.height),bounds,vertical=True)
    with img:
        base.composite(img, left=center[0], top=center[1])

def text_to_image(text, font_tup, icon=None, kerning=0):
    """
    Creates an image from text. If the icon field is said, then the icon will
    be prepended to the text. This will be commonly used to create the Keywords
    found in text
    """
    out = Image(height=1,width=1) #dummy image
    with Drawing() as draw:
        font_path, font_size, color = font_tup
        draw.font = font_path
        draw.font_size = font_size
        draw.fill_color = color
        draw.text_kerning = kerning

        metrics = draw.get_font_metrics(out, text)
        asc = int(metrics.ascender)
        desc = int(-1*metrics.descender)
        width = metrics.text_width + max(metrics.x1, -1*metrics.x1) # I believe this gets the full text width
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
