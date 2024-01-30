from typing import Literal, final

from pydantic import BaseModel, Field

from mitsuba_wrapper.bsdf import BSDF
from mitsuba_wrapper.emitter import Emitter
from mitsuba_wrapper.ref import Ref
from mitsuba_wrapper.utils import Point3f, Transform4f

type ObjType = Literal["obj"]
type SphereType = Literal["sphere"]
type RectangleType = Literal["rectangle"]
type CubeType = Literal["cube"]
type GroupType = Literal["shapegroup"]
type InstanceType = Literal["instance"]

type ShapeType = ObjType | SphereType | RectangleType | CubeType | GroupType | InstanceType
# Need to force Shape to be lazily evaluated since it is the value type parameter of the mapping
# in ShapeGroup.
type Shape = "Obj | Sphere | Rectangle | Cube | ShapeGroup | Instance"


class ShapeLike(BaseModel, frozen=True):
    to_world: None | Transform4f = Field(
        default=None,
        description="""
            Specifies an optional linear object-to-world transformation. Note that non-uniform scales and shears are
            not permitted!
        """,
    )
    bsdf: None | BSDF | Ref = Field(default=None, description="Specifies the object's BSDF")
    emitter: None | Emitter | Ref = Field(default=None, description="Specifies the object's emitter")


class PrimitiveLike(ShapeLike, frozen=True):
    silhouette_sampling_weight: float = Field(
        default=1,
        description="Weight associated with this shape when sampling silhoeuttes in the scene",
    )


@final
class Obj(ShapeLike, frozen=True):
    filename: str = Field(description="Filename of the OBJ file that should be loaded")
    face_normals: bool = Field(
        default=False,
        description="""
            When set to true, any existing or computed vertex normals are discarded and face normals will instead be
            used during rendering. This gives the rendered object a faceted appearance
        """,
    )
    flip_tex_coords: bool = Field(
        default=True,
        description="""
            Treat the vertical component of the texture as inverted? Most OBJ files use this convention
        """,
    )
    flip_normals: bool = Field(
        default=False,
        description="Is the mesh inverted, i.e. should the normal vectors be flipped?",
    )
    type: ObjType = "obj"


@final
class Sphere(PrimitiveLike, frozen=True):
    center: Point3f = Field(
        default_factory=lambda: Point3f(root=(0, 0, 0)),
        description="Center of the sphere",
    )
    radius: float = Field(default=1, description="Radius of the sphere")
    type: SphereType = "sphere"


@final
class Rectangle(PrimitiveLike, frozen=True):
    flip_normals: bool = Field(
        default=False,
        description="Is the rectangle inverted, i.e. should the normal vectors be flipped?",
    )
    type: RectangleType = "rectangle"

@final
class Cube(PrimitiveLike, frozen=True):
    flip_normals: bool = Field(
        default=False,
        description="Is the cube inverted, i.e. should the normal vectors be flipped?",
    )
    type: CubeType = "cube"

@final
class ShapeGroup(BaseModel, extra="allow", frozen=True):
    # One or more shapes that should be made available for geometry instancing
    __pydantic_extra__: dict[str, Shape]  # type: ignore
    type: GroupType = "shapegroup"


@final
class Instance(BaseModel, frozen=True):
    to_world: None | Transform4f = Field(
        default=None,
        description="""
            Specifies an optional linear object-to-world transformation. Note that non-uniform scales and shears are
            not permitted!
        """,
    )
    shapegroup: ShapeGroup | Ref = Field(description="A reference to a shape group that should be instantiated")
    type: InstanceType = "instance"
