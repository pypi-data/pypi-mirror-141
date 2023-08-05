import warnings

from qtpy import QtGui
import qtawesome

from ..renderer import Renderer
from .schema import QtSchema


class QtRenderer(Renderer):

    schema = QtSchema

    _NO_ICON = None

    @classmethod
    def _get_no_icon(cls):
        if cls._NO_ICON is None:
            cls._NO_ICON = QtGui.QIcon()
        return cls._NO_ICON

    @classmethod
    def value_to_icon(cls, value):
        """
        Helper to convert a value to an icon.
        """
        if value is None:
            return cls._get_no_icon()
        try:
            return qtawesome.icon(value)
        except Exception as err:
            warnings.warn(err)
            return cls._get_no_icon()
