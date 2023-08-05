from ...enums import Enums
from ..renderer import QtRenderer
from ...render_context import RenderContext
from ..app import App


def _add_elements(schema):
    s = schema
    with s.Frame(title="Elements"):
        with s.VBox():
            with s.Splitter():
                with s.SplitterPanel():
                    s.Label("This is a simple Label")
                    s.Text(
                        "This is a Text, which is in fact a Label with word wrapping activated."
                    )
                    s.H3("This is a Header 3 Label")
                    s.Label(
                        text="This is a formated Label using html.",
                        format="<center><hr>{text}<hr></center>",
                    )
                with s.SplitterPanel():
                    s.Markdown(
                        text="""
# Markdown

The `Markdown` component is easier to use than **html** based Label.
Users without technical background should be able to:
- Enrich their text with **Bold**, *Itaic*, _Underlined_
- Use external editor
- Copy/paste markdown from other markdown enabled apps like Notion or Coda.

It is also usefull for documentation since:
```python
# It supportes python code:
from starwars import *
if this_ship is plenipotentiary:
    find("Amabassador")

```
and command lines:
```
pip install -U tgzr.dshell
```

            """
                    )


def components_demo(renderer: QtRenderer, parent):
    s = renderer.schema
    with parent:
        with s.Group("component_demo"):
            with s.Splitter(orientation=Enums.Orientation.VERTICAL):
                with s.SplitterPanel():
                    _add_elements(s)
                with s.SplitterPanel(
                    layout_orientation=Enums.Orientation.HORIZONTAL,
                    layout_stretch=False,
                ):
                    with s.Frame(title="Controls"):
                        with s.VBox():
                            s.Button("A Button")
                            s.Toggle("A Toggle")
                            s.Input(value="An Input")
                            with s.Group("menu"):
                                with s.Button("show_menu", label="Menu"):
                                    with s.Menu(
                                        "A Menu",
                                        trigger_state="show",
                                        popup_at_cursor=False,
                                    ):
                                        s.MenuAction("A Menu Action")
                                        s.MenuAction("A Menu Action")
                                        s.MenuAction("A Menu Action")
                                        s.MenuAction("A Menu Action")
                            s.Stretch()
                    with s.Frame(title="Item Views"):
                        items = [
                            dict(Path="Spam", Status="In progress"),
                            dict(
                                Path="Foo/Bar/Baz",
                                Status=dict(value="Ok", icon="fa5s.check"),
                            ),
                            dict(
                                Path="Foo/Bar/Spam",
                                Status=dict(
                                    value="Fail !",
                                    icon="fa.warning",
                                    background_color="#FF8888",
                                ),
                            ),
                        ]
                        with s.VBox():
                            with s.Tabs():
                                with s.Tab(
                                    "Tree", icon="mdi.file-tree", layout_stretch=False
                                ):
                                    s.ItemView(
                                        decorated_root=True,
                                        columns=["Path", "Status"],
                                        group_by=["Path"],
                                        items=items,
                                    )
                                with s.Tab(
                                    "Table",
                                    icon="mdi.table-large",
                                    layout_stretch=False,
                                ):
                                    s.ItemView(
                                        columns=["Path", "Status"],
                                        items=items,
                                    )

    def show_menu(renderer, *a, **k):
        renderer.update_states({"component_demo/menu/show": True})

    renderer.set_handler(show_menu, key="show_menu")


def button_demo(renderer: QtRenderer, parent):

    with parent:
        with renderer.schema.Group("button_demo"):
            renderer.schema.Button(label="Click Me !", action_key="a button")
            renderer.schema.Button(label="Click Me Too !", action_key="another button")
            renderer.schema.Label(text="@binded:message")
            renderer.schema.Stretch()

    def on_clicked(self, key, action, context, *args, **kwargs):
        if key == "a button":
            msg = "You clicked me :)"
            print(msg)
            context.set_state("button_demo/message", msg)
        elif key == "another button":
            msg = "You clicked me too :)"
            print(msg)
            context.set_state("button_demo/message", msg)
        else:
            return True  # keep propagating

    renderer.set_handler(on_clicked, action="button_demo/clicked")


