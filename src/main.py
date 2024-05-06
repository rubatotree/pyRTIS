import sys
import random
import time
from threading import Thread
import multiprocessing
from mathlib.graphics_math import *
from img_io.img_output import *
from scene_object.scene_object import *
from scene_object.scenes import *
from scene_object.scene_object_group import *
from scene_object.primitives import *
from scene_object.camera import *
from materials.material import *
from core.path_integrator import *

output_gif = True 
use_pillow = False
compress_output = True

width, height = 800, 600
spp = 16
thread_num = 32
backup_num = 100

main_scene = scene_cornell_box()
# main_scene = scene_mis()
# main_scene = scene_skybox_test()

col_sum = []
img = []

def calc_pixel(x, y):
    uv = (float(x) / width, float(y) / height)
    r = main_scene.main_camera.gen_ray(uv[0], uv[1])
    return shade_path_tracer(r, main_scene, 0)

def render_lines(start, end):
    for j in range(start, end):
        for i in range(width):
            col = calc_pixel(i + random.random(), height - 1 - j + random.random())
            col_sum[j][i] += col

def generate_img(frame):
    for j in range(height):
        for i in range(width):
            img_col = col_sum[j][i] / (frame + 1)
            if img_col.r() < 0 or img_col.g() < 0 or img_col.b() < 0:
                print(f"\nError: ({img_col})\n(At ({i}, {j}))")
            for c in range(3):
                img_col.e[c] = clamp(img_col.e[c], 0.0, 1.0)
                img[j][i] = gamma_correction(img_col)

def main():
    output_filename = "image"
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]

    for j in range(height):
        row = []
        img_row = []
        for i in range(width):
            row.append(vec3.zero())
            img_row.append(vec3.zero())
        col_sum.append(row)
        img.append(img_row)

    print(f'Image Size: {width} * {height}', flush=True)

    start_time = time.time()
    split_num = 16
    split_line_num = height // split_num
    thread_line_num = split_line_num // thread_num

    for k in range(spp):
        for split in range(split_num):
            split_start = split_line_num * split
            split_end = split_line_num * (split + 1)
            if split == split_num - 1:
                split_end = height

            if thread_num > 1:
                threads = []
                for i in range(thread_num):
                    start = split_start + thread_line_num * i
                    end =   split_start + thread_line_num * (i + 1)
                    if i == thread_num - 1:
                        end = split_end
                    threads.append(Thread(target=render_lines, args=(start, end)))
                for i in range(thread_num):
                    threads[i].start()
                for i in range(thread_num):
                    threads[i].join()
            else:
                render_lines(split_start, split_end)

            time_str = '{:.3f}'.format(time.time() - start_time)
            progress = (k * width * height + split_end * width) / (spp * width * height)
            percent = int(progress * 100)
            time_tot = '{:.3f}'.format((time.time() - start_time) / progress) 
            if compress_output:
                print('\r\033[', f'\[{percent}%] F={k+1}/{spp} \tL={split_end}/{height} \tT={time_str}/{time_tot}(s) ', end='', flush=True)
            else:
                print('\r\033[', f'\[{percent}%] Frame = {k+1}/{spp} \tLine={split_end}/{height} \tTime={time_str}(s)/{time_tot}(s) ', end='', flush=True)

        if output_gif:
            generate_img(k)
            if use_pillow:
                output_img(f'./output/{output_filename}/temp/{k}.jpg', img)
            else:
                output_ppm(f'./output/{output_filename}/temp/{k}.ppm', img)
        else:
            if k % backup_num == backup_num - 1:
                generate_img(k)
                output_ppm(f'./output/{output_filename}/temp/{k}.ppm', img)

    generate_img(spp - 1)
    if use_pillow:
        output_img(f'./output/{output_filename}/{output_filename}.bmp', img)
    else:
        output_img(f'./output/{output_filename}/{output_filename}.ppm', img)

    print(f'\nRayTracing Finish\n')

if __name__ == "__main__":
    main()
