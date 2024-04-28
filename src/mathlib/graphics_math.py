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

def reflect(v:vec3, n:vec3):
    return v - 2 * dot(v, n) * n

def refract(wo:vec3, n:vec3, etai_over_etat:float):
    cosTheta = dot(wo, n)
    r_out_parallel = etai_over_etat * (-wo + cosTheta * n)
    r_out_perp = -math.sqrt(1.0 - r_out_parallel.norm_sqr()) * n;
    return r_out_parallel + r_out_perp

def schlick(cosine:float, ref_idx:float):
    r0 = ((1.0 - ref_idx) / (1.0 + ref_idx)) ** 2
    return r0 + (1 - r0) * ((1 - cosine) ** 5)

def random_float() -> float :
    return random.random()

def random_sphere_surface_uniform():
    x = random_float() * 2 * math.pi
    y = random_float() * 2 * math.pi
    pdf = 1.0 / 4 / math.pi
    vec = vec3(math.cos(x) * math.sin(y), math.sin(x) * math.sin(y), math.cos(y))
    return (vec, pdf)

def random_sphere_uniform():
    x = random_float() * 2 * math.pi
    y = random_float() * 2 * math.pi
    r = random_float()
    pdf = 1.0 / 4 / math.pi * 3
    vec = vec3(math.cos(x) * math.sin(y), math.sin(x) * math.sin(y), math.cos(y)) * (r ** 0.333)
    return (vec, pdf)

def random_hemisphere_surface_uniform(normal):
    vec, pdf = random_sphere_surface_uniform()
    if dot(vec, normal) < 0:
        vec = -vec
    return (vec, pdf)

def gamma_correction(col:vec3) -> vec3 :
    gamma = 1.0 / 2.2
    return vec3(col.e[0] ** gamma, col.e[1] ** gamma, col.e[2] ** gamma)
