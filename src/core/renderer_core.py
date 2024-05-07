import sys
sys.path.append(".")
from mathlib.graphics_math import *
from abc import abstractmethod
from img_io.img_output import *
from core.path_integrator import *

class Renderer:
    @abstractmethod
    def render(self):
        pass

class RendererCore:
    scene = None

    def __init__(self, scene, width, height, output_filename):
        self.scene = scene
        self.width = width
        self.height = height
        self.output_filename = output_filename
        self.col_sum     = img_init(width, height)
        self.col_sum_sq  = img_init(width, height)
        self.sample_n    = img_init(width, height, 0)
        self.img         = img_init(width, height)
        self.img_nogamma = img_init(width, height)

    def calc_variance(self, x, y):
        sq =   self.col_sum_sq[y][x]
        sumv = self.col_sum[y][x]
        n =    self.sample_n[y][x]
        var_vec = sq / n - sumv * sumv / n / n
        return var_vec.norm()

    def calc_pixel(self, x, y):
        uv = ((x + random_float()) / self.width, 1 - (y + random_float()) / self.height)
        r = self.scene.main_camera.gen_ray(uv[0], uv[1])
        col = shade_path_tracer(r, self.scene, 0)
        self.col_sum[y][x] += col
        self.col_sum_sq[y][x] += col * col
        self.sample_n[y][x] += 1

    def render_lines(self, start, end):
        for j in range(start, end):
            for i in range(self.width):
                self.calc_pixel(i, j)

    def generate_img(self):
        for j in range(self.height):
            for i in range(self.width):
                img_col = self.col_sum[j][i] / self.sample_n[j][i]
                self.img_nogamma[j][i] = self.col_sum[j][i] / self.sample_n[j][i]
                if img_col.r() < 0 or img_col.g() < 0 or img_col.b() < 0:
                    print(f"\nError: ({img_col})\n(At ({i}, {j}))")
                for c in range(3):
                    img_col.e[c] = clamp(img_col.e[c], 0.0, 1.0)
                self.img[j][i] = gamma_correction(img_col)
