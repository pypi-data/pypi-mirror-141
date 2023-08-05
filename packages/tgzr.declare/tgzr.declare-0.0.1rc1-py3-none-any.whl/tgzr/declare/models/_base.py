from __future__ import annotations

from typing import Any, List
import pprint

import pydantic

from ..enums import Enums, _EnumMixin


#
#   TOOLS
#


class _ParentStack(object):
    STACK: List["ComponentModel"] = []

    @classmethod
    def push(cls, parent):
        cls.STACK += [parent]
        # indent = len(cls.STACK) * "    "
        # print(indent, ">", parent.__class__.__name__, parent.ID)

    @classmethod
    def pop(cls):
        # indent = len(cls.STACK) * "    "
        parent = cls.STACK.pop()  # noqa F841
        # print(indent, "<", parent.__class__.__name__, parent.ID)

    @classmethod
    def current(cls):
        return cls.STACK and cls.STACK[-1] or None


#
#   MODELS
#


class Collection(pydantic.BaseModel):
    pass


class ParamsModel(Collection):
    class Config:
        use_enum_values = False
        json_encoders = {_EnumMixin: lambda v: v.__json__()}
        # TODO: see if we would want this:
        # validate_assignment = True

    TYPE: str = None

    @classmethod
    def like(cls, other):
        return cls(**other.dict())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TYPE = self.__class__.__name__

    def pformat(self):
        return pprint.pformat(self.dict(), indent=True)

    def pprint(self):
        print(self.pformat())


class PropertyModel(ParamsModel):
    pass


class RootModel(ParamsModel):

    children: List["ComponentModel"] = []


class ComponentModel(RootModel):

    ID: Any = None

    def __init__(self, *args, **kwargs):
        if args:
            kwargs["ID"] = args[0]
            args = args[1:]
        super().__init__(*args, **kwargs)

        parent = _ParentStack.current()
        if parent is not None:
            parent.children.append(self)

    def __enter__(self):
        _ParentStack.push(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        _ParentStack.pop()
