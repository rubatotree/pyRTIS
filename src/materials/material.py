import sys
from abc import abstractmethod

sys.path.append(".")
from mathlib.graphics_math import *
from mathlib.ray import *
from scene_object.scene_object import *

class Material:
    def emission(self, wo:vec3, rec:HitRecord):
        return vec3.zero()
    # return: (fr, wi, pdf)
    def sample(self, wo:vec3, rec:HitRecord):
        return (vec3.zero(), vec3.zero(), 1.0)
    def bsdf(self, wi:vec3, wo:vec3, rec:HitRecord):
        return vec3.zero()

class SimpleLambertian(Material):
    albedo = vec3(1.0)
    def __init__(self, albedo:vec3):
        self.albedo = albedo
    def sample(self, wo:vec3, rec:HitRecord):
        direction, pdf = random_sphere_surface_uniform()
        wi = (direction + rec.normal).normalized()
        fr = self.albedo * pdf / dot(rec.normal, wi)
        return (fr, wi, pdf)
    def bsdf(self, wi:vec3, wo:vec3, rec:HitRecord):
        pdf = 1.0 / 4 / math.pi
        return self.albedo * pdf / dot(rec.normal, wi)

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
    def bsdf(self, wi:vec3, wo:vec3, rec:HitRecord):
        wo_ref = reflect(-wo, rec.normal)
        if self.fuzz == 0:
            if dot(wo_ref, wi) > 0.99999:
                pdf = 1.0 / 4 / math.pi * 3
                return self.albedo * pdf / dot(rec.normal, wi)
            else:
                return vec3.zero()

        d = ((wo_ref - wi).norm() / self.fuzz)
        pdf = 0
        if d >= 0 and d <= 1:
            pdf = 3 * d * d * 1.0 / 4 / math.pi * 3
        return self.albedo * pdf / dot(rec.normal, wi)

class SimpleTransparent(Material):
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
    def brdf(self, wi:vec3, wo:vec3, rec:HitRecord):
        attenuation = vec3(1.0)
        etai_over_etat = (1.0 / self.ref_idx) if rec.front_face else self.ref_idx
        fr = attenuation / dot(rec.normal, wi)
        if etai_over_etat * sinTheta > 1.0:
            return fr

        NdotV = min(dot(wo, rec.normal), 1.0)
        sinTheta = math.sqrt(1.0 - NdotV * NdotV)
        reflect_prob = schlick(NdotV, etai_over_etat)
        wi_reflect = reflect(wo, rec.normal)
        wi_refract = refract(wo, rec.normal, etai_over_etat)
        if dot(wi_reflect, wi) > 0.9999:
            return fr * reflect_prob
        if dot(wi_refract, wi) > 0.9999:
            return fr * (1 - reflect_prob)
        return vec3.zero()

# Temporal "Light material"
class SimpleLight(Material):
    irradiance = vec3(1.0)
    normal = vec3(0.0)
    def __init__(self, normal:vec3, irradiance:vec3):
        self.normal = normal
        self.irradiance = irradiance
    def emission(self, wo:vec3, rec:HitRecord):
        direction, pdf = random_hemisphere_surface_uniform(self.normal)
        wi = direction
        if dot(self.normal, wo) > 0:
            le = self.irradiance / pdf / math.pi
        else:
            le = vec3.zero()
        return le
