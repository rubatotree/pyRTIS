import sys
import random
from mathlib.graphics_math import *
from img_io.img_output import *
from scene_object.scene_object import *
from scene_object.scene_object_group import *
from scene_object.primitives import *
from scene_object.camera import *
from materials.material import *

width, height = 400, 225
spp = 256
main_scene = SceneObjectGroup()
main_scene.append(Sphere(vec3(0.0, 1.0, 0.0), 1.0, Lambertian(vec3(1.0, 0.6, 0.8))))
main_scene.append(Sphere(vec3(0.0, -1000.0, 0.0), 1000.0, Lambertian(vec3(0.8, 1.0, 0.8))))

main_camera = Camera()
p_russian_roulette = 0.8

def ray_color(r, scene):
    rec = scene.hit(r, 0.0001, math.inf)
    if rec.success:
        if random_float() > p_russian_roulette:
            return vec3.zero()
        fr, wi, pdf = rec.material.sample(rec)
        li = ray_color(ray(rec.pos, wi), scene)
        cosval = dot(wi, rec.normal)
        col = li * fr * cosval / pdf
        return col
    else:
        return lerp(vec3(1.0), vec3(0.4, 0.6, 1.0), 0.5 * (r.direction.y() + 1.0) * 0.8 + 0.2);

def calc_pixel(x, y):
    uv = (float(x) / width, float(y) / height)
    r = main_camera.gen_ray(uv[0], uv[1])
    return ray_color(r, main_scene)

def main():
    output_filename = "./output/image.ppm"
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]

    img = []
    for j in range(height):
        row = []
        print(f'Scanlines: {j + 1}/{height}')
        for i in range(width):
            col = vec3(0.0)
            for k in range(spp):
                col += calc_pixel(i + random.random(), height - 1 - j + random.random())
            col /= float(spp)
            row.append(col)
        img.append(row)

    output_ppm(output_filename, img)

if __name__ == "__main__":
    main()
