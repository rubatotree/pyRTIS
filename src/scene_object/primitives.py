import sys
sys.path.append(".")
from mathlib.graphics_math import *
from scene_object.scene_object import *

class Sphere(SceneObject):
    material = None
    def __init__(self, origin:vec3, radius:float, material=None):
        self.origin = origin
        self.radius = radius
        self.material = material
    def hit(self, r:ray, t_min:float, t_max:float):
        oc = r.origin - self.origin
        a = r.direction.norm_sqr()
        half_b = dot(oc, r.direction)
        c = oc.norm_sqr() - self.radius * self.radius
        delta = half_b * half_b - a * c
        if delta < 0:
            return HitRecord.inf()
        else:
            root = math.sqrt(delta)
            tmp = (-half_b - root) / a
            if tmp < t_max and tmp > t_min:
                pos = r.at(tmp)
                return HitRecord(pos, (pos - self.origin).normalized(), tmp, True, self.material, True)
            tmp = (-half_b + root) / a
            if tmp < t_max and tmp > t_min:
                pos = r.at(tmp)
                return HitRecord(pos, -(pos - self.origin).normalized(), tmp, False, self.material, True)
        return HitRecord.inf() 

