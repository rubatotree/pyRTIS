from mathlib.graphics_math import *
from scene_object.scene_object import *
from scene_object.scene_object_group import *
from scene_object.primitives import *
from scene_object.skybox import *
from scene_object.lights import *
from scene_object.camera import *
from materials.material import *

class Scene:
    def __init__(self, object_root = SceneObjectGroup(), main_camera = Camera(), skybox = SkyBox_ColorFill()):
        self.object_root = object_root
        self.main_camera = main_camera
        self.skybox = skybox

def scene_cornell_box() -> Scene:
    obj_root = SceneObjectGroup()
    mat = SimpleLambertian(vec3(1.0, 1.0, 1.0))
    matc = SimpleLambertian(vec3(1.0, 1.0, 1.0))
    matl = SimpleLambertian(vec3(1.0, 0.0, 0.0))
    matr = SimpleLambertian(vec3(0.0, 1.0, 0.0))
    obj_root.append(Triangle((vec3(-1.0, -1.0, -1.0), vec3( 1.0, -1.0, -1.0), vec3(-1.0,  1.0, -1.0)), mat))
    obj_root.append(Triangle((vec3( 1.0, -1.0, -1.0), vec3( 1.0,  1.0, -1.0), vec3(-1.0,  1.0, -1.0)), mat))
    obj_root.append(Triangle((vec3(-1.0, -1.0, -1.0), vec3(-1.0, -1.0,  1.0), vec3( 1.0, -1.0,  1.0)), mat))
    obj_root.append(Triangle((vec3(-1.0, -1.0, -1.0), vec3( 1.0, -1.0,  1.0), vec3( 1.0, -1.0, -1.0)), mat))
    obj_root.append(Triangle((vec3(-1.0, -1.0,  1.0), vec3(-1.0, -1.0, -1.0), vec3(-1.0,  1.0,  1.0)), matl))
    obj_root.append(Triangle((vec3(-1.0, -1.0, -1.0), vec3(-1.0,  1.0, -1.0), vec3(-1.0,  1.0,  1.0)), matl))
    obj_root.append(Triangle((vec3( 1.0, -1.0,  1.0), vec3( 1.0,  1.0,  1.0), vec3( 1.0, -1.0, -1.0)), matr))
    obj_root.append(Triangle((vec3( 1.0, -1.0, -1.0), vec3( 1.0,  1.0,  1.0), vec3( 1.0,  1.0, -1.0)), matr))
    obj_root.append(Triangle((vec3(-1.0,  1.0, -1.0), vec3( 1.0,  1.0,  1.0), vec3(-1.0,  1.0,  1.0)), mat))
    obj_root.append(Triangle((vec3(-1.0,  1.0, -1.0), vec3( 1.0,  1.0, -1.0), vec3( 1.0,  1.0,  1.0)), mat))
    v0 = vec3(-0.75, -1.0, 0.0)
    v1 = vec3(0.5, 0.0, -0.2)
    v2 = vec3(0.2, 0.0, 0.5)
    v3 = vec3(0.0, 1.2, 0.0)
    obj_root.append(Triangle((v0     , v0 + v1 + v2     , v0 + v2          ), matc))
    obj_root.append(Triangle((v0     , v0 + v1          , v0 + v1 + v2     ), matc))
    obj_root.append(Triangle((v0 + v3, v0 + v1 + v2 + v3, v0 + v2 + v3     ), matc))
    obj_root.append(Triangle((v0 + v3, v0 + v1 + v3     , v0 + v1 + v2 + v3), matc))
    obj_root.append(Triangle((v0     , v0 + v1 + v3     , v0 + v1          ), matc))
    obj_root.append(Triangle((v0     , v0 + v3          , v0 + v1 + v3     ), matc))
    obj_root.append(Triangle((v0 + v2, v0 + v1 + v3 + v2, v0 + v1 + v2     ), matc))
    obj_root.append(Triangle((v0 + v2, v0 + v3 + v2     , v0 + v1 + v3 + v2), matc))
    obj_root.append(Triangle((v0     , v0 + v3 + v2     , v0 + v2          ), matc))
    obj_root.append(Triangle((v0     , v0 + v3          , v0 + v3 + v2     ), matc))
    obj_root.append(Triangle((v0 + v1, v0 + v3 + v2 + v1, v0 + v2 + v1     ), matc))
    obj_root.append(Triangle((v0 + v1, v0 + v3 + v1     , v0 + v3 + v2 + v1), matc))
    obj_root.append(Sphere(vec3(0.45, -0.7, 0.3), 0.3, SimpleMetal(vec3(1.0))))

    radiance = vec3(20.0)
    obj_root.append(TriangleLight((vec3(-0.25,  0.95, -0.25), vec3( 0.25,  0.95, 0.25), vec3( -0.25,  0.95,  0.25)), radiance))
    obj_root.append(TriangleLight((vec3(-0.25,  0.95, -0.25), vec3( 0.25,  0.95, -0.25), vec3( 0.25,  0.95,  0.25)), radiance))
    main_camera = Camera()
    main_camera.set_pos(vec3(0.0, 0.0, 4.0))
    main_camera.look_at(vec3(0.0, 0.0, 0.0))
    return Scene(obj_root, main_camera, SkyBox_NeonNight())

def scene_one_weekend() -> Scene:
    obj_root = SceneObjectGroup()
    checklist = []
    obj_root.append(Sphere(vec3(0, -10000, -1), 10000, SimpleLambertian(vec3(0.4, 0.4, 0.45))))
    obj_root.append(Sphere(vec3(-1.5, 1, -1.5), 1, SimpleLambertian(vec3(1.0, 0.4, 0.4))))
    obj_root.append(Sphere(vec3(0.0, 1, 0.0), 1, SimpleMetal(vec3(0.9, 0.9, 1.0))))
    obj_root.append(Sphere(vec3(1.5, 1, 1.5), 1, SimpleTransparent(1.5)))
    checklist.append((vec3(-1.5, 1, 1.5), 1))
    checklist.append((vec3(0, 1, 0), 1))
    checklist.append((vec3(1.5, 1, 1.5), 1))

    for i in range(400):
        x = (random_float() - 0.5) * 20
        z = (random_float() - 0.5) * 20 - 5
        pos = vec3(x, 0.2, z)
        flag = False
        for check in checklist:
            if (check[0] - pos).norm() < check[1] + 0.2 + 0.1:
                flag = True
                break
        if flag:
            continue

        checklist.append((pos, 0.2))

        p = random_float()
        col = vec3(random_float() * random_float(), random_float() * random_float(), random_float() * random_float())
        fuz = random_float()
        fuz *= fuz
        fuz = clamp(fuz - 0.5, 0.0, 1.0)

        if p < 0.4:
            obj_root.append(Sphere(pos, 0.2, SimpleLambertian(col)))
        elif p < 0.7:
            obj_root.append(Sphere(pos, 0.2, SimpleMetal(col, fuz)))
        else:
            obj_root.append(Sphere(pos, 0.2, SimpleTransparent(1.5)))

    main_camera = Camera()
    main_camera.set_pos(vec3(0.0, 1.5, 5.0))
    main_camera.look_at(vec3(0.0, 0.5, 0.0))

    return Scene(obj_root, main_camera, SkyBox_OneWeekend())
