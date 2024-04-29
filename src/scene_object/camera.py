import sys
sys.path.append(".")
from mathlib.graphics_math import *
from mathlib.ray import *

class Camera:
    origin = vec3(0.0, 1.0, 3.0)
    base_x = vec3(1.0, 0.0, 0.0)
    base_y = vec3(0.0, 1.0, 0.0)
    base_z = vec3(0.0, 0.0, -1.0)
    width = 4.0
    height = 3.0
    dist = 4.0

    def __init__(self):
        pass

    def set_pos(self, origin:vec3):
        self.origin = origin

    def look_at(self, pos:vec3):
        self.base_z = (pos - self.origin).normalized()
        self.base_x = cross(self.base_z, vec3(0.0, 1.0, 0.0))
        self.base_y = cross(self.base_x, self.base_z)

    def gen_ray(self, u:float, v:float):
        u = (u - 0.5) * self.width
        v = (v - 0.5) * self.height
        return ray(self.origin, self.base_x * u + self.base_y * v + self.base_z * self.dist )

