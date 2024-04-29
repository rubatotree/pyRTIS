from mathlib.graphics_math import *
from abc import abstractmethod

class SkyBox:
    @abstractmethod
    def sample(self, direction:vec3) -> vec3:
        pass

class SkyBox_ColorFill(SkyBox):
    color = vec3(0.0)
    def __init__(self, color=vec3(0.0)):
        self.color = color
    def sample(self, direction:vec3) -> vec3:
        return self.color

class SkyBox_OneWeekend(SkyBox):
    def sample(self, direction:vec3) -> vec3:
        return lerp(vec3(1.0), vec3(0.4, 0.6, 1.0), 0.5 * (direction.y() + 1.0) * 0.8 + 0.2)

class SkyBox_NeonNight(SkyBox):
    def sample(self, direction:vec3) -> vec3:
        return lerp(vec3(0.8, 0.0, 0.32), vec3(0.05, 0.0, 0.1), (direction.y() * 0.5 + 0.5) ** 0.5)
