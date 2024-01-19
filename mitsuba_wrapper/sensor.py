from typing import Literal, final

from pydantic import Field

from mitsuba_wrapper.film import HDRFilm
from mitsuba_wrapper.sampler import Independent, Sampler
from mitsuba_wrapper.spectrum import Spectrum
from mitsuba_wrapper.utils import Placeable

type PerspectiveType = Literal["perspective"]
type ThinLensType = Literal["thinlens"]

type SensorType = PerspectiveType | ThinLensType
type Sensor = Perspective | ThinLens


class PerspectiveLike(Placeable, frozen=True):
    # TODO: fov and focal_length are mutually exclusive
    fov: None | float = Field(
        default=None,
        description="""
            Denotes the camera's field of view in degrees—must be between 0 and 180, excluding the extremes.
            Alternatively, it is also possible to specify a field of view using the focal_length parameter.
        """,
    )
    focal_length: None | str = Field(
        # default="50mm",
        default=None,
        description="""
            Denotes the camera's focal length specified using 35mm film equivalent units. Alternatively, it is also
            possible to specify a field of view using the fov parameter. See the main description for further details.
            (Default: 50mm)
        """,
    )
    # TODO: focus_distance is an undocumented parameter for Perspective.
    focus_distance: float = Field(
        default=0,
        description="Denotes the world-space distance from the camera's aperture to the focal plane",
    )
    # TODO: RuntimeError: ​[xml_v.cpp:467] Unreferenced property "fov_axis" in plugin of type "thinlens"!
    fov_axis: Literal["x", "y", "diagonal", "smaller", "larger"] = Field(
        default="x",
        description="""
            When the parameter fov is given (and only then), this parameter further specifies the image axis, to which
            it applies.
            x: fov maps to the x-axis in screen space.
            y: fov maps to the y-axis in screen space.
            diagonal: fov maps to the screen diagonal.
            smaller: fov maps to the smaller dimension (e.g. x when width < height)
            larger: fov maps to the larger dimension (e.g. y when width < height)
            The default is x.
        """,
    )
    near_clip: float = Field(default=1e-2, description="Distance to the near/far clip planes")
    far_clip: float = Field(default=1e4, description="Distance to the near/far clip planes")
    srf: None | Spectrum = Field(
        default=None,
        description="Sensor Response Function that defines the spectral sensitivity of the sensor",
    )
    sampler: Sampler = Field(
        default_factory=Independent,
        description="Specifies the sampler to use for generating camera rays",
    )
    film: HDRFilm = Field(
        default_factory=HDRFilm,
        description="Specifies the film to use for storing the rendered image",
    )


@final
class Perspective(PerspectiveLike, arbitrary_types_allowed=True, frozen=True):
    principal_point_offset_x: float = Field(
        default=0,
        description="""
            Specifies the position of the camera's principal point relative to the center of the film
        """,
    )
    principal_point_offset_y: float = Field(
        default=0,
        description="""
            Specifies the position of the camera's principal point relative to the center of the film
        """,
    )
    type: PerspectiveType = "perspective"


@final
class ThinLens(PerspectiveLike, frozen=True):
    aperture_radius: None | float = Field(
        default=None,
        description="Denotes the radius of the camera's aperture in scene units",
    )
    type: ThinLensType = "thinlens"
