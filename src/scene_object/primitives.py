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
                return HitRecord(pos, (pos - self.origin).normalized(), tmp, True, self.material, True, obj=self)
            tmp = (-half_b + root) / a
            if tmp < t_max and tmp > t_min:
                pos = r.at(tmp)
                return HitRecord(pos, -(pos - self.origin).normalized(), tmp, False, self.material, True, obj=self)
        return HitRecord.inf() 

class Triangle(SceneObject):
    material = None
    vertices = (vec3.zero, vec3.zero, vec3.zero)
    def __init__(self, vertices, material=None):
        self.vertices = vertices
        self.material = material

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
            return HitRecord(pos, normal, t, front_face, self.material, True, obj=self)
        else:
            return HitRecord.inf()


