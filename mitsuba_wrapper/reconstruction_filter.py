from typing import Literal, final

from pydantic import BaseModel, Field

type BoxType = Literal["box"]
type CatmullRomType = Literal["catmullrom"]
type GaussianType = Literal["gaussian"]
type TentType = Literal["tent"]

type ReconstructionFilterType = BoxType | CatmullRomType | GaussianType | TentType
type ReconstructionFilter = BoxFilter | CatmullRomFilter | GaussianFilter | TentFilter


@final
class BoxFilter(BaseModel, frozen=True):
    type: BoxType = "box"


@final
class TentFilter(BaseModel, frozen=True):
    radius: float = Field(default=1.0, description="Specifies the radius of the tent function")
    type: TentType = "tent"


@final
class CatmullRomFilter(BaseModel, frozen=True):
    type: CatmullRomType = "catmullrom"


@final
class GaussianFilter(BaseModel, frozen=True):
    stddev: float = Field(default=0.5, description="Specifies the standard deviation")
    type: GaussianType = "gaussian"
