import random
import string

from qtpy import QtWidgets

from .editor import Editor

# we're using the default schema since it's the
# one supported by the QtRenderer.
from ...default.schema import DefaultSchema
from ...enums import Enums


def default_ui():
    S = DefaultSchema
    with S.VBox() as UI:
        S.Button("Yeah !", icon="fa5s.user")

    return UI


def markdown_preset():
    S = DefaultSchema
    with S.VBox() as UI:
        S.Markdown(text="@binded:MD")
        S.Input(value="@binded:MD")
        S.State("MD", value="# Title\n text...")
    return UI


def form_preset():
    S = DefaultSchema
    with S.VBox() as UI:
        with S.Frame(title="My Frame"):
            with S.VBox():
                for i in range(3):
                    with S.HBox():
                        S.State(name=f"params/value_{i}", value=f"value: {i}")
                        S.Label(text=f"Param {i}", fixed_width=100)
                        S.Input(value=f"@binded:params/value_{i}")
                S.Stretch()
                with S.Button("submit", icon="fa5s.user"):
                    S.Handle(
                        key="submit",
                        action="clicked",
                        script="print(get_state('params/'))",
                    )
    return UI


def tabs_preset():
    S = DefaultSchema
    with S.VBox() as UI:
        with S.Tabs():
            with S.Tab(title="User", icon="fa5s.user"):
                with S.HBox(stretch=1):
                    S.Button("Yolo takavoir !!!")
                    S.Button("Button 2")
                    S.Button(label="Button 3")
                with S.HBox():
                    S.PrintStatesButton()
                    S.PrintContextButton()
                S.Button(label="Another Button !?!")
            with S.Tab(title="Tags", icon="fa5s.tags"):
                S.Button("Button 4")
                S.Button("Button 5")
                S.Button(label="Button 6")

    return UI


def table_preset():
    S = DefaultSchema
    with S.VBox() as UI:
        with S.Group(namespace="table_preset"):
            with S.ListState(name="items"):
                length = 10
                for i in range(300):
                    name = "".join(
                        random.choices(string.ascii_uppercase + string.digits, k=length)
                    )
                    value = random.randint(1, 1000)
                    S.ListStateAppend(dict(Name=name, Value=value, Value_2=value - 99))
            S.PrintStatesButton()
            S.ItemView(
                columns=["Name", "Value", "Value_2", "Nope Value"],
                items="@binded:items",
            )

    return UI


def item_view_preset():
    S = DefaultSchema
    with S.VBox() as UI:
        S.H1("Sorry, this demo is not available yet...", word_wrap=True)
        S.Stretch()
    return UI


def embed():
    editor = Editor()
    editor.add_preset("Default", default_ui())
    editor.add_preset("Markdown", markdown_preset())
    editor.add_preset("Form", form_preset())
    editor.add_preset("Tabs", tabs_preset())
    editor.add_preset("Table", table_preset())
    editor.add_preset("ItemView", item_view_preset())
    editor.show()
    editor.load_ui(default_ui())


def main():
    app = QtWidgets.QApplication([])

    embed()

    app.exec_()


if __name__ == "__main__":
    main()
