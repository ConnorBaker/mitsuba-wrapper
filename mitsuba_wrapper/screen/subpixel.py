from mitsuba_wrapper.emitter import Area
from mitsuba_wrapper.shape import Cube
from mitsuba_wrapper.spectrum import RGB
from mitsuba_wrapper.utils import Color3f, Transform4f


def subpixel(
    intensities: tuple[float, float, float],
    origin: tuple[float, float, float],
    shift_up: tuple[bool, bool, bool],
    lengths: tuple[float, float, float],
) -> Cube:
    """
    A subpixel is a cube with a given radiance, placed at a given origin,
    where the origin is the bottom left corner of the cube.

    Args:
        radiance: The radiance of the subpixel.
        origin: The origin of the subpixel (x, y, z)
        shift_up: The direction to shift the subpixel (x, y, z) to align it with the origin
        lengths: The dimensions of the subpixel (x, y, z)
    """
    (x, y, z) = origin
    (x_length, y_length, z_length) = lengths
    (x_up, y_up, z_up) = shift_up
    # Reminder: The cube is in [-1,-1,-1] to [1,1,1], so the sides have length 2.
    # We want the sides to have length `lengths`, so we scale by `lengths / 2`.
    scale = (x_length / 2, y_length / 2, z_length / 2)
    translate = (
        # Change the sign of the translation depending on the direction of the subpixel
        # 2 * bool - 1 is 1 if bool is True, -1 if bool is False.
        x + (2 * x_up - 1) * x_length / 2,
        y + (2 * y_up - 1) * y_length / 2,
        z + (2 * z_up - 1) * z_length / 2,
    )
    return Cube(
        to_world=Transform4f.scale_rotate_translate(scale=scale, translate=translate),
        emitter=Area(radiance=RGB(value=Color3f(root=intensities))),
    )
