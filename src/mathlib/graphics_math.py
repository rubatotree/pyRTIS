from mathlib.vec3 import *

def clamp(x, a, b):
    if x < a:
        return a
    if x > b:
        return b
    return x

