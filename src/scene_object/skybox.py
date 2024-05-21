from mathlib.graphics_math import *
from abc import abstractmethod
from img_io.img_in import *
from collections import deque

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
base_forward = [vec3(-1, 0, 0), vec3(1, 0, 0), vec3(0, -1, 0), vec3(0, 1, 0), vec3(0, 0, -1), vec3(0, 0, 1)]
base_u = [vec3(0, 0, -1), vec3(0, 0, 1), vec3(1, 0, 0), vec3(1, 0, 0), vec3(1, 0, 0), vec3(-1, 0, 0)]
base_v = [vec3(0, -1, 0), vec3(0, -1, 0), vec3(0, 0, 1), vec3(0, 0, -1), vec3(0, -1, 0), vec3(0, -1, 0)]
class SkyBox_FromCubeMap(SkyBox):
    filename_type_id = -1
    suffix = ""
    images = []
    width = []
    height = []
    success = False
    def make_alias_table(self):
        list_pos = []
        self.list_alias = []
        self.list_p_alias = []
        self.pdfs = []
        list_weight = []
        n = 0
        weight_sum = 0
        for k in range(6):
            self.list_alias.append(img_init(self.width[k], self.height[k], (0, 0, 0)))
            self.list_p_alias.append(img_init(self.width[k], self.height[k], 0))
            self.pdfs.append(img_init(self.width[k], self.height[k], 1))
            for i in range(self.height[k]):
                for j in range(self.width[k]):
                    w = self.images[k][i][j].norm()
                    list_pos.append((k, i, j))
                    self.list_alias[k][i][j] = (k, i, j)
                    list_weight.append(w)
                    n += 1
                    weight_sum += w
        deq_notfull = deque()
        deq_full = deque()
        for i in range(n):
            img, r, c = list_pos[i]
            u = 2 * c / self.width[img] - 1
            v = 2 * r / self.height[img] - 1
            dist_sq = vec3(u, v, 1).norm_sqr()
            list_weight[i] *= n / weight_sum
            self.pdfs[img][r][c] = list_weight[i] *dist_sq / 6
            if list_weight[i] > 1:
                deq_full.append(i)
            elif list_weight[i] < 1:
                deq_notfull.append(i)
        while len(deq_full) > 0 and len(deq_notfull) > 0:
            fl = deq_full.pop()
            nfl = deq_notfull.pop()
            fl_img, fl_r, fl_c = list_pos[fl]
            nfl_img, nfl_r, nfl_c = list_pos[nfl]
            self.list_p_alias[nfl_img][nfl_r][nfl_c] = 1 - list_weight[nfl]
            self.list_alias[nfl_img][nfl_r][nfl_c] = list_pos[fl]
            list_weight[fl] -= 1 - list_weight[nfl]
            if list_weight[fl] < 1:
                deq_notfull.append(fl)
            elif list_weight[fl] > 1:
                deq_full.append(fl)

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
            self.make_alias_table()

    def sample_dir(self):
        img = int(random_float() * 6)
        x = int(random_float() * self.width[img])
        y = int(random_float() * self.height[img])
        if random_float() < self.list_p_alias[img][y][x]:
            img, y, x = self.list_alias[img][y][x]
        direction = self.get_direction(img, x + random_float(), y + random_float())
        sample_light_pdf = self.pdfs[img][y][x];
        # print(f"IMG {img} X {x} Y {y} PDF {sample_light_pdf} DIR {direction}")
        return direction, sample_light_pdf

    # left, right, bottom, top, forward, back
    def get_direction(self, img, x, y):
        u = 2 * x / self.width[img] - 1
        v = 2 * y / self.height[img] - 1
        return (base_forward[img] + u * base_u[img] + v * base_v[img]).normalized()

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