def label_demo(renderer: QtRenderer, parent):

    with parent:
        with renderer.schema.Group("label_demo"):
            renderer.schema.H1(text="This is a Header #1 label")
            renderer.schema.H2(text="This is a Header #2 label")
            renderer.schema.H3(text="This is a Header #3 label")
            renderer.schema.H4(text="This is a Header #4 label")
            renderer.schema.Label(text="This is a default label")
            with renderer.schema.HBox():
                with renderer.schema.Label(
                    text="This is a formated label",
                    format=renderer.schema.Binded(state_key="label_format"),
                ) as label:
                    label.widget.layout.stretch = 100
                with renderer.schema.Button(ID="Format"):
                    with renderer.schema.Menu(
                        popup_at_cursor=False, trigger_state="show_menu"
                    ):
                        renderer.schema.MenuAction(ID="Red")
                        renderer.schema.MenuAction(ID="Bold")
                        renderer.schema.MenuAction(ID="Pre")
                renderer.schema.Button(ID="Red")
                renderer.schema.Button(ID="Bold")
                renderer.schema.Button(ID="Pre")
            renderer.schema.Stretch()

    def on_format(renderer: QtRenderer, *a, **k):
        renderer.update_states({"label_demo/show_menu": True})

    def on_red(renderer: QtRenderer, *a, **k):
        renderer.update_states(
            {"label_demo/label_format": "<font color=#884444>{text}</font>"}
        )

    def on_bold(renderer: QtRenderer, *a, **k):
        renderer.update_states({"label_demo/label_format": "<b>{text}</b>"})

    def on_pre(renderer: QtRenderer, *a, **k):
        renderer.update_states({"label_demo/label_format": "<pre>{text}</pre>"})

    renderer.set_handler(on_format, "Format")
    renderer.set_handler(on_red, "Red")
    renderer.set_handler(on_bold, "Bold")
    renderer.set_handler(on_pre, "Pre")


def text_demo(renderer: QtRenderer, parent):
    Schema = renderer.schema
    with parent:
        with Schema.Group("text_demo"):
            with Schema.VBox():
                Schema.Label(
                    text="This is a label, which does not word wrap by default"
                )
                Schema.H1(text="Header 1")
                Schema.H2(text="Header 2")
                Schema.H3(text="Header 3")
                Schema.H3(text="Header 4")
                Schema.Text(
                    text="This is a text with word wrapping..." + 50 * "some text, "
                )
                Schema.Markdown(
                    text="""
# Title
## This is Mardkonw
It is quite **cool !**
```python
also = 'it supports python code'
class ThisMeans(ThatYouCan):
    def get_geeky(self):
        return "AF !"
```
                """
                )
                Schema.Stretch()


def frame_demo(renderer: QtRenderer, parent):
    Schema = QtRenderer.schema

    with parent:
        with Schema.Group("frame_demo"):
            with Schema.VBox():
                with Schema.Frame(title="My Frame"):
                    with Schema.VBox():
                        Schema.Label(text="This frame has a title.")
                        Schema.Button()
                        Schema.Button()
                        Schema.Button()
                        Schema.Stretch()
                with Schema.Frame():
                    with Schema.VBox():
                        Schema.Label(text="This frame has no title.")
                        Schema.Button()
                        Schema.Button()
                        Schema.Button()
                        Schema.Stretch()


