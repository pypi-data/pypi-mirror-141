from typing import Union, List

from ..enums import Enums
from ._base import PropertyModel


class Binded(PropertyModel):
    """
    Use this as the Value of a property (a bindable param)
    to bind it to a state value.
    """

    state_key: str = None


BindableBool = Union[bool, str, Binded]
BindableInt = Union[int, str, Binded]
BindableFloat = Union[float, str, Binded]
BindableString = Union[str, str, Binded]
BindableList = Union[List, str, Binded]

BindableAlignment = Union[Enums.Alignment, str, Binded]
BindableOrientation = Union[Enums.Orientation, str, Binded]
