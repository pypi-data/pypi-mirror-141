"""

    The `DefaultSchema` is the first one I wrote. Not the best ;)
    More will come and this one will probably disapear...

"""
from typing import Optional

from ..enums import Enums
from ..models import (
    ComponentModel,
    ParamsModel,
    BindableBool,
    BindableInt,
    BindableString,
    BindableList,
    BindableAlignment,
    BindableOrientation,
)
from ..base.schema import BaseSchema

#
#   Widget
#


class LayoutItem(ComponentModel):

    stretch: BindableInt = 0
    alignment: Optional[BindableAlignment] = None
    separator: bool = False


class Widget(ComponentModel):

    widget_class: Optional[str] = None
    enabled: BindableBool = True  # TODO: support binding in Qt
    visible: BindableBool = True  # TODO: support binding in Qt
    tooltip: BindableString = None  # TODO: support param + binding in Qt
    layout: LayoutItem = LayoutItem()


#
#   Elements
#
class TextWidgetCommun(ParamsModel):
    text: BindableString = None
    word_wrap: BindableBool = False
    fixed_width: BindableInt = None


class Label(ComponentModel, TextWidgetCommun):
    """
    Add a text to the UI.

    The `format` parameter can be used to decorate the text.
    The `{text}` place holder will be replaced by the value
    of the `text` parameter.
        `<h2>{text}</h2>`
    """

    format: BindableString = None
    widget: Widget = Widget()


class H1(ComponentModel, TextWidgetCommun):
    pass


class H2(ComponentModel, TextWidgetCommun):
    pass


class H3(ComponentModel, TextWidgetCommun):
    pass


class H4(ComponentModel, TextWidgetCommun):
    pass


class Text(ComponentModel, TextWidgetCommun):
    pass


class Markdown(ComponentModel):
    text: BindableString = ""
    min_width: Optional[int] = None
    min_height: Optional[int] = None

    widget: Widget = Widget()


#   Controls
#
class Button(ComponentModel):

    label: BindableString = None
    icon: BindableString = None
    action_key: Optional[str] = None

    widget: Widget = Widget()


class Toggle(ComponentModel):

    label: BindableString = None
    value: BindableBool = False
    action_key: Optional[str] = None

    widget: Widget = Widget()


class Input(ComponentModel):

    value: BindableString = ""
    action_key: Optional[str] = None
    realtime: Optional[bool] = True
    "Update the value on every change ? (or only on Enter key)"

    widget: Widget = Widget()


#   Container
#


class LayoutCommun(ParamsModel):
    """
    Those parameters are commun to all layout related Components.
    """

    debug: bool = False
    stretch: BindableInt = 0
    margins: BindableInt = None


class Layout(ComponentModel, LayoutCommun):
    """
    Builds a layout as described.

    You should not use this, but prefer the VBox, HBox, etc... components.
    """

    layout_class: str = None
    orientation: Enums.Orientation = Enums.Orientation.VERTICAL


class VBox(ComponentModel, LayoutCommun):
    """
    Adds a Layout which organizes its children vertically.
    """


class HBox(ComponentModel, LayoutCommun):
    """
    Adds a Layout which organizes its children horizontally.
    """


class Stretch(ComponentModel):
    """
    Adds a space in the current Layout.
    """


class Frame(ComponentModel):
    """
    Adds a Frame which can receive a Layout.

    If a title is given, a surronding box and a title will
    be visible.

    If `checkable` is True, a check box will be shown next to
    the frame title. This checkbox will enable/disable every component
    in the frame.
    """

    title: BindableString = None
    checkable: BindableBool = None
    checked: BindableBool = None
    flat: BindableBool = None
    widget: Widget = Widget()


class Tabs(ComponentModel):
    """
    A Component which can have some `Tab` child components.
    """

    closable: BindableBool = False
    movable: BindableBool = False
    current: BindableInt = 0
    widget: Widget = Widget()


