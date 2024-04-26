sys.path.append(".")
from mathlib.graphics_math import *

class Camera:
    vec_up = vec3(0.0, 1.0, 0.0)

    origin = vec3(0.0, 0.0, 2.0)
    base_x = vec3(1.0, 0.0, 0.0)
    base_y = vec3(0.0, 1.0, 0.0)
    base_z = vec3(0.0, 0.0, -1.0)
    width = 4.0
    height = 2.25
    dist = 2.0

    def __init__(self):
        pass

    def set_pos(self, origin:vec3):
        self.origin = origin

    def look_at(self, pos:vec3):
        base_z = (pos - origin).normalized()
        base_x = cross(base_z, vec_up)
        base_y = cross(base_x, base_z)

    def gen_ray(u:float, v:float):
        u = (u - 0.5) * width_
        v = (v - 0.5) * height_
        return ray(origin, u * base_x + v * base_y + dist * base_z)

