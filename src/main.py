import sys
from mathlib.graphics_math import *
from img_io.img_output import *

width, height = 400, 200

def calc_pixel(x, y):
    uv = (float(x) / width, float(y) / height)
    col = vec3(uv[0], uv[1], 1) * vec3(0.8, 0.4, 0.4)
    return col

def main():
    img = []
    for j in range(height):
        row = []
        print(f'Scanlines: {j + 1}/{height}')
        for i in range(width):
            row.append(calc_pixel(i, j))
        img.append(row)

    output_filename = "./output/temp.ppm"
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
    output_ppm(output_filename, img)

if __name__ == "__main__":
    main()
