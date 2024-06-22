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
        self.domelight = DomeLight(skybox)
        self.base_list = object_root.get_objects()
        self.light_list = LightList()
        self.light_list.domelight = self.domelight
        for obj in self.base_list:
            if isinstance(obj, Light):
                self.light_list.append(obj)
        if environment_as_light:
            self.light_list.append(self.domelight)
    def hit(self, r:ray, t_min:float, t_max:float):
        rec_temp = self.object_root.hit(r, t_min, t_max)
        if rec_temp.success:
            return rec_temp
        else:
            rec = HitRecord(vec3(math.inf) * r.direction, -r.direction, math.inf, success=False, obj=self.domelight)
            rec.material = self.domelight.material
            rec.isLight = True
            return rec

def scene_skybox_test() -> Scene:
    obj_root = SceneObjectGroup()
    obj_root.append(Sphere(vec3(0.0), 0.5, SimpleMetal(vec3(1.00))))
    main_camera = Camera()
    main_camera.set_pos(vec3(0, 0, 4))
    main_camera.look_at(vec3(0.0, 0.0, 0.0))
    skybox = SkyBox_FromCubeMap("miramar")
    return Scene(obj_root, main_camera, skybox)

def scene_cornell_box() -> Scene:
    obj_root = SceneObjectGroup()
    mat  = SimpleLambertian(vec3(1.0, 1.0, 1.0))
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
    obj_root.append(Sphere(vec3(0.45, -0.7, -0.1), 0.3, SimpleMetal(vec3(1.0, 0.6, 0.8))))
    # obj_root.append(Sphere(vec3(0.45, -0.7, 0.3), 0.3, mat))
    # obj_root.append(Sphere(vec3(0.1, -0.8, 0.7), 0.2, SimpleTransparent(1.5)))

    obj_root.append(Sphere(vec3(-0.7, -0.85, 0.7), 0.15, SimpleMetal(vec3(1.0), 0.0)))
    # obj_root.append(Sphere(vec3(-0.7, -0.85, 0.7), 0.15, SimpleLambertian(vec3(1.0))))
    obj_root.append(Sphere(vec3(-0.35, -0.85, 0.7), 0.15, SimpleMetal(vec3(1.0), 0.2)))
    obj_root.append(Sphere(vec3( 0.0, -0.85, 0.7), 0.15, SimpleMetal(vec3(1.0), 0.4)))
    obj_root.append(Sphere(vec3( 0.35, -0.85, 0.7), 0.15, SimpleMetal(vec3(1.0), 0.7)))
    obj_root.append(Sphere(vec3( 0.7, -0.85, 0.7), 0.15, SimpleMetal(vec3(1.0), 1.0)))

    radiance = vec3(3.0)
    obj_root.append(TriangleLight((vec3(-0.25,  0.95, -0.25), vec3( 0.25,  0.95, 0.25), vec3( -0.25,  0.95,  0.25)), radiance))
    obj_root.append(TriangleLight((vec3(-0.25,  0.95, -0.25), vec3( 0.25,  0.95, -0.25), vec3( 0.25,  0.95,  0.25)), radiance))
    # obj_root.append(SphereLight(vec3(0.0, 0.5, 0.0), 0.1, radiance))
    main_camera = Camera()
    main_camera.set_pos(vec3(0.0, 0.0, 4.0))
    main_camera.look_at(vec3(0.0, 0.0, 0.0))
    skybox = SkyBox_NeonNight()
    # skybox = SkyBox_ColorFill(vec3(0.0))
    return Scene(obj_root, main_camera, skybox)

def scene_cornell_box_cubemap() -> Scene:
    scene = scene_cornell_box()
    skybox = SkyBox_FromCubeMap("miramar")
    return Scene(scene.object_root, scene.main_camera, skybox)

