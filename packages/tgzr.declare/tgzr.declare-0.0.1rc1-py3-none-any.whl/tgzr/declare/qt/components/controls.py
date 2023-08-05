from qtpy import QtWidgets, QtGui, QtCore
import qtawesome

from ...render_context import RenderContext
from ..renderer import QtRenderer, QtSchema
from ._qt_utils import make_widget_property, make_qobject_property


@QtRenderer.register
def Button(context: RenderContext, params: QtRenderer.schema.Button):

    # print("--------BUTTON", params.label, params.ID)
    # context.pprint()

    make_widget_property("label", str, context, qproperty_name="text")
    make_widget_property(
        "icon", QtRenderer.value_to_icon, context, qproperty_name="icon"
    )

    with params.widget as w:
        w.widget_class = "QPushButton"
        QtRenderer.schema.set_or_bind(context, "label", params.label, params.ID)
        QtRenderer.schema.set_or_bind(context, "icon", params.icon, None)
        # Append our children to the configured widget:
        w.children += params.children

    sub_context = context.render(w)
    button = sub_context["widget"]

    # this is needed by parent component who want to affect us.
    context["widget"] = button

    #
    # Trigger clicked action, and update action_state if requested:
    #
    # support Group namespaces:
    clicked = QtRenderer.schema._namespaces.get_action_name(context, "clicked")
    clicked_action_trigger = context.get_handler(
        params.action_key or params.ID, clicked
    )
    button.clicked.connect(clicked_action_trigger)


@QtRenderer.register
def Toggle(context: RenderContext, params: QtRenderer.schema.Toggle):

    make_widget_property("label", str, context, qproperty_name="text")
    make_widget_property("value", bool, context, qproperty_name="checked")

    with params.widget as w:
        w.widget_class = "QCheckBox"
        QtRenderer.schema.set_or_bind(context, "label", params.label, params.ID or "")
        value_state = QtRenderer.schema.set_or_bind(
            context, "value", params.value, False
        )
        # Append our children to the configured widget:
        w.children += params.children

    sub_context = context.render(w)
    cb = sub_context["widget"]

    # this is needed by parent component who want to affect us.
    context["widget"] = cb

    #
    # Trigger toggled action, and update action_state if requested:
    #
    toggled = QtRenderer.schema._namespaces.get_action_name(context, "toggled")
    toggled_action_trigger = context.get_handler(
        params.action_key or params.ID, toggled
    )

    def on_state_changed():
        checked = cb.isChecked()
        toggled_action_trigger(checked)
        if value_state is not None:
            context.set_state(value_state, checked)

    cb.stateChanged.connect(on_state_changed)


@QtRenderer.register
def Input(context: RenderContext, params: QtRenderer.schema.Input):

    # TODO: a str value is a little too simple for an input widget, right ?
    make_widget_property("value", str, context, qproperty_name="text")

    with params.widget as w:
        w.widget_class = "QLineEdit"
        value_state = QtRenderer.schema.set_or_bind(context, "value", params.value, "")
        # Append our children to the configured widget:
        w.children += params.children

    le = context.render(w)["widget"]

    # this is needed by parent component who want to affect us.
    context["widget"] = le

    #
    # Trigger applied action, and update applied_state if requested:
    #
    applied = QtRenderer.schema._namespaces.get_action_name(context, "applied")
    applied_action = context.get_handler(params.action_key or params.ID, applied)

    applied_state = value_state
    edited_state = None
    if params.realtime:
        edited_state = value_state

    def on_return_pressed():
        text = le.text()
        applied_action(text)
        if applied_state is not None:
            print("APPLY", applied_state, text)
            context.set_state(applied_state, text)

    le.returnPressed.connect(on_return_pressed)

    #
    # Trigger edited action, and update edited_state if requested:
    #
    edited = QtRenderer.schema._namespaces.get_action_name(context, "edited")
    edited_action = context.get_handler(params.action_key or params.ID, edited)

    def on_edited():
        text = le.text()
        edited_action(text)
        if edited_state is not None:
            context.set_state(edited_state, text)

    le.textChanged.connect(on_edited)