def binding_demo(renderer: QtRenderer, parent):
    Schema = renderer.schema

    visual_debug = False

    with parent:
        with Schema.Group("binding_demo"):
            with Schema.VBox(ID="TOP"):
                with Schema.HBox(ID="ButtBOX", debug=visual_debug):
                    Schema.Button(ID="B1", label=Schema.Binded(state_key="label"))
                    with Schema.Button(ID="B2", label="Hop !") as b:
                        Schema.Set(name="label", value="Submit")
                        b.widget.enabled = Schema.Binded(state_key="enabled")
                with Schema.Toggle(value="@Binded:enabled") as t:
                    t.label = 'This use the "@Binded:" prefix to bind the value'
                    t.widget.layout.alignment = Enums.Alignment.HCENTER
                Schema.Input(ID="I1", value=Schema.Binded(state_key="label"))
                with Schema.Input(ID="I1", value="This is a text input..."):
                    Schema.Set(name="value", value="???")
                Schema.Stretch()

    renderer.update_states(
        {"binding_demo/label": "Yolo !", "binding_demo/enabled": True}
    )


def include_demo(renderer: QtRenderer, parent):
    Schema = renderer.schema

    with Schema.Frame(title="V1"):
        with Schema.VBox(ID="included_VBox") as include_ui_v1:
            Schema.Button(ID="included_B1")
            Schema.Button(ID="included_B2")
            Schema.Button(ID="included_B3")
            Schema.Stretch()

    with Schema.Frame(title="V2"):
        with Schema.HBox(ID="included_HBox") as include_ui_v2:
            Schema.Button(ID="included_B1")
            Schema.Button(ID="included_B2")
            Schema.Button(ID="included_B3")
            Schema.Stretch()

    with parent:
        with Schema.Group("include_demo"):
            with Schema.VBox():
                Schema.Button(ID="Swap Include")
                Schema.Include(source_state="INCLUDE", trigger_state="reload")

    def swap_include(renderer, key, action, context, *args, **kwargs):
        current = context.get_state("include_demo/current", "v1")
        print("   current", current)
        if current == "include_demo/v1":
            current = "include_demo/v2"
        else:
            current = "include_demo/v1"
        context.set_state("include_demo/current", current)
        context.set_state("include_demo/INCLUDE", context.get_state(current))
        context.set_state("include_demo/reload", True)

    renderer.set_handler(handler=swap_include, key="Swap Include")

    renderer.update_states(
        {
            "include_demo/v1": include_ui_v1.dict(),
            "include_demo/v2": include_ui_v2.dict(),
            "include_demo/current": "include_demo/v1",
            "include_demo/INCLUDE": include_ui_v1.dict(),
            "include_demo/reload": "change this to relod the indluded UI",
        }
    )


def tabs_demo(renderer, parent):
    schema: QtRenderer.schema = renderer.schema

    with parent:
        with schema.Group("tabs_demo"):
            with schema.Tabs(closable=False, movable=True):
                with schema.Tab(ID="Tab #1", icon="fa5s.user"):
                    schema.Button()
                    schema.Button()
                    schema.Button()
                with schema.Tab(
                    layout_stretch=False,
                    layout_orientation=Enums.Orientation.HORIZONTAL,
                    icon="fa5.user",
                ):
                    schema.Button()
                    schema.Button()
                    schema.Button()


