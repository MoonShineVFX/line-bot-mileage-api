import glob
from random import shuffle, randint, random
from PIL import Image, ImageDraw, ImageFont
from .to_leet import to_leet
import os
os.environ['PYPINYIN_NO_PHRASES'] = 'true'
os.environ['PYPINYIN_NO_DICT_COPY'] = 'true'

from pypinyin import lazy_pinyin


relp = os.path.dirname(__file__) + '/'


class LOLGenerator(object):
    def __init__(self):
        self.pngs = glob.glob(relp + 'crew_edit/*.png')
        self.cord_start = 178
        self.cord_gap = 188
        self.cord_top = 22
        self.cord_bottom = 388
        self.font = ImageFont.truetype(relp + 'font.ttf', 17)

    def generate(self):
        shuffle(self.pngs)
        tp = Image.open(relp + 'template.jpg')

        for idx, png in enumerate(self.pngs[:10]):
            filename = os.path.basename(png)
            filename = filename.split('.')[0]
            names = lazy_pinyin(filename, strict=False)[1:]

            if random() > 0.65:
                iidx = randint(0, len(names) - 1)
                names[iidx] = names[iidx][0]

            if random() > 0.45:
                text = names[-1]
                names[-1] = text[:-1] + text[-1].upper()

            name = ''.join([n[0].upper() + n[1:] for n in names])

            if random() > 0.65:
                name = to_leet(name)

            this_image = Image.open(png)

            is_bottom = idx > 4
            x = self.cord_start + self.cord_gap * (idx - (5 if is_bottom else 0))
            y = self.cord_bottom if is_bottom else self.cord_top
            tp.paste(this_image, (x, y), this_image)

            d = ImageDraw.Draw(tp)
            w, h = d.textsize(name)
            d.text((x + 88 - w, y + 272 - h), name, font=self.font)

        return tp
