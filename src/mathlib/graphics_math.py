from mathlib.vec3 import *
import random
import math

def clamp(x, a, b):
    if x < a:
        return a
    if x > b:
        return b
    return x

def clamp_vec(vec):
    return vec3(clamp(vec.e[0], 0.0, 1.0), 
                clamp(vec.e[1], 0.0, 1.0), 
                clamp(vec.e[2], 0.0, 1.0))

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
    y = random_float() * math.pi
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
    pdf *= 2
    return (vec, pdf)

def random_hemisphere_surface_cosine(normal=vec3(0,1,0)):
    phi = random_float() * math.pi * 2
    r_sq = random_float()
    r = math.sqrt(r_sq)
    h = math.sqrt(1 - r_sq)
    vec_base = vec3(math.cos(phi) * r, math.sin(phi) * r, h)
    base_x = cross(normal, vec3(0.0, 1.0, 0.0)).safe_normalized()
    if base_x.norm() < 0.001:
        base_x = cross(normal, vec3(1.0, 0.0, 0.0)).safe_normalized()
    base_y = cross(base_x, normal)
    vec = vec_base.x() * base_x + vec_base.y() * base_y + vec_base.z() * normal
    pdf = h / math.pi
    return (vec, pdf)

def gamma_correction(col:vec3) -> vec3 :
    gamma = 1.0 / 2.2
    return vec3(col.e[0] ** gamma, col.e[1] ** gamma, col.e[2] ** gamma)

def img_init(width, height, col=vec3(0.0)):
    img = []
    for j in range(height):
        row = []
        for i in range(width):
            row.append(col)
        img.append(row)
    return img
