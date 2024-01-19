from collections.abc import Mapping

from mitsuba_wrapper.bsdf import BSDF, Conductor, Dielectric, Diffuse
from mitsuba_wrapper.emitter import Area
from mitsuba_wrapper.film import HDRFilm
from mitsuba_wrapper.integrator import Integrator, Path
from mitsuba_wrapper.reconstruction_filter import TentFilter
from mitsuba_wrapper.ref import ID, Ref
from mitsuba_wrapper.sampler import Independent
from mitsuba_wrapper.scene import Scene
from mitsuba_wrapper.sensor import Perspective, Sensor
from mitsuba_wrapper.shape import Obj, Shape, Sphere
from mitsuba_wrapper.spectrum import RGB
from mitsuba_wrapper.utils import Color3f, Transform4f

spp: int = 128
res: int = 256
max_depth: int = 6
integrator: str = "path"

config: Mapping[ID, Integrator | Sensor] = {
    ID("integrator"): Path(max_depth=max_depth),
    ID("sensor"): Perspective(
        fov_axis="smaller",
        near_clip=0.001,
        far_clip=100.0,
        focus_distance=1000,
        fov=39.3077,
        to_world=Transform4f.look_at(
            origin=(0, 0, 4),
            target=(0, 0, 0),
            up=(0, 1, 0),
        ),
        sampler=Independent(sample_count=spp),
        film=HDRFilm(
            width=res,
            height=res,
            pixel_format="rgb",
            component_format="float32",
            rfilter=TentFilter(),
        ),
    ),
}

bsdfs: Mapping[ID, BSDF] = {
    ID("gray"): Diffuse(reflectance=RGB(value=Color3f(root=(0.85, 0.85, 0.85)))),
    ID("white"): Diffuse(reflectance=RGB(value=Color3f(root=(0.885809, 0.698859, 0.666422)))),
    ID("green"): Diffuse(reflectance=RGB(value=Color3f(root=(0.105421, 0.37798, 0.076425)))),
    ID("red"): Diffuse(reflectance=RGB(value=Color3f(root=(0.570068, 0.0430135, 0.0443706)))),
    ID("glass"): Dielectric(),
    ID("mirror"): Conductor(),
}

shapes: Mapping[ID, Shape] = {
    ID("light"): Obj(
        filename="./scenes/meshes/cbox_luminaire.obj",
        to_world=Transform4f.scale_rotate_translate(translate=(0, -0.01, 0)),
        emitter=Area(radiance=RGB(value=Color3f(root=(18.387, 13.9873, 6.75357)))),
        bsdf=Ref(id=ID("white")),
    ),
    ID("floor"): Obj(
        filename="./scenes/meshes/cbox_floor.obj",
        bsdf=Ref(id=ID("white")),
    ),
    ID("ceiling"): Obj(
        filename="./scenes/meshes/cbox_ceiling.obj",
        bsdf=Ref(id=ID("white")),
    ),
    ID("back"): Obj(
        filename="./scenes/meshes/cbox_back.obj",
        bsdf=Ref(id=ID("white")),
    ),
    ID("greenwall"): Obj(
        filename="./scenes/meshes/cbox_greenwall.obj",
        bsdf=Ref(id=ID("green")),
    ),
    ID("redwall"): Obj(
        filename="./scenes/meshes/cbox_redwall.obj",
        bsdf=Ref(id=ID("red")),
    ),
    ID("mirrorsphere"): Sphere(
        to_world=Transform4f.scale_rotate_translate(
            scale=(0.5, 0.5, 0.5),
            translate=(-0.3, -0.5, 0.2),
        ),
        bsdf=Ref(id=ID("mirror")),
    ),
    ID("glasssphere"): Sphere(
        to_world=Transform4f.scale_rotate_translate(
            scale=(0.25, 0.25, 0.25),
            translate=(0.5, -0.75, -0.2),
        ),
        bsdf=Ref(id=ID("glass")),
    ),
}

cbox = Scene.model_validate(bsdfs | shapes | config)
