from collections.abc import Mapping
from itertools import product
from typing import Literal, final

from pydantic import BaseModel, Field

from mitsuba_wrapper.ref import ID
from mitsuba_wrapper.screen.subpixel import subpixel
from mitsuba_wrapper.shape import Shape


@final
class VirtualDisplay(BaseModel, frozen=False, extra="forbid"):
    """
    A virtual display rendered in 3D.
    """

    height_resolution: int = Field(30, gt=0, description="Height of the screen in pixels")
    width_resolution: int = Field(40, gt=0, description="Width of the screen in pixels")

    height_length: float = Field(3, gt=0, description="Height of the screen")
    width_length: float = Field(4, gt=0, description="Width of the screen")

    def to_shapes(self, origin: tuple[float, float, float] = (0, 0, 0)) -> Mapping[ID, Shape]:
        (X, Y, Z) = origin

        # Depth of a pixel -- should not be changed
        pixel_depth: float = 0.0001

        # To find the pixel width and height, we need to solve the equations
        #
        #    height_resolution * (pixel_height + inter_pixel_spacing) + inter_pixel_spacing = height_length
        #    width_resolution * (pixel_width + inter_pixel_spacing) + inter_pixel_spacing = width_length
        #
        # NOTE: This formulation has `inter_pixel_spacing` between each pixel and at the edges.
        inter_pixel_spacing: float = 0.005
        pixel_height: float = (self.height_length - inter_pixel_spacing) / self.height_resolution - inter_pixel_spacing
        pixel_width: float = (self.width_length - inter_pixel_spacing) / self.width_resolution - inter_pixel_spacing

        # To find the subpixel width, we need to solve the equation:
        #
        #    3 * subpixel_width + 2 * intra_pixel_spacing = pixel_width
        #
        # NOTE: The depth and height of the subpixel are the same as the pixel.
        intra_pixel_spacing: float = 0.001
        subpixel_width: float = (pixel_width - 2 * intra_pixel_spacing) / 3

        subpixels: Mapping[Literal["red", "green", "blue"], tuple[float, float, float]] = {
            "red": (10.387, 0.9873, 0.75357),
            "green": (0.387, 10.9873, 0.75357),
            "blue": (0.387, 0.9873, 10.75357),
        }

        subpixel_position: Mapping[Literal["red", "green", "blue"], int] = {
            "red": 0,
            "green": 1,
            "blue": 2,
        }

        shapes: dict[ID, Shape] = {}
        for x, y, c in product(range(self.width_resolution), range(self.height_resolution), ("red", "green", "blue")):
            id = ID(f"{c}_light_{x}_{y}")
            intensities = subpixels[c]
            origin = (
                # The left edge of the screen
                (X + inter_pixel_spacing)
                # The length of all the pixels to the left of this one
                + x * (pixel_width + inter_pixel_spacing)
                # The length of all the subpixels to the left of this one
                + subpixel_position[c] * (intra_pixel_spacing + subpixel_width),
                # The bottom edge of the screen
                (Y + inter_pixel_spacing)
                # The length of all the pixels below this one
                + y * (pixel_height + inter_pixel_spacing),
                # All pixels are at the same depth
                Z,
            )
            # We use negative `z` to indicate distance from the camera.
            shift_up = (True, True, False)
            lengths = (subpixel_width, pixel_height, pixel_depth)
            shapes[id] = subpixel(
                intensities,
                origin,
                shift_up,
                lengths,
            )
        return shapes
