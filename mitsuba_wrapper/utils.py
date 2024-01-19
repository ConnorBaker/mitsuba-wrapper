from collections.abc import Callable, Iterable, Sequence
from typing import Self, cast, final

import mitsuba as mi
from pydantic import BaseModel, Field, RootModel, SerializationInfo
from pydantic.functional_serializers import model_serializer

_ScalarColor3f: Callable[[list[float]], mi.Color3f] = getattr(mi, "ScalarColor3f")
_ScalarPoint3f: Callable[[list[float]], mi.Point3f] = getattr(mi, "ScalarPoint3f")
_ScalarVector3f: Callable[[list[float]], mi.Vector3f] = getattr(mi, "ScalarVector3f")
_ScalarVector4f: Callable[[list[float]], mi.Vector4f] = getattr(mi, "ScalarVector4f")
_ScalarVector4fTy: type = getattr(mi, "ScalarVector4f")
_ScalarTransform4f: Callable[[list[mi.Vector4f]], mi.Transform4f] = getattr(mi, "ScalarTransform4f")


# NOTE: If we add a return type to the model serializer, Pydantic will error because it cannot generate a schema for
# the mitsuba types.


def _serializer_helper[A, B](
    xs: Sequence[A],
    fn: Callable[[list[A]], B],
    mode: str,
) -> list[A] | B:
    as_list = list(xs)
    match mode:
        case "python":
            return fn(as_list)
        case "json":
            return as_list
        case _:
            raise ValueError(f"Unsupported serialization mode: {mode}")


@final
class Color3f(RootModel[tuple[float, float, float]]):
    root: tuple[float, float, float] = Field(description="A color in 3D space")

    @model_serializer
    def root_serializer(self: Self, info: SerializationInfo):
        return _serializer_helper(self.root, _ScalarColor3f, info.mode)


@final
class Point3f(RootModel[tuple[float, float, float]]):
    root: tuple[float, float, float] = Field(description="A point in 3D space")

    @model_serializer
    def root_serializer(self: Self, info: SerializationInfo):
        return _serializer_helper(self.root, _ScalarPoint3f, info.mode)


@final
class Vector3f(RootModel[tuple[float, float, float]]):
    root: tuple[float, float, float] = Field(description="A vector in 3D space")

    @model_serializer
    def root_serializer(self: Self, info: SerializationInfo):
        return _serializer_helper(self.root, _ScalarVector3f, info.mode)


@final
class Vector4f(RootModel[tuple[float, float, float, float]]):
    root: tuple[float, float, float, float] = Field(description="A vector in 4D space")

    @model_serializer
    def root_serializer(self: Self, info: SerializationInfo):
        return _serializer_helper(self.root, _ScalarVector4f, info.mode)


@final
class Transform4f(RootModel[tuple[Vector4f, Vector4f, Vector4f, Vector4f]]):
    root: tuple[Vector4f, Vector4f, Vector4f, Vector4f] = Field(description="A matrix in 4D space")

    @model_serializer
    def root_serializer(self: Self, info: SerializationInfo):
        component_dumps = [v.model_dump(**info.__dict__) for v in self.root]
        match info.mode:
            case "python":
                assert all(isinstance(v, _ScalarVector4fTy) for v in component_dumps)
                return _ScalarTransform4f(cast(list[mi.Vector4f], component_dumps))
            case "json":
                return component_dumps
            case _:
                raise ValueError(f"Unsupported serialization mode: {info.mode}")

    @classmethod
    def to_transform4f(cls: type[Self], m: Iterable[Iterable[float]]) -> Self:
        # NOTE: SUPER MEGA IMPORTANT
        # Arrays are stored in row-major order, i.e. the first index is the row, the second index is the column.
        # HOWEVER, these matrices are stored in column-major order, i.e. the first index is the column, the second
        # index is the row. This is because the matrices are stored as column vectors, and the first index is the
        # index of the vector.
        # def to_vector4f(v: Iterable[float]) -> Vector4f:
        #     (x, y, z, w) = v
        #     return Vector4f(root=(x, y, z, w))

        return cls(
            root=tuple(  # type: ignore
                map(
                    # Convert each vector to a Vector4f.
                    Vector4f.model_validate,
                    # Transpose the matrix so that it is in row-major order.
                    zip(*m),
                )
            )
        )

    # Recall that the transformations compose right-to-left!
    @classmethod
    def scale_rotate_translate(
        cls: type[Self],
        scale: tuple[float, float, float] | Vector3f = (1.0, 1.0, 1.0),
        rotate_axis: tuple[float, float, float] | Point3f = (0.0, 0.0, 0.0),
        rotate_degrees: float = 0.0,
        translate: tuple[float, float, float] | Vector3f = (0.0, 0.0, 0.0),
    ) -> Self:
        """
        Returns the matrix representing the composition of the given transformations.

        The transformations are applied in the order: scale, rotate, translate.

        The defaults for each transformation are their identities.
        """
        if isinstance(scale, Vector3f):
            scale = scale.root
        if isinstance(rotate_axis, Point3f):
            rotate_axis = rotate_axis.root
        if isinstance(translate, Vector3f):
            translate = translate.root

        return cls.to_transform4f(
            mi.ScalarTransform4f.translate(translate)  # type: ignore
            .rotate(rotate_axis, rotate_degrees)
            .scale(scale)
            .matrix
        )

    @classmethod
    def look_at(
        cls: type[Self],
        origin: tuple[float, float, float] | Point3f,
        target: tuple[float, float, float] | Point3f,
        up: tuple[float, float, float] | Point3f,
    ) -> Self:
        """
        Returns the matrix representing the composition of the given transformations.
        """
        if isinstance(origin, Point3f):
            origin = origin.root
        if isinstance(target, Point3f):
            target = target.root
        if isinstance(up, Point3f):
            up = up.root
        return cls.to_transform4f(
            mi.ScalarTransform4f.look_at(  # type: ignore
                origin=origin,
                target=target,
                up=up,
            ).matrix
        )


class Placeable(BaseModel, frozen=True):
    to_world: None | Transform4f = Field(
        default=None,
        description="""
            Specifies an optional camera-to-world transformation. (Default: none, i.e. object space = world space)
        """,
    )
