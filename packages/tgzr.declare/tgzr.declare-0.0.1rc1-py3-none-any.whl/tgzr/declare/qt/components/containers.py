import traceback
import json

from qtpy import QtWidgets, QtGui, QtCore
import qtawesome

from ...serialization import JSON
from ...render_context import RenderContext
from ...enums import Enums
from ..renderer import QtRenderer
from ._qt_utils import make_widget_property, get_qt_horientation


@QtRenderer.register
def Layout(context: RenderContext, params: QtRenderer.schema.Layout):

    layout_parent = context.get("layout_parent")
    layout = context.get("layout")

    if layout_parent is None and layout is None:
        context.pprint()
        raise Exception("Cannot create layout: no layout or widget to add it to !")

    DEBUG = params.debug

    def set_debug(context, b):
        # If there is a layout_parent, we need to use it:
        widget = layout_parent or context["widget"]
        DEBUG = b
        if DEBUG:
            widget.setStyleSheet("*{border: 1px solid red;}")
        else:
            widget.setStyleSheet("")

    def get_debug(context):
        return DEBUG

    context.register_property("debug", get_debug, set_debug)
    set_debug(context, params.debug)

    new_layout = getattr(QtWidgets, params.layout_class)()
    if layout_parent is not None:
        # a new widget has been created, we must use it:
        layout_parent.setLayout(new_layout)
    else:
        layout.addLayout(new_layout, params.stretch)

    if params.margins is not None:
        new_layout.setContentsMargins(
            params.margins, params.margins, params.margins, params.margins
        )
        new_layout.setSpacing(params.margins)

    # This will be used to place separator in the right direction:
    context["layout_orientation"] = params.orientation

    # Render our children in a new context, with removed layout_parent
    context["layout"] = new_layout
    context["layout_parent"] = None
    context.render_children(
        params.children,
        # **context_properties,
    )


@QtRenderer.register
def VBox(context: RenderContext, params: QtRenderer.schema.VBox):

    lo = QtRenderer.schema.cast_model(params, Layout)
    lo.layout_class = "QVBoxLayout"
    context.render(lo)


@QtRenderer.register
def HBox(context: RenderContext, params: QtRenderer.schema.HBox):

    with QtRenderer.schema.cast_model(params, Layout) as lo:
        lo.layout_class = "QHBoxLayout"
    context.render(lo)


@QtRenderer.register
def Stretch(context, params: QtRenderer.schema.Stretch):
    if context.get("layout_parent") is not None:
        # This means a widget has been created
        # between the layout and us !
        raise Exception("Cannot add a stretch, add a layout first !")

    layout = context["layout"]
    if layout is None:
        raise ValueError("Cannot add stretch, add a layout first !")
    layout.addStretch()


@QtRenderer.register
def Frame(context: RenderContext, params: QtRenderer.schema.Frame):
    widget_class = "QFrame"
    if (
        params.title,
        params.checkable,
        params.checked,
        params.flat,
    ) != (None, None, None, None):
        widget_class = "QGroupBox"
        make_widget_property("title", str, context)
        make_widget_property("checkable", bool, context)
        make_widget_property("checked", bool, context)
        make_widget_property("flat", bool, context)

    set_or_bind = QtRenderer.schema.set_or_bind
    with params.widget as w:
        w.widget_class = widget_class
        if widget_class == "QGroupBox":
            set_or_bind(context, "title", params.title, params.ID or "Frame")
            set_or_bind(context, "checkable", params.checkable, False)
            set_or_bind(context, "checked", params.checked, False)
            set_or_bind(context, "flat", params.flat, False)

        w.children += params.children

    context.render(w)


