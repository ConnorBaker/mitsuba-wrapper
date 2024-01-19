from typing import Literal, final

from pydantic import BaseModel, Field

type PathType = Literal["path"]
type VolPathType = Literal["volpath"]
type VolPathMisType = Literal["volpathmis"]

type IntegratorType = PathType | VolPathType | VolPathMisType
type Integrator = Path | VolPath | VolPathMis


class PathBasedIntegrator(BaseModel, frozen=True):
    type: IntegratorType
    max_depth: int = Field(
        default=-1,
        description="""
            Specifies the longest path depth in the generated output image (where -1 corresponds to infinity). A value
            of 1 will only render directly visible light sources. 2 will lead to single-bounce (direct-only)
            illumination, and so on
        """,
    )
    rr_depth: int = Field(
        default=5,
        description="""
            Specifies the path depth, at which the implementation will begin to use the russian roulette path
            termination criterion. For example, if set to 1, then path generation many randomly cease after
            encountering directly visible surfaces
        """,
    )
    hide_emitters: bool = Field(default=False, description="Hide directly visible emitters")


@final
class Path(PathBasedIntegrator, frozen=True):
    type: PathType = "path"


@final
class VolPath(PathBasedIntegrator, frozen=True):
    type: VolPathType = "volpath"


@final
class VolPathMis(PathBasedIntegrator, frozen=True):
    type: VolPathMisType = "volpathmis"
