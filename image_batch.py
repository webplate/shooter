#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from PIL import Image

path = os.path.join('imgs')

color_keys = [(255, 0, 255, 255), (0, 255, 255, 255)]


def uniformize_format(path):
    # OVERWRITE IMGS in /imgs to uniformize their format
    for root, dirs, files in os.walk(path):
        for f in files: 
            # Open the image
            try:
                print(os.path.join(root, f))
                img = Image.open(os.path.join(root, f))
            except IOError:
                continue
            img = img.convert("RGBA")
            color = color_keys[0]
            w, h = img.size
            for x in range(w):
                for y in range(h):
                    if img.getpixel((x, y)) == color_keys[0]:
                        color = color_keys[1]

            back = Image.new("RGBA", img.size, color)
            # paste on opaque background with img alpha map
            back.paste(img, (0, 0), img)
            back = back.convert("RGB")
            back.save(os.path.join(root, f))
 
def put_all_in_same():
    
