import sys
sys.path.append(".")
from mathlib.graphics_math import *
from core.renderer_core import *
from core.renderer_frame_spp import RendererFrameSPP
from threading import Thread
import time
from collections import deque


class RendererVarianceHeuristic(Renderer):
    def __init__(self, renderer_core:RendererCore, accvar_spp:int, total_sample_n:int, thread_num = 1, backup_num = 100, use_pillow = False, output_gif = False, compress_output = False):
        self.accvar_spp = accvar_spp
        self.total_sample_n = total_sample_n
        self.thread_num = thread_num
        self.renderer_core = renderer_core
        self.img_num = 0
        self.render_time = 0
        self.backup_num = backup_num
        self.use_pillow = use_pillow
        self.output_gif = output_gif
        self.compress_output = compress_output
    def render(self):
        width = self.renderer_core.width
        height = self.renderer_core.height
        print("Precalculating alias table...")
        weight_sum = 0
        weight_min = math.inf
        alias   = img_init(width, height, (0, 0)) 
        p_alias = img_init(width, height, 0) 
        weight  = img_init(width, height, 0) 
        deq_notfull = deque()
        deq_full = deque()

        variance_map = img_init(width, height, 0) 
        variance_max = 0
        weight_map = img_init(width, height, 0)
        weight_max = 0

        rspp = RendererFrameSPP(self.renderer_core, self.accvar_spp, self.thread_num, self.accvar_spp + 1, output_gif = self.output_gif, compress_output = self.compress_output)

        rspp.render()

        for j in range(height):
            for i in range(width):
                weight[j][i] = self.renderer_core.calc_variance(i, j)

                variance_map[j][i] = weight[j][i]
                variance_max = max(variance_max, variance_map[j][i])

                weight_min = min(weight[j][i], weight_min)
                col = self.renderer_core.col_sum[j][i] / self.renderer_core.sample_n[j][i]
                if min(col.r(), col.g(), col.b()) > 2.0:
                    lightn = 0
                    for cx in range(-1, 2):
                        for cy in range(-1, 2):
                            col = self.renderer_core.col_sum[j + cx][i + cy] / self.renderer_core.sample_n[j + cx][i + cy]
                            if min(col.r(), col.g(), col.b()) > 2.0:
                                lightn += 1
                    if lightn > 2:
                        # is Light
                        weight[j][i] = weight_min
                weight_sum += weight[j][i]
        weight_sum2 = 0
        for j in range(height):
            for i in range(width):
                weight[j][i] = weight[j][i] * width * height / weight_sum
                weight[j][i] = lerp(weight[j][i], 1, 0.2)
                weight_sum2 += weight[j][i]
        for j in range(height):
            for i in range(width):
                weight[j][i] = weight[j][i] * width * height / weight_sum2

                weight_map[j][i] = weight[j][i]
                weight_max = max(weight_max, weight_map[j][i])

                if weight[j][i] < 1:
                    deq_notfull.append((i, j))
                elif weight[j][i] > 1:
                    deq_full.append((i, j))

        for j in range(height):
            for i in range(width):
                weight_map[j][i] /= weight_max
                variance_map[j][i] /= variance_max

        output_ppm_data("./weight.ppm", weight_map)
        output_ppm_data("./variance.ppm", variance_map)


        while len(deq_full) > 0 and len(deq_notfull) > 0:
            fl = deq_full.pop()
            nfl = deq_notfull.pop()
            p_alias[nfl[1]][nfl[0]] = 1 - weight[nfl[1]][nfl[0]]
            alias[nfl[1]][nfl[0]] = fl
            weight[fl[1]][fl[0]] -=  1 - weight[nfl[1]][nfl[0]]
            if weight[fl[1]][fl[0]] < 1:
                deq_notfull.append(fl)
            elif weight[fl[1]][fl[0]] > 1:
                deq_full.append(fl)

        print("Alias table finished. Begin Variance Heuristic Sampling...")
        start_time = time.time()
        img_num = rspp.img_num

        for i in range(self.total_sample_n):
            x = int(random_float() * width)
            y = int(random_float() * height)
            if random_float() < p_alias[y][x]:
                x, y = alias[y][x]

            self.renderer_core.calc_pixel(x, y)

            if i % 10000 == 0 and self.output_gif:
                self.renderer_core.generate_img()
                if self.use_pillow:
                    output_img(f'./output/{self.renderer_core.output_filename}/temp/{img_num}.jpg', self.renderer_core.img)
                else:
                    output_ppm(f'./output/{self.renderer_core.output_filename}/temp/{img_num}.ppm', self.renderer_core.img)
                img_num += 1

            time_str = '{:.3f}'.format(time.time() - start_time)
            progress = (i + 1) / self.total_sample_n
            percent = int(progress * 100)
            time_tot = '{:.3f}'.format((time.time() - start_time) / progress) 
            if self.compress_output:
                print('\r\033[', f'\[{percent}%]  \t{i+1}/{self.total_sample_n} \tt={time_str}/{time_tot}(s) ', end='', flush=True)
            else:
                print('\r\033[', f'\[{percent}%] \tray={i+1}/{self.total_sample_n} \ttime={time_str}(s)/{time_tot}(s) ', end='', flush=True)

        print("\n")
