sys.path.append(".")
from mathlib.graphics_math import *
from mathlib.ray import *
import math

class HitRecord:
    pos = vec3.zero()
    normal = vec3.zero()
    dist = math.inf
    front_face = False
    material = None
    def __init__(self, pos=vec3.zero(), normal=vec3.zero(), dist=math.inf, front_face=False, material=None):
        self.pos = pos
        self.normal = normal
        self.dist = dist
        self.front_face = front_face
        self.material = material
        pass
    @staticmethod
    def inf():
        return HitRecord()

class SceneObject:
    material = None
    @abstractmethod
    def hit(r:ray, t_min:float, t_max:float, rec:HitRecord)
        pass 