def scene_cornell_box_no_specular() -> Scene:
    obj_root = SceneObjectGroup()
    mat  = SimpleLambertian(vec3(1.0, 1.0, 1.0))
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
    obj_root.append(Sphere(vec3(0.45, -0.7, -0.1), 0.3, SimpleLambertian(vec3(0.6, 0.6, 1.0))))
    # obj_root.append(Sphere(vec3(0.45, -0.7, 0.3), 0.3, mat))
    # obj_root.append(Sphere(vec3(0.1, -0.8, 0.7), 0.2, SimpleTransparent(1.5)))

    obj_root.append(Sphere(vec3(-0.7, -0.85, 0.7), 0.15, SimpleMetal(vec3(1.0), 0.2)))
    obj_root.append(Sphere(vec3(-0.35, -0.85, 0.7), 0.15, SimpleMetal(vec3(1.0), 0.4)))
    obj_root.append(Sphere(vec3( 0.0, -0.85, 0.7), 0.15, SimpleMetal(vec3(1.0), 0.6)))
    obj_root.append(Sphere(vec3( 0.35, -0.85, 0.7), 0.15, SimpleMetal(vec3(1.0), 0.8)))
    obj_root.append(Sphere(vec3( 0.7, -0.85, 0.7), 0.15, SimpleMetal(vec3(1.0), 1.0)))

    radiance = vec3(6.0)
    obj_root.append(TriangleLight((vec3(-0.25,  0.95, -0.25), vec3( 0.25,  0.95, 0.25), vec3( -0.25,  0.95,  0.25)), radiance))
    obj_root.append(TriangleLight((vec3(-0.25,  0.95, -0.25), vec3( 0.25,  0.95, -0.25), vec3( 0.25,  0.95,  0.25)), radiance))
    # obj_root.append(SphereLight(vec3(0.0, 0.5, 0.0), 0.1, radiance))
    main_camera = Camera()
    main_camera.set_pos(vec3(0.0, 0.0, 4.0))
    main_camera.look_at(vec3(0.0, 0.0, 0.0))
    skybox = SkyBox_NeonNight()
    return Scene(obj_root, main_camera, skybox)


def scene_cornell_ao() -> Scene:
    obj_root = SceneObjectGroup()
    mat  = SimpleLambertian(vec3(1.0, 1.0, 1.0))
    matc = SimpleLambertian(vec3(1.0, 1.0, 1.0))
    matl = SimpleLambertian(vec3(1.0, 0.0, 0.0))
    matr = SimpleLambertian(vec3(0.0, 1.0, 0.0))
    obj_root.append(Triangle((vec3(-1.0, -1.0, -1.0), vec3(-1.0, -1.0,  1.0), vec3( 1.0, -1.0,  1.0)), mat))
    obj_root.append(Triangle((vec3(-1.0, -1.0, -1.0), vec3( 1.0, -1.0,  1.0), vec3( 1.0, -1.0, -1.0)), mat))
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
    obj_root.append(Sphere(vec3(0.45, -0.7, -0.1), 0.3, SimpleMetal(vec3(1.0, 0.6, 0.8))))
    # obj_root.append(Sphere(vec3(0.45, -0.7, -0.1), 0.3, matc))
    # obj_root.append(Sphere(vec3(0.45, -0.7, 0.3), 0.3, mat))

    obj_root.append(Sphere(vec3(-0.7, -0.85, 0.7), 0.15, SimpleMetal(vec3(1.0), 0.0)))
    obj_root.append(Sphere(vec3(-0.35, -0.85, 0.7), 0.15, SimpleMetal(vec3(1.0), 0.2)))
    obj_root.append(Sphere(vec3( 0.0, -0.85, 0.7), 0.15, SimpleMetal(vec3(1.0), 0.4)))
    obj_root.append(Sphere(vec3( 0.35, -0.85, 0.7), 0.15, SimpleMetal(vec3(1.0), 0.7)))
    obj_root.append(Sphere(vec3( 0.7, -0.85, 0.7), 0.15, SimpleMetal(vec3(1.0), 1.0)))
    # obj_root.append(Sphere(vec3(-0.7, -0.85, 0.7), 0.15,  matc))
    # obj_root.append(Sphere(vec3(-0.35, -0.85, 0.7), 0.15, matc))
    # obj_root.append(Sphere(vec3( 0.0, -0.85, 0.7), 0.15,  matc))
    # obj_root.append(Sphere(vec3( 0.35, -0.85, 0.7), 0.15, matc))
    # obj_root.append(Sphere(vec3( 0.7, -0.85, 0.7), 0.15,  matc))

    main_camera = Camera()
    main_camera.set_pos(vec3(0.0, 0.0, 4.0))
    main_camera.look_at(vec3(0.0, 0.0, 0.0))
    # skybox = SkyBox_OneWeekend()
    # skybox = SkyBox_ColorFill(vec3(1.0, 0.0, 1.0))
    skybox = SkyBox_FromCubeMap("miramar")
    return Scene(obj_root, main_camera, skybox)