@QtRenderer.register
def Include(context, params: QtRenderer.schema.Include):
    if params.source_state is None:
        raise Exception("Cannot Include without a `source_state` !")

    def clear():
        include_context = context.get("include_context")
        if include_context is None:
            # nothing built yet, nothing to clear...
            return

        # If there is a widget in the context,
        # delete it:
        widget = include_context.get("widget_to_clear")
        if widget is not None:
            # FIXME: We need to remove all state bindings or the
            # state store will try to reach this widget after
            # deletion !
            # widget.setParent(None)
            # widget.show()
            widget.deleteLater()

    def build_error(ctx, err, trace, ui):
        with QtRenderer.schema.Frame() as frame:
            with QtRenderer.schema.VBox():
                QtRenderer.schema.Label(
                    text=f"<H2><font color=#880000>Error building incude: {err}</font></h2>"
                )
                QtRenderer.schema.Label(text=f"<pre>{trace}</pre>", wordWrap=True)
                QtRenderer.schema.H3(text="ui was:")
                QtRenderer.schema.Label(text=f"<pre>{ui.pformat()}</pre>")
                QtRenderer.schema.H3(text="states were:")
                states = context.get_states()
                QtRenderer.schema.Label(
                    text=f"<pre>{json.dumps(states, indent=2, cls=JSON.Encoder)}</pre>"
                )
                # QtRenderer.schema.PrintContextButton(
                #     label="[Print Include Context]", alt_context=ctx
                # )
                QtRenderer.schema.Stretch()
        context.render(frame)

    def build():
        source_state = QtRenderer.schema._namespaces.get_state_key(
            context, params.source_state
        )
        ui_dict = context.get_state(source_state)

        # TODO: turn the dict into UI
        ui = context["renderer"].ui_from_dict(ui_dict)

        # import devtools

        # print("============= DICT")
        # devtools.debug(ui_dict)
        # print("============= UI")
        # devtools.debug(ui)
        # print("============= <<")

        with QtRenderer.schema.Widget(widget_class="QWidget") as include_widget:
            with QtRenderer.schema.HBox() as box:
                # TODO: FIXME: WARNING: this works only if we set children
                # inside the Hbox context, but on using constructor parameter !
                # IDFKW :/ but this is going to bite. Hard :[
                box.children = [ui]

        with context(include_source_state=source_state) as include_context:
            context["include_context"] = include_context
            try:
                sub_context = include_context.render(include_widget)
            except Exception as err:
                raise
                trace = traceback.format_exc()
                build_error(include_context, err, trace, include_widget)
            else:
                widget = sub_context["widget"]
                include_context["widget_to_clear"] = widget

    def on_trigger(value):
        clear()
        build()

    if params.trigger_state is not None:
        trigger_state = QtRenderer.schema._namespaces.get_state_key(
            context, params.trigger_state
        )
        context.bind_state(trigger_state, on_trigger)


@QtRenderer.register
def Tabs(context: RenderContext, params: QtRenderer.schema.Tabs):

    make_widget_property("current", int, context, qproperty_name="currentIndex")
    make_widget_property("movable", bool, context)
    make_widget_property("closable", bool, context, qproperty_name="tabsClosable")

    Set = QtRenderer.schema.Set
    with params.widget as w:
        w.widget_class = "QTabWidget"
        Set(name="current", value=params.current)
        Set(name="movable", value=params.movable)
        Set(name="closable", value=params.closable)

    sub_context = context.render(w)
    tabs = sub_context["widget"]

    def on_tab_close(index):
        w = tabs.widget(index)
        w.deleteLater()

    tabs.tabCloseRequested.connect(on_tab_close)

    # store in context for sub-component access:
    # (note that we didnt give our children to the widget sub-component...)
    with context(tabs_widget=tabs, layout_parent=tabs) as ctx:
        ctx.render_children(params.children)