def menu_demo(renderer: QtRenderer, parent):
    with parent:
        with QtRenderer.schema.Group(namespace="menu_demo"):
            QtRenderer.schema.Label(text=renderer.schema.Binded(state_key="label_text"))
            # At cursor menu
            with QtRenderer.schema.Menu(trigger_state="popup_some_menu") as m:
                m.popup_at_cursor = True
                QtRenderer.schema.MenuAction(
                    ID="Click him", icon="fa5s.briefcase-medical"
                )
                QtRenderer.schema.MenuAction(
                    ID="Click him too", icon="fa5s.laptop-medical"
                )
                with QtRenderer.schema.Menu(label="Sub Menu", icon="fa5s.sd-card"):
                    QtRenderer.schema.MenuAction(
                        ID="Click sub-him", icon="fa5s.briefcase-medical"
                    )
                    QtRenderer.schema.MenuAction(
                        ID="Click sub-him too", icon="fa5s.laptop-medical"
                    )

                QtRenderer.schema.MenuAction(
                    ID="Click him tree", icon="fa5s.comment-medical"
                )

            with QtRenderer.schema.VBox():
                with QtRenderer.schema.HBox():
                    with QtRenderer.schema.Button(
                        label="Popup here", action_key="mine"
                    ):
                        # Button menu
                        with QtRenderer.schema.Menu(
                            trigger_state="popup_button_menu"
                        ) as m:
                            m.popup_at_cursor = False
                            QtRenderer.schema.MenuAction(
                                ID="Click me",
                                checkable=True,
                                checked=True,
                                icon="fa5s.briefcase",
                            )
                            QtRenderer.schema.MenuAction(
                                ID="Click me too", icon="fa5s.laptop"
                            )
                            QtRenderer.schema.MenuAction(
                                ID="Click me tree", icon="fa5s.comment"
                            )
                    QtRenderer.schema.Button(label="Pop his popup", action_key="his")
                QtRenderer.schema.Button(label="Pop at cursor", action_key="cursor")
                QtRenderer.schema.Stretch()

    def show_message(context, text):
        print("Message:", text)
        context.set_state("menu_demo/label_text", f"## {text}")

    def on_hover(renderer, key, action, context, *args, **kwargs):
        show_message(context, f"Hover: {key}")

    def on_toggled(renderer, key, action, context, *args, **kwargs):
        show_message(context, f"Toggled: {key}")

    def on_clicked(renderer, key, action, context, *args, **kwargs):
        if key in ("mine", "his"):
            show_message(context, "Show Menu: bubton_menu")
            context.set_state("menu_demo/popup_button_menu", True)
        elif key == "cursor":
            show_message(context, "Show Menu: some_menu")
            context.set_state("menu_demo/popup_some_menu", True)
        else:
            show_message(context, f"Clicked: {key}")
            context.set_state("menu_demo/label_text", f"## Clicked: {key}")

    renderer.set_handler(on_hover, action="menu_demo/hovered")
    renderer.set_handler(on_toggled, action="menu_demo/toggled")
    renderer.set_handler(on_clicked, action="menu_demo/clicked")


