import sys
sys.path.append(".")
from mathlib.graphics_math import *
from scene_object.scene_object import *
from scene_object.scene_object_group import *
from materials.material import *
from scene_object.skybox import *

environment_as_light = True

class Light(SceneObject):
    def sample_light(self, pos:vec3):
        return (vec3(0.0), vec3(0.0), vec3(0.0), 0.0)
    def sample_light_pdf(self, wi, rec):
        return 0.0
    def sample_light_emission(self, wi, rec_sample, rec_self):
        return vec3(0.0)

class LightList(SceneObjectGroup):
    def __init__(self):
        self.obj_list = []
        self.domelight = None
        pass
    def choose_uniform(self):
        N = len(self.obj_list)
        select_light_pdf = 1.0 / N
        light_id = int(math.floor(N * random_float()))
        return (self.obj_list[light_id], select_light_pdf)
    def sample_light_pdf(self, wi, rec):
        pdf = 0
        N = len(self.obj_list)
        for light in self.obj_list:
            pdf += light.sample_light_pdf(wi, rec)
        pdf /= N
        return pdf
    def sample_light_emission(self, wi, rec_sample, rec_self=None):
        emission = vec3(0.0)
        if rec_self == None:
            rec_self = self.hit(ray(rec_sample.pos, wi), 0.0001, math.inf)
        if not rec_self.success:
            emission = self.domelight.sample_light_emission(wi, rec_sample, rec_self)
        else:
            emission = rec_self.obj.sample_light_emission(wi, rec_sample, rec_self)
        return emission
    def __len__(self):
        return len(self.obj_list)

class TriangleLight(Light):
    material = None
    vertices = (vec3.zero, vec3.zero, vec3.zero)
    def __init__(self, vertices, radiance:vec3, use_irradiance = False):
        self.vertices = vertices
        dircross = cross(vertices[1] - vertices[0], vertices[2] - vertices[0])
        self.normal = dircross.normalized()
        self.area = abs(dircross.norm()) / 2
        self.material = SimpleDirectionalLight(self.normal, radiance / self.area)
        self.radiance = radiance
        if use_irradiance:
            self.radiance = radiance * self.area
        self.irradiance = self.radiance / self.area

    def hit(self, r:ray, t_min:float, t_max:float):
        # zhuanlan.zhihu.com/p/451582864
        S = r.origin - self.vertices[0]
        E1 = self.vertices[1] - self.vertices[0]
        E2 = self.vertices[2] - self.vertices[0]
        S1 = cross(r.direction, E2)
        S2 = cross(S, E1)
        normal = cross(E1, E2).normalized()

        S1E1 = dot(S1, E1)
        # parallel to the triangle mesh: not hit
        if S1E1 == 0:
            return HitRecord.inf()

        t = dot(S2, E2) / S1E1
        b1 = dot(S1, S) / S1E1
        b2 = dot(S2, r.direction) / S1E1
        if t > t_min and t < t_max and b1 >= 0.0 and b2 >= 0.0 and (1 - b1 - b2) >= 0.0:
            pos = r.at(t)
            front_face = dot(normal, r.direction) < 0
            if not front_face:
                normal = -normal
            rec = HitRecord(pos, normal, t, front_face, self.material, True)
            rec.isLight = True
            rec.obj = self
            return rec
        else:
            return HitRecord.inf()

    def sample_light(self, pos:vec3):
        base_x = self.vertices[1] - self.vertices[0]
        base_y = self.vertices[2] - self.vertices[0]
        normal = cross(base_x, base_y).normalized()
        x = random_float()
        y = random_float()
        if x + y > 1:
            x = 1 - x
            y = 1 - y
        sampled_light_pos = self.vertices[0] + base_x * x + base_y * y
        direction = (sampled_light_pos - pos).normalized()
        dist = (sampled_light_pos - pos).norm()
        cosval = dot(-direction, normal)
        sample_light_pdf = 1 / self.area * dist * dist / abs(cosval)
        if cosval <= 0:
            success = False 
            emission = vec3(0.0)
        else:
            emission = self.irradiance / math.pi
        return (emission, direction, sampled_light_pos, sample_light_pdf)

    def sample_light_pdf(self, wi, rec:HitRecord):
        r = ray(rec.pos, wi)
        hitrec = self.hit(r, 0.0001, math.inf)
        if not hitrec.success:
            return 0.0
        cosval = dot(-r.direction, hitrec.normal)
        sample_light_pdf = 1 / self.area * hitrec.dist * hitrec.dist / abs(cosval)
        return sample_light_pdf

    def sample_light_emission(self, wi, rec_sample, rec_self=None):
        emission = vec3(0.0)
        if rec_self == None:
            rec_self = self.hit(ray(rec_sample.pos, wi), 0.0001, math.inf)
        if rec_self.front_face:
            emission = self.irradiance / math.pi
        return emission

