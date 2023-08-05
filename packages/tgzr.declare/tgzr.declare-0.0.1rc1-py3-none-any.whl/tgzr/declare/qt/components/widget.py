from qtpy import QtWidgets

from ...enums import Enums
from ...render_context import RenderContext
from ..renderer import QtRenderer
from ._qt_utils import get_qt_alignment, make_widget_property


@QtRenderer.register
def LayoutItem(context: RenderContext, params: QtRenderer.schema.LayoutItem):

    try:
        widget = context["widget"]
    except KeyError:
        raise ValueError(
            "Cannot layout an item which doesn't declare a `widget` in its context !"
        )

    try:
        layout = context["layout"]
    except KeyError:
        raise ValueError("Cannot layout item: unable to find a layout in the context !")

    # if not layout:
    #     raise Exception(f"Cannot layout widget {widget}: no current layout !!!")

    if params.separator:
        line = QtWidgets.QFrame(widget)
        horientation = context["layout_orientation"]
        if horientation == Enums.Orientation.HORIZONTAL:
            line.setFrameShape(line.VLine)
            line.setFrameShadow(line.Sunken)
        else:
            line.setFrameShape(line.HLine)
            line.setFrameShadow(line.Sunken)
        layout.addWidget(line)

    kwargs = {}
    if params.alignment is not None:
        kwargs["alignment"] = get_qt_alignment(params.alignment)
    layout.addWidget(widget, params.stretch, **kwargs)

    def get_stretch(context):
        layout = context["layout"]
        widget = context["widget"]
        index = layout.indexOf(widget)
        return layout.stretch(index)

    def set_stretch(context, value):
        layout = context["layout"]
        widget = context["widget"]
        index = layout.indexOf(widget)
        return layout.setStretch(index, value)

    context.register_property("stretch", get_stretch, set_stretch)

    def get_alignment(context):
        layout = context["layout"]
        widget = context["widget"]
        index = layout.indexOf(widget)
        layout_item = layout.itemAt(index)
        return layout_item.alignment()

    def set_alignment(context, value):
        if value is None:
            return
        layout = context["layout"]
        widget = context["widget"]
        alignment = get_qt_alignment(value)
        layout.setAlignment(widget, alignment)

    context.register_property("alignment", get_alignment, set_alignment)

    context.render_children(params.children)


@QtRenderer.register
def Widget(context: RenderContext, params: QtRenderer.schema.Widget):

    parent = context["widget"]
    widget = getattr(QtWidgets, params.widget_class)(parent)

    # widget.setStyleSheet("*{border: 1px solid red; background-color: #880000;}")

    # We need to update this context (not only the render_children
    # context) so that parent renderer can retrieve the widget:
    context["widget"] = widget

    make_widget_property("visible", bool, context)
    make_widget_property("enabled", bool, context)

    # /!\ This needs to be executed AFTER creating the properties /!\
    with params.layout as lo:
        QtRenderer.schema.set_or_bind(context, "visible", params.visible, True)
        QtRenderer.schema.set_or_bind(context, "enabled", params.enabled, True)

    # Render the LayoutItem, it will place us in current layout
    # + configure our `visible` and `enabled` properties
    context.render(lo)

    # Render child component, with us as the parent for new layouts:
    context.render_children(params.children, layout_parent=widget)
