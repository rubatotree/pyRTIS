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

# width, height = 400, 225 
# spp = 128
width, height = 200, 113
spp = 16
p_russian_roulette = 0.6 

main_scene = scene_one_weekend()

def ray_color(r, scene):
    rec = scene.object_root.hit(r, 0.0001, math.inf)
    direction = r.direction.normalized()
    if rec.success:
        if random_float() > p_russian_roulette:
            return vec3.zero()
        wo = -direction
        fr, wi, pdf = rec.material.sample(wo, rec)
        li = ray_color(ray(rec.pos, wi), scene)
        cosval = dot(wi, rec.normal)
        col = li * fr * cosval / pdf
        return col
    else:
        return scene.skybox.sample(direction)

def calc_pixel(x, y):
    uv = (float(x) / width, float(y) / height)
    r = main_scene.main_camera.gen_ray(uv[0], uv[1])
    return ray_color(r, main_scene)

def main():
    output_filename = "./output/image.ppm"
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
                img[j][i] = gamma_correction(col_sum[j][i] / (k + 1))
            time_str = '{:.3f}'.format(time.time() - start_time)
            progress = (k * width * height + j * width + i + 1) / (spp * width * height)
            percent = int(progress * 100)
            time_tot = '{:.3f}'.format((time.time() - start_time) / progress) 

            print('\r\033[', f'\[{percent}%] Frame = {k+1}/{spp} \tLine={j+1}/{height} \tTime={time_str}(s)/{time_tot}(s) ', end='', flush=True)
        output_ppm(f'./output/temp/{k}.ppm', img)

    output_ppm(output_filename, img)

    print(f'\nRayTracing Finish\n')

if __name__ == "__main__":
    main()
