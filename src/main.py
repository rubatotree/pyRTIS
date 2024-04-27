import sys
import random
from mathlib.graphics_math import *
from img_io.img_output import *
from scene_object.scene_object import *
from scene_object.primitives import *
from scene_object.camera import *

width, height = 400, 225
spp = 32
obj = Sphere(vec3(0.0, 0.0, 0.0), 0.5)
main_camera = Camera()

def calc_pixel(x, y):
    uv = (float(x) / width, float(y) / height)
    r = main_camera.gen_ray(uv[0], uv[1])
    rec = obj.hit(r, 0.0001, math.inf)
    if rec.success:
        return rec.normal * 0.5 + vec3(0.5)
    else:
        return lerp(vec3(1.0), vec3(0.4, 0.6, 1.0), 0.5 * (r.direction.y() + 1.0) * 0.8 + 0.2);

def main():
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

    output_filename = "./output/temp.ppm"
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
    output_ppm(output_filename, img)

if __name__ == "__main__":
    main()
