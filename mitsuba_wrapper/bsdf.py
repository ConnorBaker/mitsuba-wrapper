from typing import Literal, final

from pydantic import BaseModel, Field

from mitsuba_wrapper.spectrum import RGB, Spectrum
from mitsuba_wrapper.utils import Color3f

type DiffuseType = Literal["diffuse"]
type DielectricType = Literal["dielectric"]
type ConductorType = Literal["conductor"]

type BSDFType = Literal[DiffuseType, DielectricType, ConductorType]
type BSDF = Diffuse | Dielectric | Conductor


@final
class Diffuse(BaseModel, frozen=True):
    reflectance: Spectrum = Field(
        # TODO: SRGB, or RGB?
        default_factory=lambda: RGB(value=Color3f(root=(0.5, 0.5, 0.5))),
        description="Specifies the diffuse albedo of the material",
    )
    type: DiffuseType = "diffuse"


type DielectricMaterialType = Literal[
    "vacuum",
    "acetone",
    "bromine",
    "bk7",
    "helium",
    "ethanol",
    "water ice",
    "sodium chloride",
    "hydrogen",
    "carbon tetrachloride",
    "fused quartz",
    "amber",
    "air",
    "glycerol",
    "pyrex",
    "pet",
    "carbon dioxide",
    "benzene",
    "acrylic glass",
    "diamond",
    "water",
    "silicone oil",
    "polypropylene",
]


@final
class Dielectric(BaseModel, frozen=True):
    int_ior: float | DielectricMaterialType = Field(
        default="bk7",
        description="Interior index of refraction specified numerically or using a known material name",
    )
    ext_ior: float | DielectricMaterialType = Field(
        default="air",
        description="Exterior index of refraction specified numerically or using a known material name",
    )
    # TODO: Spectrum | Texture
    # TODO: SRGB, or RGB?
    specular_reflectance: Spectrum = Field(
        default_factory=lambda: RGB(value=Color3f(root=(1.0, 1.0, 1.0))),
        description="""
            Optional factor that can be used to modulate the specular reflection component. Note that for physical
            realism, this parameter should never be touched
        """,
    )
    specular_transmittance: Spectrum = Field(
        default_factory=lambda: RGB(value=Color3f(root=(1.0, 1.0, 1.0))),
        description="""
            Optional factor that can be used to modulate the specular transmission component. Note that for physical
            realism, this parameter should never be touched
        """,
    )
    type: DielectricType = "dielectric"


type ConductorIORListType = Literal[
    "a-C",
    "Na_palik",
    "Ag",
    "Nb",
    "Nb_palik",
    "Al",
    "Ni_palik",
    "AlAs",
    "AlAs_palik",
    "Rh",
    "Rh_palik",
    "AlSb",
    "AlSb_palik",
    "Se",
    "Se_palik",
    "Au",
    "SiC",
    "SiC_palik",
    "Be",
    "Be_palik",
    "SnTe",
    "SnTe_palik",
    "Cr",
    "Ta",
    "Ta_palik",
    "CsI",
    "CsI_palik",
    "Te",
    "Te_palik",
    "Cu",
    "Cu_palik",
    "ThF4",
    "ThF4_palik",
    "Cu2O",
    "Cu2O_palik",
    "TiC",
    "TiC_palik",
    "CuO",
    "CuO_palik",
    "TiN",
    "TiN_palik",
    "d-C",
    "d-C_palik",
    "TiO2",
    "TiO2_palik",
    "Hg",
    "Hg_palik",
    "VC",
    "VC_palik",
    "HgTe",
    "HgTe_palik",
    "V_palik",
    "Ir",
    "Ir_palik",
    "VN",
    "VN_palik",
    "K",
    "K_palik",
    "W",
    "Li",
    "Li_palik",
    "MgO",
    "MgO_palik",
    "Mo",
    "Mo_palik",
    "none",
]


@final
class Conductor(BaseModel, frozen=True):
    material: ConductorIORListType = Field(
        default="none",
        description="Name of the material preset, see conductor-ior-list",
    )
    # TODO: Add texture support
    eta: None | float | Spectrum = Field(
        default=None,
        description="""
            Real component of the material's index of refraction. (Default: based on the value of material)
        """,
    )
    k: None | float | Spectrum = Field(
        default=None,
        description="""
            Imaginary component of the material's index of refraction. (Default: based on the value of material)
        """,
    )
    # TODO: SRGB, or RGB?
    specular_reflectance: Spectrum = Field(
        default_factory=lambda: RGB(value=Color3f(root=(1.0, 1.0, 1.0))),
        description="""
            Optional factor that can be used to modulate the specular reflection component. Note that for physical
            realism, this parameter should never be touched
        """,
    )
    type: ConductorType = "conductor"