@QtRenderer.register
def Tab(context: RenderContext, params: QtRenderer.schema.Tab):
    try:
        tabs = context["tabs_widget"]
    except KeyError:
        raise Exception(
            f"Unable to create Tab component {params.ID}: not Tabs found in parents."
        )

    #
    #   BUILD OUR PROPERTIES
    #
    def get_title(context):
        tabs = context["tabs_widget"]
        widget = context["widget"]
        index = tabs.indexOf(widget)
        return tabs.tabText(index)

    def set_title(context, title):
        tabs = context["tabs_widget"]
        widget = context["widget"]
        index = tabs.indexOf(widget)
        tabs.setTabText(index, title)

    context.register_property("title", get_title, set_title)

    def get_icon(context):
        tabs = context["tabs_widget"]
        widget = context["widget"]
        index = tabs.indexOf(widget)
        icon = tabs.tabIcon(index)
        return icon._source_name

    def set_icon(context, icon_name):
        tabs = context["tabs_widget"]
        widget = context["widget"]
        index = tabs.indexOf(widget)
        if icon_name is None:
            icon = QtGui.QIcon()
        else:
            icon = qtawesome.icon(icon_name)
        icon._source_name = icon_name
        tabs.setTabIcon(index, icon)

    context.register_property("icon", get_icon, set_icon)

    def get_tooltip(context):
        tabs = context["tabs_widget"]
        widget = context["widget"]
        index = tabs.indexOf(widget)
        return tabs.tabToolTip(index)

    def set_tooltip(context, tooltip):
        tabs = context["tabs_widget"]
        widget = context["widget"]
        index = tabs.indexOf(widget)
        tabs.setTabToolTip(index, tooltip)

    context.register_property("tooltip", get_tooltip, set_tooltip)

    #
    #   BUILD AND RENDER SUB-COMPONENTS
    #

    # NOTE:
    # This is tricky: the property getter/setter need to find the index
    # of our widget in the tab so they wont work until the widget is
    # added to the tabs.
    # So we need several distinct render steps:
    #   - render the widget and add it to the tabs
    #   - set or bind the properties
    #   - render our children components

    with params.widget as w:
        w.widget_class = "QWidget"

    # Render the widget
    widget_context = context.render(w)
    widget = widget_context["widget"]
    # store the widget, it will be used by properties:
    context["widget"] = widget

    # Add the created widget to the tabs widget before appying properties
    tabs.addTab(widget, params.title or params.ID or params.TYPE)

    # Bind the properties or apply the provided value
    #
    # we need a context to gather the `Set` and `Bind`` components
    # produced by `set_of_bind()`, we use the Group for this:
    with QtRenderer.schema.Group() as group:
        QtRenderer.schema.set_or_bind(
            context,
            "title",
            params.title,
            params.ID or "Tab",
        )
        QtRenderer.schema.set_or_bind(
            context,
            "icon",
            params.icon,
            None,
        )
        QtRenderer.schema.set_or_bind(
            context,
            "tooltip",
            params.widget.tooltip,
            None,
        )
    context.render(group)

    # no render our automated layout, giving it our children:
    with QtRenderer.schema.Group() as content:
        if params.layout_orientation is Enums.Orientation.VERTICAL:
            layout_type = QtRenderer.schema.VBox
        else:
            layout_type = QtRenderer.schema.HBox
        with layout_type() as b:
            b.children += params.children
            if params.layout_stretch:
                QtRenderer.schema.Stretch()

    with context(layout_parent=widget) as content_layout:
        content_layout.render(content)


@QtRenderer.register
def Splitter(context: RenderContext, params: QtRenderer.schema.Splitter):
    make_widget_property("orientation", get_qt_horientation, context)

    with params.widget as w:
        w.widget_class = "QSplitter"
        QtRenderer.schema.set_or_bind(
            context,
            "orientation",
            params.orientation,
            default=Enums.Orientation.HORIZONTAL,
        )
    splitter = context.render(w)["widget"]

    with context(
        widget=splitter,
        splitter_widget=splitter,
        layout_parent=splitter,
    ) as ctx:
        ctx.render_children(params.children)


@QtRenderer.register
def SplitterPanel(context: RenderContext, params=QtRenderer.schema.SplitterPanel):
    try:
        splitter = context["splitter_widget"]
    except KeyError:
        raise ValueError(
            "Error creating SplitterPanle {params.ID}: No splitter found in ancestors."
        )

    with params.widget as w:
        w.widget_class = "QWidget"

    # Render the widget
    widget = context.render(w)["widget"]
    # store the widget, it will be used by properties:
    context["widget"] = widget
    splitter.addWidget(widget)

    with QtRenderer.schema.Group() as content:
        if params.layout_orientation == Enums.Orientation.VERTICAL:
            layout_type = QtRenderer.schema.VBox
        else:
            layout_type = QtRenderer.schema.HBox
        with layout_type() as b:
            b.children += params.children
            if params.layout_stretch:
                QtRenderer.schema.Stretch()

    with context(layout_parent=widget) as content_layout:
        content_layout.render(content)


class OverlayWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        parent.installEventFilter(self)
        # self.setStyleSheet("QWidget {border: 3px solid red;}")
        self.setStyleSheet("*{border: 1px solid red;}")

    def eventFilter(self, watched, event):
        if event.type() == QtCore.QEvent.ChildAdded:
            self.raise_()
        elif event.type() == QtCore.QEvent.Resize:
            self.update_geometry(watched.geometry())
        return super().eventFilter(watched, event)

    def update_geometry(self, geometry):
        self.setGeometry(geometry)


