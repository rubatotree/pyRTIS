from mathlib.graphics_math import *
from abc import abstractmethod
from img_io.img_in import *

class SkyBox:
    @abstractmethod
    def sample(self, direction:vec3) -> vec3:
        pass
    def sample_dir(self) -> vec3:
        return random_sphere_surface_uniform()

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

# left, right, bottom, top, forward, back
cubemap_filenames = [["negx", "posx", "negy", "posy", "negz", "posz"]]
cubemap_suffix = ["bmp", "jpg", "png", "ppm", "webp"]
class SkyBox_FromCubeMap(SkyBox):
    filename_type_id = -1
    suffix = ""
    images = []
    width = []
    height = []
    success = False
    def __init__(self, filename:str):
        for i in range(len(cubemap_filenames)):
            for j in range(len(cubemap_suffix)):
                if os.access(f"./data/cubemaps/{filename}/{filename}_{cubemap_filenames[i][0]}.{cubemap_suffix[j]}", os.R_OK):
                    self.filename_type_id = i
                    self.suffix = cubemap_suffix[j]
        if self.filename_type_id == -1:
            print("Error: File not exists")
            success = False
        else:
            for i in range(len(cubemap_filenames[self.filename_type_id])):
                fname = f"./data/cubemaps/{filename}/{filename}_{cubemap_filenames[self.filename_type_id][i]}.{self.suffix}"
                print("Reading File: ", fname)
                if not os.access(fname, os.R_OK):
                    print("Error: File not exists")
                    success = False
                    break
                self.images.append(read_img(fname))
                self.width.append(len(self.images[i][0]))
                self.height.append(len(self.images[i]))
        if len(self.images) == 6:
            success = True

    def sample(self, direction:vec3):
        img = 0
        u = 0
        v = 0
        direction /= max(abs(direction.x()), abs(direction.y()), abs(direction.z()))
        if abs(-1 - direction.x()) < 0.00001:
            u = -direction.z()
            v = -direction.y()
            img = 0
        elif abs(+1 - direction.x()) < 0.00001:
            u = +direction.z()
            v = -direction.y()
            img = 1
        elif abs(-1 - direction.y()) < 0.00001:
            u = +direction.x()
            v = +direction.z()
            img = 2
        elif abs(+1 - direction.y()) < 0.00001:
            u = +direction.x()
            v = -direction.z()
            img = 3
        elif abs(-1 - direction.z()) < 0.00001:
            u = +direction.x()
            v = -direction.y()
            img = 4
        elif abs(+1 - direction.z()) < 0.00001:
            u = -direction.x()
            v = -direction.y()
            img = 5
        u = u * 0.5 + 0.5
        v = v * 0.5 + 0.5
        u = clamp(u, 0, 1)
        v = clamp(v, 0, 1)
        pixel_u = int(u * (self.width[img] - 0.0001))
        pixel_v = int(v * (self.height[img] - 0.0001))
        return self.images[img][pixel_v][pixel_u]

