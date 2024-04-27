from mathlib.vec3 import *

class ray:
    def __init__(self, origin=vec3(0.0), direction=vec3(0.0)):
        self.origin = origin
        self.direction = direction
    def at(self, t:float) -> vec3:
        return self.origin + self.direction * t
