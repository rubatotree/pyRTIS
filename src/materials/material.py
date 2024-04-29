import sys
from abc import abstractmethod

sys.path.append(".")
from mathlib.graphics_math import *
from mathlib.ray import *
from scene_object.scene_object import *

class Material:
    # return: (fr, wi, pdf)
    @abstractmethod
    def sample(self, wo:vec3, rec:HitRecord):
        pass

class SimpleLambertian(Material):
    albedo = vec3(1.0)
    def __init__(self, albedo:vec3):
        self.albedo = albedo
    def sample(self, wo:vec3, rec:HitRecord):
        direction, pdf = random_sphere_surface_uniform()
        wi = (direction + rec.normal).normalized()
        fr = self.albedo * pdf / dot(rec.normal, wi)
        return (fr, wi, pdf)

class SimpleMetal(Material):
    albedo = vec3(1.0)
    fuzz = 0.0
    def __init__(self, albedo:vec3, fuzz = 0.0):
        self.albedo = albedo
        self.fuzz = fuzz
    def sample(self, wo:vec3, rec:HitRecord):
        direction, pdf = random_sphere_uniform()
        distort = direction * self.fuzz
        wi = (reflect(-wo, rec.normal) + distort).normalized()
        fr = self.albedo * pdf / dot(rec.normal, wi)
        return (fr, wi, pdf)

class Transparent(Material):
    ref_idx = 1.5
    def __init__(self, ref_idx:float):
        self.ref_idx = ref_idx

    def sample(self, wo:vec3, rec:HitRecord):
        attenuation = vec3(1.0)
        etai_over_etat = (1.0 / self.ref_idx) if rec.front_face else self.ref_idx
        NdotV = min(dot(wo, rec.normal), 1.0)
        sinTheta = math.sqrt(1.0 - NdotV * NdotV)
        reflect_prob = schlick(NdotV, etai_over_etat)

        pdf = 1.0

        if etai_over_etat * sinTheta > 1.0 or random_float() < reflect_prob:
            wi = reflect(-wo, rec.normal)
            fr = attenuation / dot(rec.normal, wi)
            return (fr, wi, pdf)
        else:
            wi = refract(wo, rec.normal, etai_over_etat)
            fr = attenuation / dot(rec.normal, wi)
            return (fr, wi, pdf)

class SimpleLight(Material):
    irradiance = vec3(1.0)
    normal = vec3(0.0)
    def __init__(self, normal:vec3, irradiance:vec3):
        self.normal = normal
        self.irradiance = irradiance
    def sample(self, wo:vec3, rec:HitRecord):
        direction, pdf = random_hemisphere_surface_uniform(self.normal)
        wi = direction
        if dot(self.normal, wo) > 0:
            fr = self.irradiance * pdf
        else:
            fr = vec3.zero()
        return (fr, wi, pdf)
