import sys
sys.path.append(".")
from mathlib.graphics_math import *
from img_io.img_output import *
from scene_object.scene_object import *
from scene_object.scenes import *
from scene_object.scene_object_group import *
from scene_object.primitives import *
from scene_object.camera import *
from materials.material import *
from abc import abstractmethod

p_russian_roulette = 0.8 

class RayTracer:
    @abstractmethod
    def ray_color(self, r, scene):
        pass

class PathTracerNoIS(RayTracer):
    def shade(self, r, scene, depth=0):
        global_light = vec3(0.0)

        rec = scene.object_root.hit(r, 0.0001, math.inf)
        direction = r.direction.normalized()
        wo = -direction

        if not rec.success:
            return scene.skybox.sample(direction)

        if rec.isLight:
            return rec.material.emission(wo, rec)

        if depth > 0 and random_float() > p_russian_roulette:
            return vec3(0.0)
        
        le = rec.material.emission(wo, rec)
        fr, wi, pdf = rec.material.sample(wo, rec)
        fr = rec.material.bsdf(wi, wo, rec)
        cosval = max(dot(wi, rec.normal), 0.0001)
            
        if fr.norm() < 0.000001 or wi.norm() < 0.00001:
            global_light = le
        else:
            li = self.shade(ray(rec.pos, wi), scene, depth + 1)
            global_light = le + li * fr * cosval / pdf

        return global_light
    def ray_color(self, r, scene):
        return self.shade(r, scene, 0)

class PathTracerMIS(RayTracer):
    def shade(self, r, scene, depth=0, rec=None):
        direct_light = vec3(0.0)
        global_light = vec3(0.0)

        if rec == None:
            rec = scene.object_root.hit(r, 0.0001, math.inf)
        direction = r.direction.normalized()
        wo = -direction

        if not rec.success:
            return scene.skybox.sample(direction)

        if rec.isLight:
            if depth == 0:
                return rec.material.emission(wo, rec)
            else:
                return vec3(0.0)

        brdf_fail_rec = None

        if len(scene.light_list) > 0:
            direct_light_is_lights = vec3(0.0)
            direct_light_is_lights_pdf = 0.0
            direct_light_is_brdf   = vec3(0.0)
            direct_light_is_brdf_pdf = 0.0

            # Sample the Lights
            light, select_light_pdf = scene.light_list.choose_uniform()
            light_emission, wi_light, light_pos, sample_light_pdf = light.sample_light(rec.pos)
            sample_light_rec = scene.object_root.hit(ray(rec.pos, wi_light), 0.0001, math.inf)
            if sample_light_pdf > 0 and dot(wi_light, rec.normal) > 0 and (sample_light_rec.pos - light_pos).norm() < 0.0001:
                fr = rec.material.bsdf(wi_light, wo, rec)
                cosval = max(dot(wi_light, rec.normal), 0.0001)
                direct_light_is_lights_pdf = select_light_pdf * sample_light_pdf
                direct_light_is_lights = light_emission * fr * cosval / direct_light_is_lights_pdf

            # Sample the BRDF
            is_brdf_fr, is_brdf_wi, is_brdf_pdf = rec.material.sample(wo, rec)
            is_brdf_fr = rec.material.bsdf(is_brdf_wi, wo, rec)
            is_brdf_rec = scene.object_root.hit(ray(rec.pos, is_brdf_wi), 0.0001, math.inf)
            if is_brdf_rec.isLight:
                direct_light_is_brdf_pdf = is_brdf_pdf
                cosval = max(dot(is_brdf_wi, rec.normal), 0.0001)
                direct_light_is_brdf = is_brdf_rec.material.emission(-is_brdf_wi, is_brdf_rec) * is_brdf_fr * cosval / direct_light_is_brdf_pdf
            else:
                brdf_fail_rec = is_brdf_rec

            # MIS
            # direct_light_is_lights_pdf = 0.0
            # direct_light_is_brdf_pdf = 0.0
            sum_weight = (direct_light_is_lights_pdf + direct_light_is_brdf_pdf)
            if sum_weight > 0:
                direct_light = (direct_light_is_lights_pdf * direct_light_is_lights + direct_light_is_brdf_pdf * direct_light_is_brdf) / sum_weight

        if depth > 0 and random_float() > p_russian_roulette:
            return direct_light
        
        le = rec.material.emission(wo, rec)
        fr, wi, pdf = rec.material.sample(wo, rec)
        fr = rec.material.bsdf(wi, wo, rec)
        cosval = max(dot(wi, rec.normal), 0.0001)
            
        if fr.norm() < 0.000001 or wi.norm() < 0.00001:
            global_light = le
        else:
            li = self.shade(ray(rec.pos, wi), scene, depth + 1, brdf_fail_rec)
            global_light = le + li * fr * cosval / pdf

        return direct_light + global_light
    def ray_color(self, r, scene):
        return self.shade(r, scene, 0)

