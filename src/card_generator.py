from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class UnitCard(object):
    def __init__(self, template):
        self.image = None
        self.template = template

def horizontal_split(ref, split_pts):
    if not all([i<=ref.size[0] and i>=0 for i in split_pts]):
        raise ValueError("Split position out of range")

    split_imgs = []

    for i,pos in enumerate(split_pts):
        if i == 0:
            bounds = (0,0,pos,ref.size[1])
            cropped_img = ref.crop(bounds)
            cropped_img.load()
            split_imgs.append((cropped_img,bounds))
        else:
            bounds = (split_pts[i-1],0,pos,ref.size[1])
            cropped_img = ref.crop(bounds)
            cropped_img.load()
            split_imgs.append((cropped_img,bounds))

        #end case
        if i == len(split_pts)-1:
            bounds = (pos,0,ref.size[0],ref.size[1])
            cropped_img = ref.crop(bounds)
            cropped_img.load()
            split_imgs.append((cropped_img,bounds))

    return split_imgs

if __name__ == '__main__':
    template = "../templates/units/UNIT_CHAMPION.png"
    img = "..\\templates\\test\\cow.jpg"
    ref = Image.open(img)

    card = UnitCard(template)
    split = horizontal_split(ref, (30,596))
