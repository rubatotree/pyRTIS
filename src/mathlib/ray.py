from mathlib.vec3 import *

class ray:
    def __init__(self, origin=vec3(0.0), direction=vec3(0.0)):
        self.origin = origin
        self.direction = direction
    def at(t:float) -> vec3:
        return origin + direction * t
