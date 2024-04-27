from mathlib.vec3 import *
import random
import math

def clamp(x, a, b):
    if x < a:
        return a
    if x > b:
        return b
    return x

def lerp(a, b, m:float):
    return a * (1 - m) + b * m

def random_float() -> float :
    return random.random()

def random_sphere_surface_uniform():
    x = random_float() * 2 * math.pi
    y = random_float() * 2 * math.pi
    pdf = 1.0 / 4 / math.pi
    vec = vec3(math.cos(x) * math.sin(y), math.sin(x) * math.sin(y), math.cos(y))
    return (vec, pdf)
