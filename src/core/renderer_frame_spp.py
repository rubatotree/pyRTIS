import sys
sys.path.append(".")
from mathlib.graphics_math import *
from core.renderer_core import *
from threading import Thread
import time

class RendererFrameSPP(Renderer):
    def __init__(self, renderer_core, spp, thread_num = 1, backup_num = 100, use_pillow = False, output_gif = False, compress_output = False):
        self.spp = spp
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
        split_num = int(math.ceil(height / self.thread_num))
        start_time = time.time()
        for img_num in range(self.spp):
            for spl in range(split_num):
                split_start = spl * self.thread_num
                split_end = min(height, (spl + 1) * self.thread_num)
                thread_num_cur = min(self.thread_num, split_end - split_start)
                if self.thread_num > 1:
                    threads = []
                    for i in range(thread_num_cur):
                        threads.append(Thread(target=self.renderer_core.render_lines, args=(split_start + i, split_start + i + 1)))
                    for i in range(thread_num_cur):
                        threads[i].start()
                    for i in range(thread_num_cur):
                        threads[i].join()
                else:
                    self.renderer_core.render_lines(split_start, split_end)
                time_str = '{:.3f}'.format(time.time() - start_time)
                progress = (img_num * width * height + split_end * width) / (self.spp * width * height)
                percent = int(progress * 100)
                time_tot = '{:.3f}'.format((time.time() - start_time) / progress) 
                if self.compress_output:
                    print('\r\033[', f'\[{percent}%] F={img_num+1}/{self.spp} \tL={split_end}/{height} \tT={time_str}/{time_tot}(s) ', end='', flush=True)
                else:
                    print('\r\033[', f'\[{percent}%] \tFrame = {img_num+1}/{self.spp} \tLine={split_end}/{height} \tTime={time_str}(s)/{time_tot}(s) ', end='', flush=True)

            self.renderer_core.generate_img()
            self.renderer_core.generate_energy_map()
            self.renderer_core.add_data_point(img_num + 1, time.time() - start_time)
            if self.output_gif:
                if self.use_pillow:
                    output_img(f'./output/{self.renderer_core.output_filename}/temp/{img_num}.jpg', self.renderer_core.img)
                else:
                    output_ppm(f'./output/{self.renderer_core.output_filename}/temp/{img_num}.ppm', self.renderer_core.img)
                    output_ppm_data(f'./output/{self.renderer_core.output_filename}/energy/{img_num}.ppm', self.renderer_core.energy_map)
            if img_num % self.backup_num == 0 and img_num > 0:
                output_ppm(f'./output/{self.renderer_core.output_filename}/temp/{img_num}.ppm', self.renderer_core.img)
                output_nogamma(f'./output/{self.renderer_core.output_filename}/temp/{img_num}_nogamma.txt', self.renderer_core.img_nogamma)
        self.img_num = img_num
        self.render_time = time.time() - start_time
        print("\n")

