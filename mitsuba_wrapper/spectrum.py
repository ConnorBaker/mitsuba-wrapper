from typing import Literal, final

from pydantic import BaseModel, Field

from mitsuba_wrapper.utils import Color3f

type RGBType = Literal["rgb"]
type SRGBType = Literal["srgb"]
type UniformType = Literal["uniform"]

type SpectrumType = RGBType | SRGBType | UniformType
type Spectrum = RGB | SRGB | Uniform


@final
class Uniform(BaseModel, frozen=True):
    wavelength_min: None | float = Field(
        default=None,
        description="Minimum wavelength of the spectral range in nanometers",
    )
    wavelength_max: None | float = Field(
        default=None,
        description="Maximum wavelength of the spectral range in nanometers",
    )
    value: float = Field(description="Value of the spectrum")
    type: UniformType = "uniform"


@final
class RGB(BaseModel, frozen=True):
    value: Color3f = Field(description="The corresponding RGB color value.")
    type: RGBType = "rgb"


@final
class SRGB(BaseModel, frozen=True):
    color: None | Color3f = Field(default=None, description="The corresponding sRGB color value.")
    value: None | Color3f = Field(
        default=None,
        description="Spectral upsampling model coefficients of the srgb color value",
    )
    type: SRGBType = "srgb"
