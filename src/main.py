import sys
import random
import time
from mathlib.graphics_math import *
from img_io.img_output import *
from scene_object.scene_object import *
from scene_object.scenes import *
from scene_object.scene_object_group import *
from scene_object.primitives import *
from scene_object.camera import *
from materials.material import *

output_gif = False 
use_pillow = False

width, height = 400, 300
spp = 256
p_russian_roulette = 0.8 

main_scene = scene_cornell_box()

def ray_color(r, scene, depth):
    direct_light = vec3(0.0)

    if depth > 0:
        N = len(scene.light_list)
        select_light_pdf = 1.0 / N
        light_id = int(math.floor(N * random_float()))
        light_emission, wi_light, light_pos, sample_light_pdf = scene.light_list[light_id].sample_light(r.origin)
        sample_light_rec = scene.object_root.hit(ray(r.origin, wi_light), 0.0001, math.inf)
        if (sample_light_rec.pos - light_pos).norm() < 0.0001:
            direct_light = light_emission / (select_light_pdf + sample_light_pdf)
        if random_float() > p_russian_roulette:
            return direct_light

    # Global Light 
    global_light = vec3(0.0)
    rec = scene.object_root.hit(r, 0.0001, math.inf)
    direction = r.direction.normalized()
    if rec.success:
        wo = -direction
        le = rec.material.emission(wo, rec)
        fr, wi, pdf = rec.material.sample(wo, rec)
        # fr = rec.material.bsdf(wi, wo, rec)
        cosval = dot(wi, rec.normal)
        if fr.norm() < 0.0001:
            global_light = le
        else:
            li = ray_color(ray(rec.pos, wi), scene, depth + 1)
            global_light = le + li * fr * cosval / pdf
    else:
        global_light = scene.skybox.sample(direction)

    return direct_light + global_light

def calc_pixel(x, y):
    uv = (float(x) / width, float(y) / height)
    r = main_scene.main_camera.gen_ray(uv[0], uv[1])
    return ray_color(r, main_scene, 0)

def main():
    # output_filename = "./output/image.ppm"
    output_filename = "image"
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]

    col_sum = []
    img = []
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
    for k in range(spp):
        for j in range(height):
            sys.stdout.flush()
            for i in range(width):
                col = calc_pixel(i + random.random(), height - 1 - j + random.random())
                col_sum[j][i] += col
                img_col = col_sum[j][i] / (k + 1)
                for c in range(3):
                    img_col.e[c] = clamp(img_col.e[c], 0.0, 1.0)
                img[j][i] = gamma_correction(img_col)
            time_str = '{:.3f}'.format(time.time() - start_time)
            progress = (k * width * height + j * width + i + 1) / (spp * width * height)
            percent = int(progress * 100)
            time_tot = '{:.3f}'.format((time.time() - start_time) / progress) 

            print('\r\033[', f'\[{percent}%] Frame = {k+1}/{spp} \tLine={j+1}/{height} \tTime={time_str}(s)/{time_tot}(s) ', end='', flush=True)
        if output_gif:
            if use_pillow:
                output_img(f'./output/{output_filename}/temp/{k}.jpg', img)
            else:
                output_ppm(f'./output/{output_filename}/temp/{k}.ppm', img)

    if use_pillow:
        output_img(f'./output/{output_filename}/{output_filename}.bmp', img)
    else:
        output_img(f'./output/{output_filename}/{output_filename}.ppm', img)

    print(f'\nRayTracing Finish\n')

if __name__ == "__main__":
    main()