class SphereLight(Light):
    def __init__(self, origin:vec3, radius:float, radiance:vec3, use_irradiance=False):
        self.origin = origin
        self.radius = radius
        self.area = math.pi * 4 * self.radius * self.radius
        self.radiance = radiance
        if use_irradiance:
            self.radiance = radiance * self.area
        self.material = SimpleLight(self.radiance / self.area)
        self.irradiance = self.radiance / self.area
    def hit(self, r:ray, t_min:float, t_max:float):
        oc = r.origin - self.origin
        a = r.direction.norm_sqr()
        half_b = dot(oc, r.direction)
        c = oc.norm_sqr() - self.radius * self.radius
        delta = half_b * half_b - a * c
        if delta <= 0:
            return HitRecord.inf()
        else:
            root = math.sqrt(delta)
            tmp = (-half_b - root) / a
            if tmp < t_max and tmp > t_min:
                pos = r.at(tmp)
                rec = HitRecord(pos, (pos - self.origin).normalized(), tmp, True, self.material, True)
                rec.isLight = True
                rec.obj = self
                return rec
            tmp = (-half_b + root) / a
            if tmp < t_max and tmp > t_min:
                pos = r.at(tmp)
                rec = HitRecord(pos, -(pos - self.origin).normalized(), tmp, False, self.material, True)
                rec.isLight = True
                rec.obj = self
                return rec
        return HitRecord.inf() 
    def sample_light(self, pos:vec3):
        center_dir = (pos - self.origin).normalized()
        sample_dir, sample_pos_pdf = random_hemisphere_surface_cosine(center_dir)
        sampled_light_pos = self.origin + sample_dir * self.radius
        direction = (sampled_light_pos - pos).normalized()
        cosval = dot(-direction, sample_dir)
        dist = (pos - sampled_light_pos).norm()
        if cosval <= 0:
            emission = vec3(0.0)
        else:
            emission = self.irradiance / math.pi
        sample_light_pdf = sample_pos_pdf / self.radius / self.radius / max(abs(cosval), 0.00001) * dist * dist
        return (emission, direction, sampled_light_pos, sample_light_pdf)
    def sample_light_pdf(self, wi, rec):
        center_dir = (rec.pos - self.origin).normalized()
        r = ray(rec.pos, wi)
        oc = r.origin - self.origin
        a = r.direction.norm_sqr()
        half_b = dot(oc, r.direction)
        c = oc.norm_sqr() - self.radius * self.radius
        delta = half_b * half_b - a * c
        dist = [self.origin, self.origin]
        if delta <= 0:
            return 0.0
        else:
            root = math.sqrt(delta)
            dist[0] = (-half_b - root) / a
            dist[1] = (-half_b + root) / a
        
        sample_light_pdf = 0.0
        for i in range(2):
            if dist[i] <= 0:
                continue
            pos = r.at(dist[i])
            sample_dir = (pos - self.origin).normalized()
            cosval = dot(-r.direction, sample_dir)
            sample_pos_pdf = dot(center_dir, sample_dir) / math.pi
            if sample_pos_pdf > 0:
                sample_light_pdf += sample_pos_pdf / self.radius / self.radius / max(abs(cosval), 0.00001) * dist[i] * dist[i]

        return sample_light_pdf

    def sample_light_emission(self, wi, rec_sample, rec_self=None):
        emission = vec3(0.0)
        if rec_self == None:
            rec_self = self.hit(ray(rec_sample.pos, wi), 0.0001, math.inf)
        if rec_self.front_face:
            emission = self.irradiance / math.pi
        return emission

class DomeLight(Light):
    def __init__(self, skybox:SkyBox):
        self.skybox = skybox
        self.material = SimpleSkybox(skybox)
    def hit(self, r:ray, t_min:float, t_max:float):
        return HitRecord.inf() 
    def sample_light(self, pos:vec3):
        direction, sample_light_pdf = self.skybox.sample_dir()
        emission = self.skybox.sample(direction)
        sampled_light_pos = vec3(math.inf, math.inf, math.inf) * direction
        return (emission, direction, sampled_light_pos, sample_light_pdf)
    def sample_light_pdf(self, wi, rec):
        return self.skybox.sample_pdf(wi)
    def sample_light_emission(self, wi, rec_sample, rec_self=None):
        emission = self.skybox.sample(wi)
