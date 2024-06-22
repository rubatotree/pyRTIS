import sys
sys.path.append(".")
from mathlib.graphics_math import *
from mathlib.ray import *
from abc import abstractmethod
import math

class HitRecord:
    obj = None
    success = False
    pos = vec3.zero()
    normal = vec3.zero()
    dist = math.inf
    front_face = False
    material = None
    isLight = False
    def __init__(self, pos=vec3.zero(), normal=vec3.zero(), dist=math.inf, front_face=False, material=None, success=True, obj=None):
        self.obj = None
        self.pos = pos
        self.normal = normal
        self.dist = dist
        self.front_face = front_face
        self.material = material
        self.success = success
        pass
    @staticmethod
    def inf():
        rec = HitRecord(success=False)
        rec.isLight = True
        rec.success = False
        return rec

class SceneObject:
    material = None
    @abstractmethod
    def hit(self, r:ray, t_min:float, t_max:float):
        pass 
    def get_objects(self):
        return [self]

