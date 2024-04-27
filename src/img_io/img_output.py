import sys
import os

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
