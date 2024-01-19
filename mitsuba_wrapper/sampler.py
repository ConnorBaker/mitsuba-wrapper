from typing import Literal, final

from pydantic import BaseModel, Field

type IndependentType = Literal["independent"]
type OrthogonalType = Literal["orthogonal"]

type SamplerType = IndependentType | OrthogonalType
type Sampler = Independent | Orthogonal


@final
class Independent(BaseModel, frozen=True):
    sample_count: int = Field(default=4, description="Number of samples per pixel")
    seed: int = Field(default=0, description="Seed offset")
    type: IndependentType = "independent"


@final
class Orthogonal(BaseModel, frozen=True):
    sample_count: int = Field(
        default=4,
        description="Number of samples per pixel. This value has to be the square of a prime number",
    )
    strength: int = Field(default=2, description="Orthogonal array's strength")
    seed: int = Field(default=0, description="Seed offset")
    jitter: bool = Field(default=True, description="Adds additional random jitter withing the substratum")
    type: OrthogonalType = "orthogonal"
