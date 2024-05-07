import sys
import os
import numpy as np
from PIL import Image

sys.path.append(".")
from mathlib.graphics_math import *

def output_ppm(filename, img):
    imgfile = open(filename, 'w')
    rows = len(img)
    if rows <= 0:
        return False
    cols = len(img[0])

    imgfile.write(f'P3\n{cols} {rows}\n255\n')

    for i in range(rows):
        for j in range(cols):
            r = int(clamp(255.999 * img[i][j].r(), 0.0, 255.999))
            g = int(clamp(255.999 * img[i][j].g(), 0.0, 255.999))
            b = int(clamp(255.999 * img[i][j].b(), 0.0, 255.999))
            imgfile.write(f'{r} {g} {b}\n')

    imgfile.close()

def output_ppm_data(filename, data):
    imgfile = open(filename, 'w')
    rows = len(data)
    if rows <= 0:
        return False
    cols = len(data[0])

    imgfile.write(f'P3\n{cols} {rows}\n255\n')

    for i in range(rows):
        for j in range(cols):
            x = int(clamp(255.999 * data[i][j], 0.0, 255.999))
            imgfile.write(f'{x} {x} {x}\n')

    imgfile.close()

def output_nogamma(filename, img):
    imgfile = open(filename, 'w')
    rows = len(img)
    if rows <= 0:
        return False
    cols = len(img[0])

    imgfile.write(f'{cols} {rows}\n')

    for i in range(rows):
        for j in range(cols):
            r = "{:.5f}".format(img[i][j].r()).rstrip("0").rstrip(".")
            g = "{:.5f}".format(img[i][j].g()).rstrip("0").rstrip(".")
            b = "{:.5f}".format(img[i][j].b()).rstrip("0").rstrip(".")
            imgfile.write(f'{r} {g} {b}\n')

    imgfile.close()


def output_img(filename, img):
    height = len(img)
    width = len(img[0])
    imgarr = np.arange(width * height * 3).reshape((height, width, 3))
    for i in range(height):
        for j in range(width):
            for c in range(3):
                imgarr[i][j][c] = int(clamp(255.999 * img[i][j].e[c], 0.0, 255.999))
    Image.fromarray(np.uint8(imgarr)).save(filename)

