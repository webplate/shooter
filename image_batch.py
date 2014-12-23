#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from PIL import Image


color_keys = [(255, 0, 255, 255), (0, 255, 255, 255)]


def uniformize_format(path, out) :
    """crawl directory tree for images
    make a copy (all in same dir and uniformized format)"""
    for root, dirs, files in os.walk(path):
        for f in files: 
            # Open the image
            try :
                img = Image.open(os.path.join(root, f))
            except IOError :
                continue
            img = img.convert("RGBA")
            color = color_keys[0]
            w, h = img.size
            for x in range(w) :
                for y in range(h) :
                    if img.getpixel((x, y)) == color_keys[0] :
                        color = color_keys[1]

            back = Image.new("RGBA", img.size, color)
            #paste on opaque background with img alpha map
            back.paste(img, (0, 0), img)
            back = back.convert("RGB")
            back.save(os.path.join(out, f))
            print os.path.join(root, f), '->', os.path.join(out, f)


def long_substr(data):
    substr = ''
    if len(data) > 1 and len(data[0]) > 0:
        for i in range(len(data[0])):
            for j in range(len(data[0])-i+1):
                if j > len(substr) and all(data[0][i:i+j] in x for x in data):
                    substr = data[0][i:i+j]
    return substr

def is_substr(find, data):
    if len(data) < 1 and len(find) < 1:
        return False
    for i in range(len(data)):
        if find not in data[i]:
            return False
    return True

def make_description(path) :
    #make list of all files
    all_files = []
    for root, dirs, files in os.walk(path):
        for f in files:
            all_files.append(os.path.splitext(f)[0])
    #find common parts between all pairs
    common_parts = []
    for i in range(len(all_files)) :
        for j in range(len(all_files)) :
            if j != i :
                common = long_substr([all_files[i], all_files[j]])
                if len(common) > 1 and common not in common_parts :
                    common_parts.append(common)
    #order them by length of common part
    common_parts= sorted(common_parts, key=lambda x: -len(x))
    #group file names with common parts
    grouped = []
    for part in  common_parts :
        fs = []
        for root, dirs, files in os.walk(path):
            for f in files:
                if part in os.path.join(root, f) :
                    fs.append(os.path.join(os.path.splitext(f)[0]))
        grouped.append(fs)
    
    for l in grouped :
        print '\'sprites\' : ', sorted(l),','
                    

path = os.path.join('imgs', 'Shmup')
output_dir = os.path.join('imgs', 'cleb2')

#~ uniformize_format(path, output_dir)
make_description(output_dir)

