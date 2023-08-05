from qtpy import QtCore

from ...enums import Enums


def make_qobject_property(
    name, converter, context, qobject_getter, qproperty_name=None
):
    """
    qobject_getter must be callable(context) and return the qobject
    where we will find the property getter and setter.

    For the rest, see make_widget_property docstring...
    """

    qproperty_name = qproperty_name or name

    def widget_getter(context):
        return getattr(qobject_getter(context), qproperty_name)()

    def widget_setter(context, value):
        if converter is not None:
            value = converter(value)
        setter_name = "set" + qproperty_name[0].title() + qproperty_name[1:]
        getattr(qobject_getter(context), setter_name)(value)

    context.register_property(name, widget_getter, widget_setter)
    return widget_getter, widget_setter


def make_widget_property(name, converter, context, qproperty_name=None):
    """
    Creates and register property setter and getter for
    the given name, following Qt property naming convention.

    This needs a 'widget' in the context (at the moment of
    getting or setting the property), and this widget must
    have methods like `{name}()` and `set{Name}(value)`.

    If converter is not None, the setter will called it
    with the value a sole argument and the result will be
    used instead of the value.
    """

    def widget_getter(context):
        return context["widget"]

    return make_qobject_property(
        name, converter, context, widget_getter, qproperty_name=qproperty_name
    )


class UnknwonOrientation(ValueError):
    def __init__(self, value, choices):
        super().__init__(
            f"Unknown value {value!r} for orientation. Should be one of {list(choices)}"
        )


def get_qt_horientation(value):
    if 0:
        # old
        qt_horientation = dict(
            Horizontal=QtCore.Qt.Horizontal,
            Vertical=QtCore.Qt.Vertical,
        )
    else:
        qt_horientation = {
            Enums.Orientation.HORIZONTAL: QtCore.Qt.Horizontal,
            Enums.Orientation.VERTICAL: QtCore.Qt.Vertical,
        }

    try:
        return qt_horientation[value]
    except KeyError:
        raise UnknwonOrientation(value, qt_horientation.keys())


class UnknwonAlignment(ValueError):
    def __init__(self, value, choices):
        super().__init__(
            f"Unknown value {value!r} for orientation. Should be one of {list(choices)}"
        )


def get_qt_alignment(value):
    qt_aligments = {
        Enums.Alignment.LEFT: QtCore.Qt.AlignLeft,
        Enums.Alignment.RIGHT: QtCore.Qt.AlignRight,
        Enums.Alignment.HCENTER: QtCore.Qt.AlignHCenter,
        Enums.Alignment.TOP: QtCore.Qt.AlignTop,
        Enums.Alignment.BOTTOM: QtCore.Qt.AlignBottom,
        Enums.Alignment.VCENTER: QtCore.Qt.AlignVCenter,
    }
    ored_flags = [flag for flag in Enums.Alignment if flag in value]
    alignment = 0
    for flag in ored_flags:
        try:
            alignment |= qt_aligments[flag]
        except KeyError:
            # print(f'Unknow layout_item alignment flag: "{flag}" in value "{value}"')
            raise UnknwonAlignment(flag, qt_aligments.keys())
            pass

    return alignment