def states_demo(renderer: QtRenderer, parent):
    s = renderer.schema

    def declare_field(state):
        """Creates a label and an input for the given state"""
        text = state.split("/", 1)[-1].replace("_", " ").title()
        with s.HBox():
            s.Label(text, fixed_width=100)
            s.Input(value="@binded:" + state)

    with parent:
        with s.Group("states_demo"):
            # State namespace can be controled by States or Group:
            with s.States("form"):
                with s.States("name"):
                    s.State("first_name", value="Harry")
                    s.State("last_name", value="Cover")
                with s.States("colors"):
                    s.State("hair", value="Brun")
                    s.State("eyes", value="Green")

            # Using Group, you can affect both state and action namespace:
            with s.Group("form"):
                with s.Frame(title="User Info"):
                    with s.VBox():
                        with s.Frame(title="Name"):
                            with s.Group("name"):
                                with s.VBox():
                                    declare_field("first_name")
                                    declare_field("last_name")
                        with s.Frame(title="Colors"):
                            with s.Group("colors"):
                                with s.VBox():
                                    declare_field("hair")
                                    declare_field("eyes")
                        with s.HBox():
                            s.Button("Submit")
                            s.Button("Submit Name")
                            s.Button("Submit Colors")
            s.Label(
                text="@binded:info",
                format="<b>Submited data:</b><br>{text}",
                word_wrap=True,
            )

            # The States component always affects Binding, but not actions:
            with s.Frame(title="Project List"):
                with s.Group("projects"):
                    with s.ListState("names"):
                        s.ListStateAppend("Project #1")
                        s.ListStateAppend("Project #2")
                        s.ListStateAppend("Project #3")
                    with s.VBox():
                        s.Label("Projects:")
                        s.Text("@binded:names")
                        s.Stretch()
                        with s.HBox():
                            s.Stretch()
                            s.Button("Add Project")
                            s.Button("Clear Projects")

    def on_edited(*a, **k):
        pass

    def on_applied(*a, **k):
        pass

    def on_submit_clicked(renderer, key, action, context):
        if key == "Submit":
            params = context.get_states("states_demo/form/")
        elif key == "Submit Name":
            params = context.get_states("states_demo/form/name/")
        elif key == "Submit Colors":
            params = context.get_states("states_demo/form/colors/")
        else:
            params = "!?!?"
        print("Submit:", params)
        context.set_state("states_demo/info", params)

    def on_projects_clicked(renderer, key, action, context):
        if key == "Add Project":
            s = renderer.schema
            # (Note: we could also read the state, modify it, then set it.
            # But using declaration is more fun ;) )
            # This context, which is the button one, is already namespaced.
            # So we dont need to use namespaces:
            with s.ListState("names") as UI:
                s.ListStateAppend(value="New Project")
            context.render(UI)
        elif key == "Clear Projects":
            # context.set_state does not honor namespaces, you
            # need to include it in the state key:
            context.set_state("states_demo/projects/names", [])

    # This is to silence the default handler.
    # TODO: maybe add a way to turn off control actions ?
    renderer.set_handler(on_edited, action="states_demo/form/name/edited")
    renderer.set_handler(on_applied, action="states_demo/form/name/applied")
    renderer.set_handler(on_edited, action="states_demo/form/colors/edited")
    renderer.set_handler(on_applied, action="states_demo/form/colors/applied")

    renderer.set_handler(on_submit_clicked, action="states_demo/form/clicked")
    renderer.set_handler(on_projects_clicked, action="states_demo/projects/clicked")
    # renderer.update_states({"states_demo/info": ""})


def splitter_demo(renderer: QtRenderer, parent):
    s = renderer.schema
    with parent:
        with s.Group("splitter_demo"):
            with s.Splitter():
                with s.SplitterPanel():
                    s.Button(1)
                    s.Button(2)
                    s.Button(3)
                with s.SplitterPanel(layout_stretch=False):
                    with s.Splitter(orientation=Enums.Orientation.VERTICAL):
                        with s.SplitterPanel():
                            s.Button(4)
                            s.Button(5)
                            s.Button(6)
                        with s.SplitterPanel():
                            s.Button(7)
                            s.Button(8)
                            s.Button(9)


def table_demo(renderer: QtRenderer, parent):
    import random

    name_icon = dict(
        foo="fa5s.futbol",
        bar="fa5s.beer",
        baz="fa5s.bacterium",
        spam="fa5s.hamburger",
        eggs="fa5s.egg",
    )
    status_color = dict(
        WIP="#8888FF",
        RTK="#FF8888",
        OOP="#888888",
        DONE="#88FF88",
    )
    count = 1000
    items = []
    for i in range(count):
        name = random.choice(list(name_icon.keys()))
        status = random.choice(list(status_color.keys()))
        items.append(
            dict(
                Name=dict(value=name, icon=name_icon[name]),
                Index=i,
                First=random.randint(1, 100),
                Last=random.randint(50, 300),
                Status=dict(value=status, background_color=status_color[status]),
            )
        )
    s = renderer.schema
    with parent:
        with s.Group("table_demo"):
            s.ItemView(
                columns=["Name", "Index", "First", "Last", "Status"],
                items=items,
                auto_expand_groups=False,
            )