class PathTracerLightsIS(RayTracer):
    def shade(self, r, scene, depth=0):
        direct_light = vec3(0.0)
        global_light = vec3(0.0)

        rec = scene.object_root.hit(r, 0.0001, math.inf)
        direction = r.direction.normalized()
        wo = -direction

        if not rec.success:
            return scene.skybox.sample(direction)

        if rec.isLight:
            if depth == 0:
                return rec.material.emission(wo, rec)
            else:
                return vec3(0.0)

        if len(scene.light_list) > 0:
            direct_light_is_lights = vec3(0.0)
            direct_light_is_lights_pdf = 0.0
            direct_light_is_brdf   = vec3(0.0)
            direct_light_is_brdf_pdf = 0.0

            # Sample the Lights
            light, select_light_pdf = scene.light_list.choose_uniform()
            light_emission, wi_light, light_pos, sample_light_pdf = light.sample_light(rec.pos)
            sample_light_rec = scene.object_root.hit(ray(rec.pos, wi_light), 0.0001, math.inf)
            if sample_light_pdf > 0 and dot(wi_light, rec.normal) > 0 and (sample_light_rec.pos - light_pos).norm() < 0.0001:
                fr = rec.material.bsdf(wi_light, wo, rec)
                cosval = max(dot(wi_light, rec.normal), 0.0001)
                direct_light_is_lights_pdf = select_light_pdf * sample_light_pdf
                direct_light_is_lights = light_emission * fr * cosval / direct_light_is_lights_pdf

            direct_light = direct_light_is_lights

        if depth > 0 and random_float() > p_russian_roulette:
            return direct_light
        
        le = rec.material.emission(wo, rec)
        fr, wi, pdf = rec.material.sample(wo, rec)
        fr = rec.material.bsdf(wi, wo, rec)
        cosval = max(dot(wi, rec.normal), 0.0001)
            
        if fr.norm() < 0.000001 or wi.norm() < 0.00001:
            global_light = le
        else:
            li = self.shade(ray(rec.pos, wi), scene, depth + 1)
            global_light = le + li * fr * cosval / pdf

        return direct_light + global_light
    def ray_color(self, r, scene):
        return self.shade(r, scene, 0)

class PathTracerBRDFIS(RayTracer):
    def shade(self, r, scene, depth=0, rec=None):
        direct_light = vec3(0.0)
        global_light = vec3(0.0)

        if rec == None:
            rec = scene.object_root.hit(r, 0.0001, math.inf)

        direction = r.direction.normalized()
        wo = -direction

        if not rec.success:
            return scene.skybox.sample(direction)

        if rec.isLight:
            if depth == 0:
                return rec.material.emission(wo, rec)
            else:
                return vec3(0.0)

        brdf_fail_rec = None
        if len(scene.light_list) > 0:
            direct_light_is_lights = vec3(0.0)
            direct_light_is_lights_pdf = 0.0
            direct_light_is_brdf   = vec3(0.0)
            direct_light_is_brdf_pdf = 0.0

            # Sample the BRDF
            is_brdf_fr, is_brdf_wi, is_brdf_pdf = rec.material.sample(wo, rec)
            is_brdf_fr = rec.material.bsdf(is_brdf_wi, wo, rec)
            is_brdf_rec = scene.object_root.hit(ray(rec.pos, is_brdf_wi), 0.0001, math.inf)
            if is_brdf_rec.isLight:
                direct_light_is_brdf_pdf = is_brdf_pdf
                cosval = max(dot(is_brdf_wi, rec.normal), 0.0001)
                direct_light_is_brdf = is_brdf_rec.material.emission(-is_brdf_wi, is_brdf_rec) * is_brdf_fr * cosval / direct_light_is_brdf_pdf
            else:
                brdf_fail_rec = is_brdf_rec
            direct_light = direct_light_is_brdf

        if depth > 0 and random_float() > p_russian_roulette:
            return direct_light
        
        le = rec.material.emission(wo, rec)
        fr, wi, pdf = rec.material.sample(wo, rec)
        fr = rec.material.bsdf(wi, wo, rec)
        cosval = max(dot(wi, rec.normal), 0.0001)
            
        if fr.norm() < 0.000001 or wi.norm() < 0.00001:
            global_light = le
        else:
            li = self.shade(ray(rec.pos, wi), scene, depth + 1, brdf_fail_rec)
            global_light = le + li * fr * cosval / pdf

        return direct_light + global_light
    def ray_color(self, r, scene):
        return self.shade(r, scene, 0)
