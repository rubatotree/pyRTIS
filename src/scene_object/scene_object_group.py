import sys
sys.path.append(".")
from mathlib.graphics_math import *
from mathlib.ray import *
from abc import abstractmethod
from scene_object.scene_object import *

class SceneObjectGroup(SceneObject):
    obj_list = []
    def __init__(self):
        pass
    def append(self, obj : SceneObject):
        self.obj_list.append(obj)
    def hit(self, r:ray, t_min:float, t_max:float):
        current_dist = t_max
        rec_final = HitRecord.inf()
        for obj in self.obj_list:
            rec_temp = obj.hit(r, t_min, current_dist)
            if rec_temp.success:
                current_dist = rec_temp.dist
                rec_final = rec_temp
        return rec_final
    def get_objects(self):
        base_list = []
        for obj in self.obj_list:
            base_list.extend(obj.get_objects())
        return base_list