def tree_demo(renderer: QtRenderer, parent):
    import random
    import datetime

    # columns
    columns = [
        dict(label="Shot", icon="fa5s.images", group_icon="fa5s.film"),
        dict(label="Dept", icon="fa5s.calendar-check"),
        "Status",
        "Start",
        "End",
    ]
    # items
    depts = "Anim", "Lighting", "Comp", "Grading"
    status_color = dict(
        WIP="#8888FF",
        RTK="#FF8888",
        OOP="#888888",
        DONE="#88FF88",
    )

    sq_count = random.randint(5, 10)
    items = []
    for sq in range(sq_count):
        sh_count = random.randint(2, 20)
        for sh in range(sh_count):
            task_count = random.randint(1, len(depts))
            tasks = random.choices(depts, k=task_count)
            start = datetime.date.today() - datetime.timedelta(
                days=random.randint(-100, 100)
            )
            end = datetime.date.today() - datetime.timedelta(
                days=random.randint(-100, 100)
            )

            for task in tasks:
                status = random.choice(list(status_color.keys()))
                items.append(
                    dict(
                        Shot=dict(
                            value=f"Film/SQ{sq:03}/SH{sh:03}",
                            icon="fa5s.images",
                        ),
                        Dept=task,
                        Start=start.isoformat(),
                        End=end.isoformat(),
                        Status=dict(
                            value=status, background_color=status_color[status]
                        ),
                    )
                )

    s = renderer.schema
    with parent:
        with s.Group("tree_demo"):
            s.State("group_by", value=["Shot", "Dept"])
            s.Toggle("Flat", value="@binded:disable_group_by")
            script = "context.set_state('tree_demo/group_by', not args[0] and ['Shot', 'Dept'] or None )"
            s.Handle(key="Flat", action="toggled", script=script)
            s.ItemView(
                decorated_root=True,
                columns=columns,
                items=items,
                group_by="@binded:group_by",
                auto_group_separator="/",
                sortable=True,
            )


def overlay_demo(renderer: QtRenderer, parent):
    s = QtRenderer.schema

    with parent:
        with s.Group(namespace="overlay_demo"):
            s.Button(1)
            s.Button(2)
            s.Button(3)
            s.Button(4)
            s.Button(5)
            s.Button(6)
            s.Button(8)
            s.Button(9)
            with s.Overlay():
                with s.VBox():
                    s.Stretch()
                    text = "This text is in an Overlay, on top of the buttons."
                    s.H2(text=text, word_wrap=True)
                    s.Button(label="This Button too !")
                    s.Stretch()


