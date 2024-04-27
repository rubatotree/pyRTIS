from mathlib.vec3 import *

def clamp(x, a, b):
    if x < a:
        return a
    if x > b:
        return b
    return x

def lerp(a, b, m:float):
    return a * (1 - m) + b * m
