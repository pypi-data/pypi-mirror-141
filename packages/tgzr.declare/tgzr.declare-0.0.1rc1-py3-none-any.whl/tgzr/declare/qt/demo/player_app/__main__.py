from ...schema import QtSchema
from ...app import App, QtRenderer

from .controler import PlayerAppControler

#
#   UI
#


def ToolbarButton(action_name, icon):
    s = QtSchema
    with s.Button(
        ID=f"toolbar.{action_name}",
        action_key=action_name,
        label=action_name.title(),
        icon=icon,
    ) as b:
        b.widget.tooltip = action_name.title()
        b.widget.enabled = s.Binded(state_key="enabled")


def create_media_controls():
    with QtSchema.HBox():
        with QtSchema.Group(namespace="toolbar"):
            ToolbarButton("Rewind", "ph.rewind-thin")
            ToolbarButton("Prev", "ph.skip-back-thin")
            ToolbarButton("Play", "ph.play-circle")
            ToolbarButton("Next", "ph.skip-forward-thin")
        QtSchema.Stretch()


def create_app_controls():
    with QtSchema.Group(namespace="app"):
        QtSchema.Toggle("Blocking", value="@binded:blocking")
        ToolbarButton("Quit", "ph.sign-in-bold")


def create_playlist_controls():
    with QtSchema.HBox():
        QtSchema.Input(value="@binded:media_folder")
        ToolbarButton("Refresh", "mdi6.refresh")


def create_playlist():
    QtSchema.ItemView(
        columns=QtSchema.Binded(state_key="media_columns"), items="@binded:medias"
    )


def create_footer():
    QtSchema.Label(text="@binded:status_text")


def get_UI():

    with QtSchema.VBox() as UI:
        with QtSchema.HBox():
            create_media_controls()
            create_app_controls()
        create_playlist_controls()
        create_playlist()
        create_media_controls()
        create_footer()
    return UI


#
#   ACTIONS
#


def on_refresh(renderer, key, action, context, *args, **kwargs):
    controler = context["controler"]
    controler.refresh_media_list()


def on_toolbar_clicked(renderer, key, action, context, *args, **kwargs):
    controler = context["controler"]

    if key == "Rewind":
        controler.rewind()

    elif key == "Prev":
        controler.prev()

    elif key == "Next":
        controler.next()

    elif key == "Play":
        controler.play()


def on_app_clicked(renderer, key, action, context, *args, **kwargs):
    if key == "Quit":
        app.quit()


#
#   APP
#

app = App("Player Demo")


@app.setup
def setup(renderer: QtRenderer):
    from . import assets

    #
    # Add access to our controler
    #
    controler = PlayerAppControler(renderer)
    renderer.update_root_context(controler=controler)

    #
    # Setup States
    #
    states = dict()
    states["media_columns"] = ["Path", "Status", "Played"]
    states["medias"] = []
    states["current_index"] = 0
    states["media_folder"] = assets.__path__[0]
    states["app/blocking"] = True
    states["toolbar/enabled"] = True

    renderer.update_states(states)

    #
    # Setup Handlers
    #
    renderer.set_handler(on_refresh, key="Refresh")
    renderer.set_handler(on_app_clicked, action="app/clicked")
    renderer.set_handler(on_app_clicked, action="app/toggled")
    renderer.set_handler(on_toolbar_clicked, action="toolbar/clicked")

    # Note that we're assuming a QtSchema in this
    # demo but one can get the actual schema used
    # by the renderer with:
    # schema = renderer.schema
    renderer.render(get_UI())

    controler.refresh_media_list()


if __name__ == "__main__":
    app.run()
