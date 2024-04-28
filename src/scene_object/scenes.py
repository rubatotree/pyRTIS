from mathlib.graphics_math import *
from scene_object.scene_object import *
from scene_object.scene_object_group import *
from scene_object.primitives import *
from scene_object.skybox import *
from scene_object.camera import *
from materials.material import *

class Scene:
    def __init__(self, object_root = SceneObjectGroup(), main_camera = Camera(), skybox = SkyBox_ColorFill()):
        self.object_root = object_root
        self.main_camera = main_camera
        self.skybox = skybox

def scene_one_weekend() -> Scene:
    obj_root = SceneObjectGroup()
    checklist = []
    obj_root.append(Sphere(vec3(0, -10000, -1), 10000, Lambertian(vec3(0.4, 0.4, 0.45))))
    obj_root.append(Sphere(vec3(-1.5, 1, -1.5), 1, Lambertian(vec3(1.0, 0.4, 0.4))))
    obj_root.append(Sphere(vec3(0.0, 1, 0.0), 1, Metal(vec3(0.9, 0.9, 1.0))))
    obj_root.append(Sphere(vec3(1.5, 1, 1.5), 1, Transparent(1.5)))
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
            obj_root.append(Sphere(pos, 0.2, Lambertian(col)))
        elif p < 0.7:
            obj_root.append(Sphere(pos, 0.2, Metal(col, fuz)))
        else:
            obj_root.append(Sphere(pos, 0.2, Transparent(1.5)))

    main_camera = Camera()
    main_camera.set_pos(vec3(0.0, 1.5, 5.0))
    main_camera.look_at(vec3(0.0, 0.5, 0.0))

    return Scene(obj_root, main_camera, SkyBox_OneWeekend())
