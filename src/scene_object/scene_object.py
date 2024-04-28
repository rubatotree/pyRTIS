import sys
sys.path.append(".")
from mathlib.graphics_math import *
from mathlib.ray import *
from abc import abstractmethod
import math

class HitRecord:
    success = False
    pos = vec3.zero()
    normal = vec3.zero()
    dist = math.inf
    front_face = False
    material = None
    def __init__(self, pos=vec3.zero(), normal=vec3.zero(), dist=math.inf, front_face=False, material=None, success=True):
        self.pos = pos
        self.normal = normal
        self.dist = dist
        self.front_face = front_face
        self.material = material
        self.success = success
        pass
    @staticmethod
    def inf():
        return HitRecord(success=False)

class SceneObject:
    material = None
    @abstractmethod
    def hit(self, r:ray, t_min:float, t_max:float):
        pass 
