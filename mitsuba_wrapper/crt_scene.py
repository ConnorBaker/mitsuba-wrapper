from collections.abc import Mapping

from mitsuba_wrapper.bsdf import BSDF, Dielectric, Diffuse
from mitsuba_wrapper.film import HDRFilm
from mitsuba_wrapper.integrator import Integrator, Path, VolPathMis
from mitsuba_wrapper.ref import ID
from mitsuba_wrapper.sampler import Orthogonal
from mitsuba_wrapper.scene import Scene
from mitsuba_wrapper.screen.virtual_display import VirtualDisplay
from mitsuba_wrapper.sensor import Perspective, Sensor
from mitsuba_wrapper.shape import Cube, Instance, Rectangle, Ref, Shape, ShapeGroup
from mitsuba_wrapper.spectrum import RGB
from mitsuba_wrapper.utils import Color3f, Transform4f

bsdfs: Mapping[ID, BSDF] = {
    ID("gray"): Diffuse(reflectance=RGB(value=Color3f(root=(0.85, 0.85, 0.85)))),
    ID("white"): Diffuse(reflectance=RGB(value=Color3f(root=(0.885809, 0.698859, 0.666422)))),
    ID("green"): Diffuse(reflectance=RGB(value=Color3f(root=(0.105421, 0.37798, 0.076425)))),
    ID("red"): Diffuse(reflectance=RGB(value=Color3f(root=(0.570068, 0.0430135, 0.0443706)))),
    ID("glass"): Dielectric(int_ior="pyrex"),
}

# TODO: Is there no way to get rid of the factor of five throughout all of these?
# NOTE: Rectangles have a length of 2 for all their sides.
the_room: ShapeGroup = ShapeGroup.model_validate({
    ID("floor"): Rectangle(
        to_world=Transform4f.scale_rotate_translate(
            scale=(5, 5, 1),  # rectangle has side length 10
            rotate_axis=(1, 0, 0),
            rotate_degrees=-90,
            translate=(5, 0, -5),  # Origin is bottom left corner
        ),
        bsdf=Ref(id=ID("gray")),
    ),
    ID("ceiling"): Rectangle(
        to_world=Transform4f.scale_rotate_translate(
            scale=(5, 5, 1),
            rotate_axis=(1, 0, 0),
            rotate_degrees=90,
            translate=(5, 10, -5),
        ),
        bsdf=Ref(id=ID("gray")),
    ),
    ID("back_wall"): Rectangle(
        to_world=Transform4f.scale_rotate_translate(
            scale=(5, 5, 1),
            translate=(5, 5, -10),
        ),
        bsdf=Ref(id=ID("gray")),
    ),
    ID("right_wall"): Rectangle(
        to_world=Transform4f.scale_rotate_translate(
            scale=(5, 5, 1),
            rotate_axis=(0, 1, 0),
            rotate_degrees=-90,
            translate=(10, 5, -5),
        ),
        bsdf=Ref(id=ID("red")),
    ),
    ID("left_wall"): Rectangle(
        to_world=Transform4f.scale_rotate_translate(
            scale=(5, 5, 1),
            rotate_axis=(0, 1, 0),
            rotate_degrees=90,
            translate=(0, 5, -5),
        ),
        bsdf=Ref(id=ID("green")),
    ),
    ID("glass_pane"): Cube(
        to_world=Transform4f.scale_rotate_translate(
            # cube in [-1,-1,-1] to [1,1,1] is scaled to prism in ((-4,-3,-0.1), (4,3,0.1))
            scale=(4, 3, 0.1),
            # prism is moved from ((-4,-3,-0.1), (4,3,0.1)) to ((0,0,-8.1), (8,6,-7.9))
            translate=(4, 3, -8),
        ),
        bsdf=Ref(id=ID("glass")),
    ),
})


shapes: Mapping[ID, Shape] = {
    ID("the_room"): the_room,
    ID("our_room"): Instance(shapegroup=Ref(id=ID("the_room"))),
} | VirtualDisplay(
    height_resolution=30,
    width_resolution=40,
    height_length=3,
    width_length=4,
).to_shapes(origin=(0.5, 0.5, -8.101))


config: Mapping[ID, Integrator | Sensor] = {
    ID("integrator"): VolPathMis(),
    ID("sensor"): Perspective(
        fov_axis="smaller",
        focus_distance=1000,
        fov=39.3077,
        near_clip=0.001,
        far_clip=100.0,
        to_world=Transform4f.look_at(
            # Camera is 10 units away, 5 units up
            # `y` is up, `z` is depth
            origin=(5, 10, 10),
            target=(5, 0, -5),
            up=(0, 1, 0),
        ),
        sampler=Orthogonal(sample_count=4),
        film=HDRFilm(
            width=512,
            height=384,
            # width=1024,
            # height=768,
            sample_border=True,
            compensate=True,
            component_format="float32",
        ),
    ),
}

my_scene = Scene.model_validate(config | bsdfs | shapes)