class Tab(ComponentModel):
    """
    A Component which can but the child of a `Tabs` components.

    The Tab child component will be layouted accordingly to the
    `layout_orientation` param.

    If `layout_streatch` is True, a `Strech` will be added after
    the last children.
    """

    title: BindableString = None
    icon: BindableString = None
    layout_orientation: Enums.Orientation = Enums.Orientation.VERTICAL
    layout_stretch: bool = True
    widget: Widget = Widget()


class Menu(ComponentModel):
    label: BindableString = None
    icon: BindableString = None

    popup_at_cursor: BindableBool = True
    trigger_state: Optional[str] = None


class MenuAction(ComponentModel):
    label: BindableString = None
    icon: BindableString = None
    checkable: BindableBool = None
    checked: BindableBool = None

    action_key: Optional[str] = None
    hovered_action_key: Optional[str] = None


class Splitter(ComponentModel):
    orientation: BindableOrientation = Enums.Orientation.HORIZONTAL
    widget: Widget = Widget()


class SplitterPanel(ComponentModel):
    layout_orientation: Enums.Orientation = Enums.Orientation.VERTICAL
    layout_stretch: bool = True
    widget: Widget = Widget()


class Overlay(ComponentModel):
    """
    An area matching the parent area where you can
    add component 'floating' over the parent components.
    """

    name: str = None
    visible: BindableBool = True
    enabled: BindableBool = True


class Anchors(ComponentModel):
    name: str = None


class Anchor(ComponentModel):
    name: str = None
    trigger_state: str = None
    effect: BindableString = None


class ItemView(ComponentModel):
    columns: BindableList = ["Name"]
    items: BindableList = []
    multiple_selection: BindableBool = False
    current_item_state: Optional[str] = None
    selected_items_state: Optional[str] = None
    group_by: BindableList = []
    auto_group_separator: BindableString = None
    auto_expand_groups: BindableBool = True
    sortable: BindableBool = False
    filter: BindableString = None
    use_filter: BindableBool = False
    decorated_root: BindableBool = False
    header_hidden: BindableBool = False
    icon_size: BindableInt = 24
    widget: Widget = Widget()


class PrintStatesButton(ComponentModel):
    pass


class PrintContextButton(ComponentModel):
    pass


#
#   The Schema
#

# NB: This split into several schemas is just
# to help the categoriation of the components in
# GUIs (like the editor's 'Add Comopnent' menu)


class Widgets:
    Widget = Widget
    LayoutItem = LayoutItem


class Elements:
    Label = Label
    H1 = H1
    H2 = H2
    H3 = H3
    H4 = H4
    Text = Text
    Markdown = Markdown


class Controls:
    Button = Button
    Toggle = Toggle
    Input = Input
    Menu = Menu
    MenuAction = MenuAction


class Containers:
    Layout = Layout
    VBox = VBox
    HBox = HBox
    Stretch = Stretch
    Frame = Frame
    Tabs = Tabs
    Tab = Tab
    Splitter = Splitter
    SplitterPanel = SplitterPanel
    Overlay = Overlay
    Anchors = Anchors
    Anchor = Anchor


class Views:
    ItemView = ItemView


class Debug:
    PrintStatesButton = PrintStatesButton
    PrintContextButton = PrintContextButton


class DefaultSchema(BaseSchema, Widgets, Elements, Controls, Containers, Views, Debug):
    """
    This is the first one I wrote. Not the best ;)

    More carefully curaretd schemas will later be implemented and
    this one will probably disapear...
    """


if __name__ == "__main__":
    # NOTE: this is a quick and ugly thing, dont do this at home ! :p
    def print_component(name, component, indent=1):
        print(f"{indent*'    '}- {name}")
        for param_name in component.__fields__:
            if param_name in ("TYPE", "ID", "children"):
                continue
            print(f"{(indent+1)*'    '}- {param_name}")
            param = getattr(component, param_name)
            try:
                getattr(param, "TYPE")
            except AttributeError:
                pass
            else:
                print_component(param_name, param, indent + 1)

    for name, model in DefaultSchema.params_models():
        print_component(name, model())
        print()
