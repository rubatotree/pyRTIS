import sys
from abc import abstractmethod

sys.path.append(".")
from mathlib.graphics_math import *
from mathlib.ray import *
from scene_object.scene_object import *

class Material:
    # return: (fr, wi, pdf)
    @abstractmethod
    def sample(self, rec:HitRecord):
        pass

class Lambertian(Material):
    albedo = vec3(1.0)
    def __init__(self, albedo):
        self.albedo = albedo
    def sample(self, rec:HitRecord):
        direction, pdf = random_sphere_surface_uniform()
        wi = (direction + rec.normal).normalized()
        fr = self.albedo * pdf / dot(rec.normal, wi)
        return (fr, wi, pdf)

