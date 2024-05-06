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
