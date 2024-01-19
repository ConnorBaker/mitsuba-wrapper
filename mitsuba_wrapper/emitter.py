from typing import Literal, final

from pydantic import BaseModel, Field

from mitsuba_wrapper.spectrum import Spectrum
from mitsuba_wrapper.utils import Placeable, Point3f

type AreaType = Literal["area"]
type PointType = Literal["point"]

type EmitterType = AreaType | PointType
type Emitter = Area | Point


@final
class Area(BaseModel, frozen=True):
    radiance: Spectrum = Field(
        description="Specifies the emitted radiance in units of power per unit area per unit steradian"
    )
    type: AreaType = "area"


@final
class Point(Placeable, frozen=True):
    intensity: Spectrum = Field(description="Specifies the radiant intensity in units of power per unit steradian")
    position: None | Point3f = Field(
        default=None,
        description="""
            Alternative parameter for specifying the light source position. Note that only one of the parameters
            to_world and position can be used at a time
        """,
    )
    type: PointType = "point"
