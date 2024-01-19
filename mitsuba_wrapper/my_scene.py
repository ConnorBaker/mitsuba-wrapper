from collections.abc import Mapping

from mitsuba_wrapper.bsdf import BSDF, Conductor, Dielectric, Diffuse
from mitsuba_wrapper.emitter import Area
from mitsuba_wrapper.film import HDRFilm
from mitsuba_wrapper.integrator import Integrator, VolPathMis
from mitsuba_wrapper.ref import ID
from mitsuba_wrapper.sampler import Orthogonal, Independent
from mitsuba_wrapper.scene import Scene
from mitsuba_wrapper.sensor import Perspective, Sensor
from mitsuba_wrapper.shape import Instance, Rectangle, Ref, Shape, ShapeGroup, Sphere
from mitsuba_wrapper.spectrum import RGB
from mitsuba_wrapper.utils import Color3f, Transform4f

bsdfs: Mapping[ID, BSDF] = {
    ID("gray"): Diffuse(reflectance=RGB(value=Color3f(root=(0.85, 0.85, 0.85)))),
    ID("white"): Diffuse(reflectance=RGB(value=Color3f(root=(0.885809, 0.698859, 0.666422)))),
    ID("green"): Diffuse(reflectance=RGB(value=Color3f(root=(0.105421, 0.37798, 0.076425)))),
    ID("red"): Diffuse(reflectance=RGB(value=Color3f(root=(0.570068, 0.0430135, 0.0443706)))),
    ID("glass"): Dielectric(),
    ID("mirror"): Conductor(),
}


# TODO: Is there no way to get rid of the factor of five throughout all of these?
the_room: ShapeGroup = ShapeGroup.model_validate({
    ID("floor"): Rectangle(
        to_world=Transform4f.scale_rotate_translate(
            scale=(5, 5, 1),
            rotate_axis=(1, 0, 0),
            rotate_degrees=-90,
            translate=(0, 0, -10),
        ),
        bsdf=Ref(id=ID("gray")),
    ),
    ID("ceiling"): Rectangle(
        to_world=Transform4f.scale_rotate_translate(
            scale=(5, 5, 1),
            rotate_axis=(1, 0, 0),
            rotate_degrees=90,
            translate=(0, 10, -10),
        ),
        bsdf=Ref(id=ID("gray")),
    ),
    ID("back_wall"): Rectangle(
        to_world=Transform4f.scale_rotate_translate(
            scale=(5, 5, 1),
            translate=(0, 5, -15),
        ),
        bsdf=Ref(id=ID("gray")),
    ),
    ID("right_wall"): Rectangle(
        to_world=Transform4f.scale_rotate_translate(
            scale=(5, 5, 1),
            rotate_axis=(0, 1, 0),
            rotate_degrees=-90,
            translate=(5, 5, -10),
        ),
        bsdf=Ref(id=ID("red")),
    ),
    ID("left_wall"): Rectangle(
        to_world=Transform4f.scale_rotate_translate(
            scale=(5, 5, 1),
            rotate_axis=(0, 1, 0),
            rotate_degrees=90,
            translate=(-5, 5, -10),
        ),
        bsdf=Ref(id=ID("green")),
    ),
    ID("mirror_sphere"): Sphere(
        to_world=Transform4f.scale_rotate_translate(
            scale=(0.5, 0.5, 0.5),
            translate=(-0.3, 4, -8),
        ),
        bsdf=Ref(id=ID("mirror")),
    ),
    ID("glass_sphere"): Sphere(
        to_world=Transform4f.scale_rotate_translate(translate=(0.5, 7, -3.4)),
        bsdf=Ref(id=ID("glass")),
    ),
})


shapes: Mapping[ID, Shape] = {
    ID("the_room"): the_room,
    ID("our_room"): Instance(
        shapegroup=Ref(id=ID("the_room")),
    ),
    ID("light"): Rectangle(
        to_world=Transform4f.scale_rotate_translate(
            rotate_axis=(1, 0, 0),
            rotate_degrees=90,
            translate=(0, 9.9, -10),
        ),
        bsdf=Ref(id=ID("white")),
        emitter=Area(radiance=RGB(value=Color3f(root=(18.387, 13.9873, 6.75357)))),
    ),
}


config: Mapping[ID, Integrator | Sensor] = {
    ID("integrator"): VolPathMis(rr_depth=2**10),
    ID("sensor"): Perspective(
        fov_axis="smaller",
        focus_distance=1000,
        fov=39.3077,
        near_clip=0.001,
        far_clip=100.0,
        to_world=Transform4f.look_at(
            # Camera is 10 units away, 5 units up
            # `y` is up, `z` is depth
            origin=(0, 5, 10),
            target=(0, 5, 0),
            up=(0, 1, 0),
        ),
        # sampler=Orthogonal(sample_count=4),
        sampler=Independent(sample_count=4),
        film=HDRFilm(
            width=1024,
            height=768,
            sample_border=True,
            compensate=True,
        ),
    ),
}

my_scene = Scene.model_validate(config | bsdfs | shapes)