def anchor_demo(renderer: QtRenderer, parent):
    s = renderer.schema

    with parent:
        with s.Group("anchor_demo"):
            with s.Anchors("demo"):
                with s.HBox():
                    with s.Group("fx"):
                        with s.Button("@binded:selected", action_key="select"):
                            with s.Menu(
                                popup_at_cursor=False,
                                trigger_state="show_menu",
                            ):
                                s.MenuAction("Default")
                                s.MenuAction("Jiggle")
                                s.MenuAction("Highlight")
                                s.MenuAction("Bubble")
                    with s.Group("target"):
                        with s.Button("@binded:selected", action_key="select"):
                            with s.Menu(
                                popup_at_cursor=False,
                                trigger_state="show_menu",
                            ):
                                s.MenuAction("Foo")
                                s.MenuAction("Bar")
                                s.MenuAction("Spam & Eggs")
                                s.MenuAction("Many")
                    s.Button("Go !")
                with s.Group(namespace="anchored"):
                    with s.Anchor("Foo", effect="Jiggle"):
                        s.Button("Foo")
                    with s.Anchor("Bar", effect="Highlight"):
                        s.Button("Bar")
                    with s.Anchor("Spam & Eggs", effect="Bubble"):
                        s.Button("Spam")
                        s.Button("Eggs")
                    with s.Anchor("Many", effect="Bubble"):
                        s.Button("There")
                        s.Button("Is")
                        s.Button("A")
                        s.Button("Nice")
                        s.Button("Default")
                        s.Button("Offset")
                        s.Button("For each")
                        s.Button("Anchor")
                        s.Button("Component")

                    s.Stretch()

    states = {}
    states["anchor_demo/fx/selected"] = "Default"
    states["anchor_demo/target/selected"] = "Many"

    renderer.update_states(states)

    def on_fx_clicked(renderer, key, action, context: RenderContext):
        if key == "select":
            context.set_state("anchor_demo/fx/show_menu", True)
        else:
            # it's a menu entry, store the selected FX:
            context.set_state("anchor_demo/fx/selected", key)

    def on_target_clicked(renderer, key, action, context: RenderContext):
        if key == "select":
            context.set_state("anchor_demo/target/show_menu", True)
        else:
            # it's a menu entry, store the selected FX:
            context.set_state("anchor_demo/target/selected", key)

    renderer.set_handler(on_fx_clicked, action="anchor_demo/fx/clicked")
    renderer.set_handler(on_target_clicked, action="anchor_demo/target/clicked")
    renderer.set_handler(lambda *a, **k: None, action="anchor_demo/fx/hovered")
    renderer.set_handler(lambda *a, **k: None, action="anchor_demo/target/hovered")

    def on_go(renderer, key, action, context):
        print(context["anchor_collections"]["demo"])
        fx = context.get_state("anchor_demo/fx/selected")
        if fx == "Default":
            fx = None
        anchor_name = context.get_state("anchor_demo/target/selected")
        anchor_context = context["anchor_collections"]["demo"][anchor_name]
        trigger = anchor_context["trigger_state"]
        context.set_state(trigger, fx)

    renderer.set_handler(on_go, key="Go !")
    renderer.set_handler(on_go, key="DEMO/demo_include", action="render_done")


def get_demo_UI(renderer: QtRenderer):
    demo_funcs = (
        components_demo,
        button_demo,
        label_demo,
        text_demo,
        frame_demo,
        binding_demo,
        include_demo,
        tabs_demo,
        menu_demo,
        states_demo,
        table_demo,
        tree_demo,
        overlay_demo,
        anchor_demo,
    )
    name_to_func = dict((func.__name__, func) for func in demo_funcs)

    s = renderer.schema
    with s.VBox() as UI:
        with s.HBox():
            s.H2("tgzr.declare - demo")
            s.Stretch()
            s.Button("Quit")
        with s.Splitter():
            with s.SplitterPanel():
                for func in demo_funcs:
                    name = func.__name__
                    label = name.rsplit("_", 1)[0]
                    s.Button(ID=name, label=label)
            with s.SplitterPanel(layout_stretch=False):
                with s.Frame(title="@binded:DEMO/label"):
                    with s.VBox():
                        s.Include(
                            source_state="DEMO/demo_include",
                            trigger_state="DEMO/update",
                        )

    def on_demo(renderer, key, action, context):
        if key == "Quit":
            app = renderer.create_root_context()["app"]
            app.quit()
            return

        func = name_to_func[key]
        context.set_state("DEMO/label", key.rsplit("_", 1)[0])
        to_include = renderer.schema.VBox()
        func(renderer, to_include)
        context.set_state("DEMO/demo_include", to_include.dict())
        context.set_state("DEMO/update", True)

    renderer.set_handler(on_demo, action="clicked")

    return UI


def test(renderer):
    s = renderer.schema
    with s.VBox() as UI:
        with QtRenderer.schema.Group("TEST"):
            with QtRenderer.schema.Frame(title="Frame!"):
                with QtRenderer.schema.VBox():
                    QtRenderer.schema.Button()
    return UI


app = App()


@app.setup
def demo(renderer):

    renderer.update_states({"state": "before"})

    if 1:
        UI = get_demo_UI(renderer)
    else:
        UI = test(renderer)

    if 0:
        UI.pprint()
    renderer.render(UI)

    renderer.update_states({"state": "after"})


if __name__ == "__main__":
    app.run()
