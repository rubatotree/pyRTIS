import sys
sys.path.append(".")
from mathlib.graphics_math import *
from scene_object.scene_object import *
from materials.material import *

class Light(SceneObject):
    pass

class TriangleLight(Light):
    material = None
    vertices = (vec3.zero, vec3.zero, vec3.zero)
    def __init__(self, vertices, radiance):
        self.vertices = vertices
        dircross = cross(vertices[1] - vertices[0], vertices[2] - vertices[0])
        self.normal = dircross.normalized()
        self.area = abs(dircross.norm()) / 2
        self.material = SimpleLight(self.normal, radiance / self.area)

    def hit(self, r:ray, t_min:float, t_max:float):
        # zhuanlan.zhihu.com/p/451582864
        S = r.origin - self.vertices[0]
        E1 = self.vertices[1] - self.vertices[0]
        E2 = self.vertices[2] - self.vertices[0]
        S1 = cross(r.direction, E2)
        S2 = cross(S, E1)
        normal = cross(E1, E2).normalized()

        S1E1 = dot(S1, E1)
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
            return rec
        else:
            return HitRecord.inf()
