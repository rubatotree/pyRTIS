import sys
import os
import numpy as np
from PIL import Image
from mathlib.graphics_math import *

def read_img(filename):
    img = Image.open(filename)
    npArray = np.array(img)
    ls = npArray.tolist()
    width = len(ls[0])
    height = len(ls)
    img = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(vec3(ls[i][j][0] / 256, ls[i][j][1] / 256, ls[i][j][2] / 256))
        img.append(row)
    return img

def read_nogamma(filename):
    f = open(filename)
    wh = f.readline().split(" ")
    w = int(wh[0])
    h = int(wh[1])
    img = img_init(w, h)
    for i in range(h):
        for j in range(w):
            rgb = f.readline().split(" ")
            r = float(rgb[0])
            g = float(rgb[1])
            b = float(rgb[2])
            img[i][j] = vec3(r, g, b)
    f.close()
    return img