@QtRenderer.register
def Overlay(context: RenderContext, params=QtRenderer.schema.Overlay):

    parent = context["widget"]
    overlay_widget = OverlayWidget(parent)
    context["widget"] = overlay_widget

    make_widget_property("visible", bool, context)
    make_widget_property("enabled", bool, context)

    # /!\ This needs to be renderer AFTER creating the properties /!\
    with QtRenderer.schema.Group() as properties_setup:
        QtRenderer.schema.set_or_bind(context, "visible", params.visible, True)
        QtRenderer.schema.set_or_bind(context, "enabled", params.enabled, True)
    context.render(properties_setup)

    # Render child component, with us as the parent for new layouts:
    context.render_children(params.children, layout_parent=overlay_widget)


@QtRenderer.register
def Anchors(context: RenderContext, params=QtRenderer.schema.Anchors):

    anchor_collections = context.get("anchor_collections", None)
    if anchor_collections is None:
        anchor_collections = dict()
        context["anchor_collections"] = anchor_collections

    name = params.name or params.ID

    # Don't reset existing collection, this is a feature:
    if name not in anchor_collections:
        anchor_collections[name] = dict()

    context["current_anchor_collection"] = anchor_collections[name]

    context.render_children(params.children)


@QtRenderer.register
def Anchor(context: RenderContext, params=QtRenderer.schema.Anchor):
    name = params.name or params.ID
    if name is None:
        raise ValueError("Cannot create Anchor without name nor ID.")

    # store anchor config in the context:
    trigger_state = params.trigger_state or params.ID
    trigger_state = QtRenderer.schema._namespaces.get_state_key(context, trigger_state)
    context["trigger_state"] = trigger_state
    context["anchor_effect"] = params.effect

    # store the context in the current anchor collection, under its name (no namespace here!):
    anchor_collection = context["current_anchor_collection"]
    anchor_collection[name] = context

    def jiggle(widget, duration=300):
        anim = QtCore.QPropertyAnimation(widget, b"pos")
        anim.setDuration(duration)
        anim.setEasingCurve(QtCore.QEasingCurve.OutElastic)
        anim.setStartValue(widget.pos() + QtCore.QPoint(20, 0))
        anim.setEndValue(widget.pos())
        anim.setLoopCount(1)
        widget._anchor_fx = anim
        widget.raise_()
        anim.start()

    def bubble(widget, duration=300):
        anims = QtCore.QParallelAnimationGroup()

        anim = QtCore.QPropertyAnimation(widget, b"pos")
        anim.setDuration(duration)
        anim.setEasingCurve(QtCore.QEasingCurve.InCubic)
        anim.setStartValue(widget.pos() + QtCore.QPoint(-10, -10))
        anim.setEndValue(widget.pos())
        anims.addAnimation(anim)

        anim = QtCore.QPropertyAnimation(widget, b"size")
        anim.setDuration(duration)
        anim.setEasingCurve(QtCore.QEasingCurve.InCubic)
        anim.setStartValue(widget.size() + QtCore.QSize(20, 20))
        anim.setEndValue(widget.size())
        anims.addAnimation(anim)

        widget._anchor_fx = anims
        widget.raise_()
        anims.start()

    def trigger(effect=None, *args, **kwargs):
        effect = effect or params.effect
        if effect is None:
            return
        if effect == "Jiggle":
            fx = jiggle
        elif effect == "Bubble":
            fx = bubble
        else:
            print("????", effect)
            return
        duration = 300
        offset = 50
        widgets = context.get("anchor_widgets", [])
        for widget in widgets:
            # widget.setStyleSheet("*{border: 1px solid red;}")
            fx(widget, duration)
            duration += offset

    context.bind_state(trigger_state, trigger)

    # we dont use context.render_children() here because we need to keep
    # track of created widgets, but apart from that we do the same:
    anchor_widgets = []
    with context(INFO="anchor_children_context") as ctx:
        for child in params.children:
            print(child.TYPE)
            child_context = ctx.render(child)
            try:
                child_widget = child_context["widget"]
            except KeyError:
                pass
            else:
                if child_widget is not None:
                    anchor_widgets.append(child_widget)
    context["anchor_widgets"] = anchor_widgets
