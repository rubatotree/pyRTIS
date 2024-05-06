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

output_gif = False 
use_pillow = False
compress_output = False
output_filename = "image"
width, height = 800, 600
spp = 4
thread_num = 1
backup_num = 100
time_limit = -1
scene_name = "cornell"

scenes=dict()
scenes["cornell"]=scene_cornell_box
scenes["cornell_cubemap"]=scene_cornell_box_cubemap
scenes["material"]=scene_skybox_test
scenes["mis"]=scene_mis
scenes["oneweekend"]=scene_one_weekend

def read_args():
    global output_filename, width, height, spp, thread_num, backup_num, output_gif, use_pillow, compress_output, time_limit, scene_name
    argc = len(sys.argv)
    for i in range(argc):
        if sys.argv[i] == "-gif":
            output_gif = True
        elif sys.argv[i] == "-nogif":
            output_gif = False
        elif sys.argv[i] == "-pillow":
            use_pillow = True
        elif sys.argv[i] == "-nopillow":
            use_pillow = False
        elif sys.argv[i] == "-compress-output":
            compress_output = True
        elif sys.argv[i] == "-nocompress-output":
            compress_output = False
        elif i < argc - 1:
            if sys.argv[i] == "-o":
                output_filename = str(sys.argv[i + 1])
            elif sys.argv[i] == "-size":
                spl = sys.argv[i + 1].split("x") 
                if len(spl) != 2:
                    spl = sys.argv[i + 1].split("*") 
                if len(spl) != 2:
                    spl = sys.argv[i + 1].split(",") 
                if len(spl) != 2:
                    print("Error: Size format error")
                    continue
                width = int(spl[0])
                height = int(spl[1])
            elif sys.argv[i] == "-spp":
                spp = int(sys.argv[i + 1])
            elif sys.argv[i] == "-j":
                thread_num = int(sys.argv[i + 1])
            elif sys.argv[i] == "-backup":
                backup_num = int(sys.argv[i + 1])
            elif sys.argv[i] == "-timelimit":
                time_limit_tmp = float(sys.argv[i + 1])
                if time_limit_tmp > 0:
                    time_limit = time_limit_tmp
                else:
                    print("Error: Time Limit format error")
            elif sys.argv[i] == "-scene":
                scene_name_tmp = str(sys.argv[i + 1])
                if scene_name_tmp in scenes:
                    scene_name = scene_name_tmp
                else:
                    print("Error: Scene not exist")

col_sum = []
img = []
img_nogamma = []

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
            img_col = col_sum[j][i] / frame
            img_nogamma[j][i] = col_sum[j][i] / frame
            if img_col.r() < 0 or img_col.g() < 0 or img_col.b() < 0:
                print(f"\nError: ({img_col})\n(At ({i}, {j}))")
            for c in range(3):
                img_col.e[c] = clamp(img_col.e[c], 0.0, 1.0)
            img[j][i] = gamma_correction(img_col)

def main():
    global main_scene
    read_args()
    main_scene = scenes[scene_name]()
    for j in range(height):
        row = []
        img_row = []
        img_nogamma_row = []
        for i in range(width):
            row.append(vec3.zero())
            img_row.append(vec3.zero())
            img_nogamma_row.append(vec3.zero())
        col_sum.append(row)
        img.append(img_row)
        img_nogamma.append(img_nogamma_row)

    print(f'Image Size: {width} * {height}', flush=True)

    time_limit_mode = False
    if time_limit > 0:
        time_limit_mode = True
        print("Time Limit Mode")

    start_time = time.time()
    split_num = int(math.ceil(height / thread_num))

    img_num = 0

    while True:
        for spl in range(split_num):
            split_start = spl * thread_num
            split_end = min(height, (spl + 1) * thread_num)
            thread_num_cur = min(thread_num, split_end - split_start)

            if thread_num > 1:
                threads = []
                for i in range(thread_num_cur):
                    threads.append(Thread(target=render_lines, args=(split_start + i, split_start + i + 1)))
                for i in range(thread_num_cur):
                    threads[i].start()
                for i in range(thread_num_cur):
                    threads[i].join()
            else:
                render_lines(split_start, split_end)

            time_str = '{:.3f}'.format(time.time() - start_time)
            if time_limit_mode:
                progress = (time.time() - start_time) / time_limit
                percent = int(progress * 100)
                if compress_output:
                    print('\r\033[', f'\[{percent}%] F={img_num+1} \tL={split_end}/{height} \tT={time_str}/{time_limit}(s) ', end='', flush=True)
                else:
                    print('\r\033[', f'\[{percent}%] \tFrame = {img_num+1} \tLine={split_end}/{height} \tTime={time_str}(s)/{time_limit}(s) ', end='', flush=True)
            else:
                progress = (img_num * width * height + split_end * width) / (spp * width * height)
                percent = int(progress * 100)
                time_tot = '{:.3f}'.format((time.time() - start_time) / progress) 
                if compress_output:
                    print('\r\033[', f'\[{percent}%] F={img_num+1}/{spp} \tL={split_end}/{height} \tT={time_str}/{time_tot}(s) ', end='', flush=True)
                else:
                    print('\r\033[', f'\[{percent}%] \tFrame = {img_num+1}/{spp} \tLine={split_end}/{height} \tTime={time_str}(s)/{time_tot}(s) ', end='', flush=True)

        if output_gif:
            generate_img(img_num + 1)
            if use_pillow:
                output_img(f'./output/{output_filename}/temp/{img_num}.jpg', img)
            else:
                output_ppm(f'./output/{output_filename}/temp/{img_num}.ppm', img)
        else:
            if img_num % backup_num == 0 and img_num > 0:
                generate_img(img_num + 1)
                output_ppm(f'./output/{output_filename}/temp/{img_num}.ppm', img)
                output_nogamma(f'./output/{output_filename}/temp/{img_num}_nogamma.txt', img_nogamma)
        img_num += 1
        if time_limit_mode:
            if time.time() - start_time >= time_limit:
                print(f"\nTime Limit Exceed. spp={img_num}")
                break
        else:
            if img_num >= spp:
                break

    time_str = '{:.3f}'.format(time.time() - start_time)

    generate_img(img_num)
    output_nogamma(f'./output/{output_filename}/{output_filename}_nogamma.txt', img_nogamma)
    output_img(f'./output/{output_filename}/{output_filename}.ppm', img)
    if use_pillow:
        output_img(f'./output/{output_filename}/{output_filename}.bmp', img)

    logfile = open(f'./output/{output_filename}/log.txt', 'w')
    logfile.write(f'FileName = {output_filename}\n')
    logfile.write(f'Scene = {scene_name}\n')
    logfile.write(f'Size = {width}*{height}\n')
    if time_limit_mode:
        logfile.write(f'spp = {img_num}(Time Limit Mode)\n')
    else:
        logfile.write(f'spp = {img_num}\n')

    logfile.write(f'Time = {time_str}\n')
    if time_limit_mode:
        logfile.write(f'Time Limit = {time_limit}\n')
    if use_pillow:
        logfile.write(f'Use Pillow\n')
    if output_gif:
        logfile.write(f'Output GIF\n')

    print(f'\nRayTracing Finish\nSaved image to', f'./output/{output_filename}/{output_filename}.ppm')

if __name__ == "__main__":
    main()
