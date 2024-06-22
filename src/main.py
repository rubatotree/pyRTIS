import sys
import time
from threading import Thread
from mathlib.graphics_math import *
from img_io.img_output import *
from scene_object.scenes import *
import core
import matplotlib.pyplot as plt
import numpy as np
from core.path_integrator import *
from core.renderer_core import RendererCore
from core.renderer_frame_spp import RendererFrameSPP
from core.renderer_frame_timelimit import RendererFrameTimeLimit
from core.renderer_variance_heuristic import RendererVarianceHeuristic

output_gif = False 
use_pillow = False
compress_output = False
output_filename = "image"
width, height = 800, 600
spp = 16
thread_num = 1
backup_num = 100
time_limit = -1
scene_name = "cornell"
vh_num = -1
do_test = False
reference = "./data/cornell_cubemap_ref.txt"

scenes=dict()
scenes["cornell"]=scene_cornell_box
scenes["cornell_ao"]=scene_cornell_ao
scenes["cornell_light"]=scene_cornell_Light
scenes["cornell_nospecular"]=scene_cornell_box_no_specular
scenes["cornell_cubemap"]=scene_cornell_box_cubemap
scenes["material"]=scene_skybox_test
scenes["mis"]=scene_mis
scenes["oneweekend"]=scene_one_weekend

def read_args():
    global output_filename, width, height, spp, thread_num, backup_num, output_gif, use_pillow, compress_output, time_limit, scene_name, vh_num, do_test
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
        elif sys.argv[i] == "-test":
            do_test = True
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
            elif sys.argv[i] == "-vh":
                vh_num_tmp = int(sys.argv[i + 1])
                if vh_num_tmp > 0:
                    vh_num = vh_num_tmp
                else:
                    print("Error: Variance Heuristic sample ray number format error")
            elif sys.argv[i] == "-scene":
                scene_name_tmp = str(sys.argv[i + 1])
                if scene_name_tmp in scenes:
                    scene_name = scene_name_tmp
                else:
                    print("Error: Scene not exist")
            elif sys.argv[i] == "-ref":
                ref_tmp = str(sys.argv[i + 1])
                if os.path.exists(ref_tmp):
                    reference = ref_tmp
                else:
                    print("Error: Reference File not exist")

def main():
    read_args()
    main_scene = scenes[scene_name]()

    print(f'Image Size: {width} * {height}', flush=True)

    time_limit_mode = False
    if time_limit > 0:
        time_limit_mode = True
        print("Time Limit Mode")
    if vh_num > 0:
        print("Variance Heuristic Mode")

    baseline = None

    if do_test:
        print("Reading Reference...")
        baseline = read_nogamma(reference)
        integrators = [PathTracerMIS(), PathTracerLightsIS(), PathTracerCosineIS(), PathTracerBRDFIS()]
        names = ["MIS", "LightsIS", "CosineIS", "BRDFIS"]
        colors = ['red', 'blue', 'black', 'green']

        plt.rcParams.update({"font.size":8})
        # plt.figure(figsize=(6, 8))
        plt.title("Error-SPP map", fontsize=12)
        plt.xlabel('spp', fontsize=10)
        plt.ylabel('Error', fontsize=10)

        for i in range(len(integrators)):
            print(f"Testing {names[i]}...\n")
            renderer_core = RendererCore(integrators[i], main_scene, width, height, output_filename, baseline, do_test)
            if time_limit_mode:
                renderer = RendererFrameTimeLimit(renderer_core, time_limit, thread_num, backup_num, use_pillow, output_gif, compress_output)
            else:
                renderer = RendererFrameSPP(renderer_core, spp, thread_num, backup_num, use_pillow, output_gif, compress_output)
            renderer.render()
            renderer_core.generate_img()
            output_nogamma(f'./output/{output_filename}/{output_filename}_{names[i]}_nogamma.txt', renderer_core.img_nogamma)
            output_img(f'./output/{output_filename}/{output_filename}_{names[i]}.bmp', renderer_core.img)
            datafile = open(f'./output/{output_filename}/{output_filename}_{names[i]}_dataset.txt', 'w')
            spp_array = []
            time_array = []
            energy_array = []
            for data in renderer_core.datapoints:
                datafile.write(f"{data.spp} {data.time} {data.energy}\n")
                spp_array.append(data.spp)
                time_array.append(data.time)
                energy_array.append(data.energy)
            datafile.close()

            if i == 0:      # MIS
                plt.ylim((0, energy_array[0]))

            X = np.array(spp_array)
            Y = np.array(energy_array)
            plt.plot(X, Y, color=colors[i], label=names[i])

        plt.legend(loc='best')
        plt.savefig(f'./output/{output_filename}/{output_filename}_error_fig.jpg')
        print(f'\nSaved Plot to', f'./output/{output_filename}/{output_filename}_error_fig.jpg')
    else:
        start_time = time.time()
        renderer_core = RendererCore(PathTracerLightsIS(), main_scene, width, height, output_filename, baseline, do_test)
        renderer = None
        if vh_num > 0:
            renderer = RendererVarianceHeuristic(renderer_core, spp, vh_num, thread_num, backup_num, use_pillow, output_gif, compress_output)
        elif time_limit_mode:
            renderer = RendererFrameTimeLimit(renderer_core, time_limit, thread_num, backup_num, use_pillow, output_gif, compress_output)
        else:
            renderer = RendererFrameSPP(renderer_core, spp, thread_num, backup_num, use_pillow, output_gif, compress_output)

        renderer.render()
        time_str = '{:.3f}'.format(renderer.render_time)

        renderer_core.generate_img()
        output_nogamma(f'./output/{output_filename}/{output_filename}_nogamma.txt', renderer_core.img_nogamma)
        output_ppm(f'./output/{output_filename}/{output_filename}.ppm', renderer_core.img)
        if use_pillow:
            output_img(f'./output/{output_filename}/{output_filename}.bmp', renderer_core.img)

        logfile = open(f'./output/{output_filename}/log.txt', 'w')
        logfile.write(f'FileName = {output_filename}\n')
        logfile.write(f'Scene = {scene_name}\n')
        logfile.write(f'Size = {width}*{height}\n')
        if vh_num > 0:
            logfile.write(f'sample_n = {vh_num} (Variance Heuristic Mode)\n')
        elif time_limit_mode:
            logfile.write(f'spp = {renderer.img_num}(Time Limit Mode)\n')
        else:
            logfile.write(f'spp = {renderer.img_num}\n')

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