def scene_cornell_Light() -> Scene:
    obj_root = SceneObjectGroup()
    mat  = SimpleLambertian(vec3(1.0, 1.0, 1.0))
    matc = SimpleLambertian(vec3(1.0, 1.0, 1.0))
    matl = SimpleLambertian(vec3(1.0, 0.0, 0.0))
    matr = SimpleLambertian(vec3(0.0, 1.0, 0.0))
    obj_root.append(Triangle((vec3(-1.0, -1.0, -1.0), vec3(-1.0, -1.0,  1.0), vec3( 1.0, -1.0,  1.0)), mat))
    obj_root.append(Triangle((vec3(-1.0, -1.0, -1.0), vec3( 1.0, -1.0,  1.0), vec3( 1.0, -1.0, -1.0)), mat))
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
    obj_root.append(Sphere(vec3(0.45, -0.7, -0.1), 0.3, SimpleMetal(vec3(1.0, 0.6, 0.8))))
    # obj_root.append(Sphere(vec3(0.45, -0.7, 0.3), 0.3, mat))
    # obj_root.append(Sphere(vec3(0.1, -0.8, 0.7), 0.2, SimpleTransparent(1.5)))
    radiance = vec3(3.0)
    # obj_root.append(SphereLight(vec3(0.0, 0.5, 0.0), 0.1, radiance))
    obj_root.append(TriangleLight((vec3(-0.25,  0.95, -0.25), vec3( 0.25,  0.95, 0.25), vec3( -0.25,  0.95,  0.25)), radiance))
    obj_root.append(TriangleLight((vec3(-0.25,  0.95, -0.25), vec3( 0.25,  0.95, -0.25), vec3( 0.25,  0.95,  0.25)), radiance))

    obj_root.append(Sphere(vec3(-0.7, -0.85, 0.7), 0.15, SimpleMetal(vec3(1.0), 0.0)))
    obj_root.append(Sphere(vec3(-0.35, -0.85, 0.7), 0.15, SimpleMetal(vec3(1.0), 0.2)))
    obj_root.append(Sphere(vec3( 0.0, -0.85, 0.7), 0.15, SimpleMetal(vec3(1.0), 0.4)))
    obj_root.append(Sphere(vec3( 0.35, -0.85, 0.7), 0.15, SimpleMetal(vec3(1.0), 0.7)))
    obj_root.append(Sphere(vec3( 0.7, -0.85, 0.7), 0.15, SimpleMetal(vec3(1.0), 1.0)))

    main_camera = Camera()
    main_camera.set_pos(vec3(0.0, 0.0, 4.0))
    main_camera.look_at(vec3(0.0, 0.0, 0.0))
    skybox = SkyBox_ColorFill(vec3(0))
    return Scene(obj_root, main_camera, skybox)

def scene_mis() -> Scene:
    obj_root = SceneObjectGroup()
    theta_range = math.pi * 0.4
    theta_min = -math.pi / 2 - theta_range / 7 / 2
    theta_max = theta_min + theta_range
    radius = 1.0
    width = 2.0
    fuzz_list = [1, 0.5, 0.1, 0.0]
    for i in range(4):
        fuzz = fuzz_list[i]
        theta_min_i = theta_min + theta_range / 7 * 2 * i
        theta_max_i = theta_min + theta_range / 7 * (2 * i + 1.75)
        z1 = -math.cos(theta_min_i) * radius
        z2 = -math.cos(theta_max_i) * radius
        y1 = math.sin(theta_min_i) * radius
        y2 = math.sin(theta_max_i) * radius
        if i == 3:
            y2 += (y2 - y1) * 2
            z2 += (z2 - z1) * 2
        x1 = -width / 2
        x2 = width / 2
        p1 = vec3(x1, y1, z1)
        p2 = vec3(x2, y1, z1)
        p3 = vec3(x1, y2, z2)
        p4 = vec3(x2, y2, z2)
        mat = SimpleMetal(vec3(0.1), fuzz)
        obj_root.append(Triangle((p1, p2, p3), mat))
        obj_root.append(Triangle((p3, p2, p4), mat))

    mat = SimpleLambertian(vec3(0.5))
    v1 = vec3(-20, -1.3, -20)
    v2 = vec3(20, -1.3, -20)
    v3 = vec3(20, -1.3, 20)
    v4 = vec3(-20, -1.3, 20)
    obj_root.append(Triangle((v1, v2, v3), mat))
    obj_root.append(Triangle((v3, v4, v1), mat))

    l_width = width * 1.3

    obj_root.append(SphereLight(vec3(-l_width / 2 + 1 * l_width / 5, 0.3, -0.5), 0.01, 20 * vec3(1.0, 0.6, 0.8), True))
    obj_root.append(SphereLight(vec3(-l_width / 2 + 2 * l_width / 5, 0.3, -0.5), 0.02, 20 * vec3(0.6, 1.0, 0.6), True))
    obj_root.append(SphereLight(vec3(-l_width / 2 + 3 * l_width / 5, 0.3, -0.5), 0.04, 20 * vec3(1.0, 1.0, 0.6), True))
    obj_root.append(SphereLight(vec3(-l_width / 2 + 4 * l_width / 5, 0.3, -0.5), 0.15, 20 * vec3(0.6, 0.8, 1.0), True))

    main_camera = Camera()
    main_camera.set_pos(vec3(0.0, 0.1, 2.0))
    main_camera.look_at(vec3(0.0, -0.5, -0.7))
    skybox = SkyBox_ColorFill(vec3(0.1))
    return Scene(obj_root, main_camera, skybox)

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
