from typing import Literal, final

from pydantic import BaseModel, Field

from mitsuba_wrapper.reconstruction_filter import GaussianFilter, ReconstructionFilter

type FileFormatType = Literal["openexr", "rgbe", "pfm"]
type PixelFormatType = Literal["luminance", "luminance_alpha", "rgb", "rgba", "xyz", "xyza"]
type ComponentFormatType = Literal["float16", "float32", "uint32"]

type HDRFilmType = Literal["hdrfilm"]

# Having a type declared this way is not supported by pydantic; causes model errors.
# type FilmType = HDRFilmType
# type Film = HDRFilm


@final
class HDRFilm(BaseModel, frozen=True):
    width: int = Field(default=768, description="Width of the film in pixels")
    height: int = Field(default=576, description="Height of the film in pixels")
    file_format: FileFormatType = Field(
        default="openexr",
        description="""
            Denotes the desired output file format. The options are openexr (for ILM's OpenEXR format), rgbe (for Greg
            Ward's RGBE format), or pfm (for the Portable Float Map format)
        """,
    )
    pixel_format: PixelFormatType = Field(
        default="rgb",
        description="""
            Specifies the desired pixel format of output images. The options are luminance, luminance_alpha, rgb, rgba,
            xyz and xyza
        """,
    )
    component_format: ComponentFormatType = Field(
        default="float16",
        description="""
            Specifies the desired floating point component format of output images (when saving to disk). The options
            are float16, float32, or uint32
        """,
    )
    sample_border: bool = Field(
        default=False,
        description="""
            If set to true, regions slightly outside of the film plane will also be sampled. This may improve the image
            quality at the edges, especially when using very large reconstruction filters. In general, this is not
            needed though
        """,
    )
    compensate: bool = Field(
        default=False,
        description="""
            If set to true, sample accumulation will be performed using Kahan-style error-compensated accumulation.
            This can be useful to avoid roundoff error when accumulating very many samples to compute reference
            solutions using single precision variants of Mitsuba. This feature is currently only supported in JIT
            variants and can make sample accumulation quite a bit more expensive
        """,
    )
    rfilter: ReconstructionFilter = Field(
        default_factory=GaussianFilter,
        description="Reconstruction filter that should be used by the film",
    )
    type: HDRFilmType = "hdrfilm"
