from typing import Literal, NewType, final

from pydantic import BaseModel

ID = NewType("ID", str)

type RefType = Literal["ref"]


@final
class Ref(BaseModel, frozen=True):
    id: ID
    type: RefType = "ref"