@QtRenderer.register
def Menu(context: RenderContext, params: QtRenderer.schema.Menu):
    def get_menu_from_context(context):
        return context["menu"]

    make_qobject_property(
        "label",
        str,
        context,
        qobject_getter=get_menu_from_context,
        qproperty_name="title",
    )
    make_qobject_property(
        "icon",
        QtRenderer.value_to_icon,
        context,
        qobject_getter=get_menu_from_context,
    )

    def set_popup_at_cursor(context, b):
        context["menu"]._popup_at_cursor = bool(b)

    def get_popup_at_cursor(context):
        b = get_menu_from_context(context)._popup_at_cursor
        return b

    context.register_property(
        "popup_at_cursor", get_popup_at_cursor, set_popup_at_cursor
    )

    parent = context.get("parent_menu")
    parent_is_menu = True
    if parent is None:
        parent_is_menu = False
        parent = context.get("widget")

    menu = QtWidgets.QMenu(parent)
    menu._popup_at_cursor = False
    # This is used by property getters/setters:
    context["menu"] = menu

    if parent_is_menu:
        parent.addMenu(menu)

    with QtRenderer.schema.Group() as setup_properties:
        QtRenderer.schema.set_or_bind(
            context, "label", params.label, params.ID or "Menu"
        )
        QtRenderer.schema.set_or_bind(context, "icon", params.icon, None)
        QtRenderer.schema.set_or_bind(
            context, "popup_at_cursor", params.popup_at_cursor, True
        )
    context.render(setup_properties)

    def setTrigger_state(state):
        if not state:
            return
        if get_popup_at_cursor(context):
            pos = QtGui.QCursor.pos()
        else:
            pos = parent.mapToGlobal(QtCore.QPoint(0, parent.height()))
        menu.popup(pos)
        context.set_state(params.trigger_state, None)

    if params.trigger_state is not None:
        trigger_state = QtRenderer.schema._namespaces.get_state_key(
            context, params.trigger_state
        )
        # connect the change to the triggering state to our menu trigger:
        context.bind_state(trigger_state, setTrigger_state, None)

    # render all children with an updated `parent_menu` (used by MenuAction)
    context.render_children(params.children, parent_menu=menu)


@QtRenderer.register
def MenuAction(context: RenderContext, params: QtRenderer.schema.MenuAction):
    try:
        menu = context["parent_menu"]
    except KeyError:
        raise Exception(
            f"Error creating MenuAction {params.ID}: no parent menu in ancestors."
        )

    def action_getter(context):
        return context["action"]

    make_qobject_property("label", str, context, action_getter, qproperty_name="text")
    make_qobject_property("icon", QtRenderer.value_to_icon, context, action_getter)
    make_qobject_property("checkable", bool, context, action_getter)
    get_checked, set_checked = make_qobject_property(
        "checked", bool, context, action_getter
    )

    action = menu.addAction(params.label or params.ID)
    context["action"] = action

    with QtRenderer.schema.Group() as setup_properties:
        QtRenderer.schema.set_or_bind(
            context, "label", params.label, params.ID or "Action"
        )
        QtRenderer.schema.set_or_bind(context, "icon", params.icon, None)
        QtRenderer.schema.set_or_bind(context, "checkable", params.checkable, False)
        QtRenderer.schema.set_or_bind(context, "checked", params.checked, False)
    context.render(setup_properties)

    action_key = params.action_key or params.ID

    clicked = QtRenderer.schema._namespaces.get_action_name(context, "clicked")
    clicked_action = context.get_handler(action_key, clicked)

    toggled = QtRenderer.schema._namespaces.get_action_name(context, "toggled")
    toggled_action = context.get_handler(action_key, toggled)

    hovered = QtRenderer.schema._namespaces.get_action_name(context, "hovered")
    hovered_action = context.get_handler(action_key, hovered)

    def on_clicked():
        clicked_action()

    def on_toggled():
        # Update our property (it will deal with binded state)
        checked = action.isChecked()
        set_checked(context, checked)
        # Trigger action
        toggled_action(checked)

    def on_hovered():
        hovered_action()

    action.triggered.connect(on_clicked)
    action.toggled.connect(on_toggled)
    action.hovered.connect(on_hovered)
