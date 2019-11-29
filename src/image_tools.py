from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageEnhance
import re
import sys
# Runeterra spell font:
# 36 point
# Good min font size?

def size(bounds):
    return (bounds[2]-bounds[0],bounds[3]-bounds[1])

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

def stitch_images(images, height, x_spacing=0):
    """
    Stitch a list images from left to right
    """
    total_width = -1*x_spacing # don't pad out left most
    for img in images:
        total_width+=img.size[0] + x_spacing

    composite = Image.new('RGBA', (total_width, height))
    offset = 0
    for img in images:
        composite.paste(img, (offset, 0))
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
    composite = Image.new('RGBA', (width, max_height))
    for img in images:
        center = int((width - img.size[0])/2.0)
        composite.paste(img, (center, y_offset), img)
        y_offset += img.size[1] + y_spacing

    return composite

def compose_keyword(keyword, font, x_spacing=0, symbol_spacing=0):
    """
    Given a keyword, compose an image of the keyword + assosiated symbol
    Note, if the keyword does not have an associated symbol, it will still return
    with the color change
    The size of the text is standard at 38 pt, and the scaling of the symbol
    should be based on that.

    TODO: symbol scaling
    """
    composite = None
    asc, desc = font.getmetrics()
    if keyword.lower() in definitions.keyword_symbols_map:
        symbol = Image.open(definitions.keyword_symbols_map[keyword.lower()])
        sym_w, sym_h = symbol.size
        words = [w.capitalize() for w in keyword.split(" ")]
        words = [compose_word(word, font, color=definitions.KEYWORD_GOLD) for word in words]
        text = stitch_images(words, asc+desc, x_spacing=x_spacing)

        # Symbol posting
        centered_sym = Image.new('RGBA', (symbol.size[0], asc+desc))
        center = int((asc+desc-symbol.size[1])/2.0)
        centered_sym.paste(symbol, (0, center))

        composite = stitch_images([centered_sym, text], asc+desc,x_spacing=symbol_spacing)

    else:
        words = [w.capitalize() for w in keyword.split(" ")]
        words = [compose_word(word, font, color=definitions.KEYWORD_GOLD) for word in words]
        composite = stitch_images(words, asc+desc, x_spacing=x_spacing)

    return composite

def render_text(text, font, color):
    """
    Text rendering with proper anti-aliasing
    Credit to
        https://nedbatchelder.com/blog/200801/truly_transparent_text_with_pil.html
    """
    asc, desc = font.getmetrics()
    w = font.getsize(text)[0]
    # Setting up image channels
    im = Image.new("RGB", (w,asc+desc), (0,0,0))
    alpha = Image.new("L", im.size, "black")

    # Make a grayscale image of the font, white on black.
    imtext = Image.new("L", im.size, 0)
    drtext = ImageDraw.Draw(imtext)
    drtext.fontmode = "1"
    drtext.text((0,0), text, font=font, fill="white")

    # Add the white text to our collected alpha channel. Gray pixels around
    # the edge of the text will eventually become partially transparent
    # pixels in the alpha channel.
    alpha = ImageChops.lighter(alpha, imtext)
    # Make a solid color, and add it to the color layer on every pixel
    # that has even a little bit of alpha showing.
    solidcolor = Image.new("RGBA", im.size, color)
    immask = Image.eval(imtext, lambda p: 255 * (int(p != 0)))

    im = Image.composite(solidcolor, im, immask)
    im.putalpha(alpha)

    return im

def compose_image_block_centered(images, max_width, height, x_spacing=0, y_padding=0, strict=False):
    """
    Given a series of images, attempt stitch them left to right such that
    appending new images does not exceed max_width. If a particular image does
    exceed it, start a new line. The rendered output will try to center each line

    If strict==False, then a single image that exceeds max_width can be placed
    on its own line. If strict is True, then this method will throw a ValueError()

    Args:
        images (List): List of PIL.Image objects
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
        if strict and w > max_width:
            raise ValueError("Single image exceeds max width of line")
        w = img.size[0]
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
    lines = [stitch_images(line, height, x_spacing=x_spacing) for line in lines]

    # Composing final image
    max_height = len(lines)*(height+y_padding) - y_padding
    y_offset = 0
    composite = Image.new('RGBA', (max_width, max_height))
    for line in lines:
        center = int((max_width - line.size[0])/2)
        composite.paste(line, (center, y_offset), line)
        y_offset += height + y_padding

    return composite

def process_img(img, pos, max_size):
    composite = Image.new('RGBA', max_size)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    composite.paste(img, pos, img)

    return composite

def reduce_opacity(img, percent):
    alpha = img.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(percent)
    img.putalpha(alpha)
    return img

def blur(img, bounds):
    pass

def resize(img, bounds):
    scale = float(bounds[2]-bounds[0])/img.size[0]
    img = img.resize((int(img.size[0]*scale), int(img.size[1]*scale)))
    return img
