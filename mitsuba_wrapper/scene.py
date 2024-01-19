from typing import Literal, final

from pydantic import BaseModel

from mitsuba_wrapper.bsdf import BSDF
from mitsuba_wrapper.integrator import Integrator
from mitsuba_wrapper.sensor import Sensor
from mitsuba_wrapper.shape import Shape

type SceneType = Literal["scene"]


@final
class Scene(BaseModel, extra="allow", frozen=True):
    __pydantic_extra__: dict[str, BSDF | Shape]  # pyright: ignore[reportIncompatibleVariableOverride]

    integrator: Integrator
    sensor: Sensor
    type: SceneType = "scene"
