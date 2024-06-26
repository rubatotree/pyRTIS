import sys
from abc import abstractmethod

sys.path.append(".")
from mathlib.graphics_math import *
from mathlib.ray import *
from scene_object.scene_object import *
from scene_object.skybox import *

class Material:
    def emission(self, wo:vec3, rec:HitRecord):
        return vec3.zero()
    # return: (fr, wi, pdf)
    def sample(self, wo:vec3, rec:HitRecord):
        return (vec3.zero(), vec3.zero(), 1.0)
    def bsdf(self, wi:vec3, wo:vec3, rec:HitRecord):
        return vec3.zero()
    def sample_pdf(self, wi:vec3, wo:vec3, rec:HitRecord) -> float:
        return 0.0

class SimpleLambertian(Material):
    albedo = vec3(1.0)
    def __init__(self, albedo:vec3):
        self.albedo = albedo
    def sample(self, wo:vec3, rec:HitRecord):
        direction, pdf = random_hemisphere_surface_cosine(rec.normal)
        wi = direction
        fr = self.albedo / math.pi
        return (fr, wi, pdf)
    def bsdf(self, wi:vec3, wo:vec3, rec:HitRecord):
        return self.albedo / math.pi
    def sample_pdf(self, wi:vec3, wo:vec3, rec:HitRecord):
        costheta = dot(wi, rec.normal)
        if costheta <= 0:
            return 0.0
        return random_hemisphere_surface_cosine_pdf(costheta)

class SimpleMetal(Material):
    albedo = vec3(1.0)
    fuzz = 0.0001
    def __init__(self, albedo:vec3, fuzz = 0.0):
        self.albedo = albedo
        if fuzz < 0.0001:
            fuzz = 0.0001
        self.fuzz = fuzz
        self.integrate_val = math.pi * ((2 * fuzz * fuzz - 1) * math.asin(fuzz) + fuzz * math.sqrt(1 - fuzz * fuzz))
    def sample(self, wo:vec3, rec:HitRecord):
        a2 = self.fuzz ** 2
        wo_ref = reflect(-wo, rec.normal).normalized()
        wi, pdf = random_ggx(a2, wo_ref)
        cosval = max(dot(wi, rec.normal), 0.0001)
        fr = pdf * self.albedo / cosval
        return (fr, wi, pdf)
    def bsdf(self, wi:vec3, wo:vec3, rec:HitRecord):
        cosval = max(dot(wi, rec.normal), 0.0001)
        fr = self.albedo * self.sample_pdf(wi, wo, rec) / cosval
        return fr
    def sample_pdf(self, wi:vec3, wo:vec3, rec:HitRecord):
        wi = wi.normalized()
        wo = wo.normalized()
        wo_ref = reflect(-wo, rec.normal).normalized()
        LdotV = dot(wo_ref, wi)
        if LdotV <= 0:
            return 0.0
        a2 = self.fuzz ** 2
        pdf = random_ggx_pdf(a2, LdotV)
        return pdf

# TODO: bugfix
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
            fr = pdf * attenuation / (dot(rec.normal, wi) + 0.0001)
            return (fr, wi, pdf)
        else:
            wi = refract(wo, rec.normal, etai_over_etat)
            fr = pdf * attenuation / (dot(rec.normal, wi) + 0.0001)
            return (fr, wi, pdf)
    def bsdf(self, wi:vec3, wo:vec3, rec:HitRecord):
        attenuation = vec3(1.0)
        etai_over_etat = (1.0 / self.ref_idx) if rec.front_face else self.ref_idx
        fr = attenuation / (dot(rec.normal, wi) + 0.0001)
        NdotV = min(dot(wo, rec.normal), 1.0)
        sinTheta = math.sqrt(1.0 - NdotV * NdotV)
        if etai_over_etat * sinTheta > 1.0:
            return fr
        reflect_prob = schlick(NdotV, etai_over_etat)
        wi_reflect = reflect(wo, rec.normal)
        wi_refract = refract(wo, rec.normal, etai_over_etat)
        if dot(wi_reflect, wi) > 0.9999:
            return fr * reflect_prob
        if dot(wi_refract, wi) > 0.9999:
            return fr * (1 - reflect_prob)
        return vec3.zero()

class SimpleDirectionalLight(Material):
    irradiance = vec3(1.0)
    normal = vec3(0.0)
    back_albedo = vec3(0.0)
    def __init__(self, normal:vec3, irradiance:vec3):
        self.normal = normal
        self.irradiance = irradiance
    def sample(self, wo:vec3, rec:HitRecord):
        if dot(self.normal, wo) > 0:
            return (vec3.zero(), vec3.zero(), 1.0)
        direction, pdf = random_sphere_surface_uniform()
        wi = (direction + rec.normal).safe_normalized()
        fr = self.back_albedo * pdf / (dot(rec.normal, wi) + 0.0001)
        return (fr, wi, pdf)
    def bsdf(self, wi:vec3, wo:vec3, rec:HitRecord):
        if dot(self.normal, wo) > 0:
            return vec3(0.0)
        pdf = 1.0 / 4 / math.pi
        return self.back_albedo * pdf / (dot(rec.normal, wi) + 0.0001)
    def emission(self, wo:vec3, rec:HitRecord):
        cosval = dot(self.normal, wo)
        if cosval > 0:
            le = self.irradiance / math.pi
        else:
            le = vec3.zero()
        return le

class SimpleLight(Material):
    irradiance = vec3(1.0)
    def __init__(self, irradiance:vec3):
        self.irradiance = irradiance
    def sample(self, wo:vec3, rec:HitRecord):
        return (vec3.zero(), vec3.zero(), 1.0)
    def bsdf(self, wi:vec3, wo:vec3, rec:HitRecord):
        return vec3(0.0)
    def emission(self, wo:vec3, rec:HitRecord):
        le = self.irradiance / math.pi
        return le

class SimpleSkybox(Material):
    def __init__(self, skybox : SkyBox):
        self.skybox = skybox
    def sample(self, wo:vec3, rec:HitRecord):
        return (vec3.zero(), vec3.zero(), 1.0)
    def bsdf(self, wi:vec3, wo:vec3, rec:HitRecord):
        return vec3(0.0)
    def emission(self, wo:vec3, rec:HitRecord):
        le = self.skybox.sample(-wo)
        return le
