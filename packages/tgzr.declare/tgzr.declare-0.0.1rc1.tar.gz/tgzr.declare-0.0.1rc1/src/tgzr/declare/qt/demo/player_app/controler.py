"""

Our App Controler
(Business object managing logic stuff that your user want)

It knows nothing about the UI, and uses the renderer to read/write states.

"""
import os
from ....renderer import Renderer

from .playsound import playsound


class Controler:
    """A Base class to build app logic using values from the renderer state store"""

    def __init__(self, renderer: Renderer):
        self._renderer = renderer
        self._app = renderer.create_root_context()["app"]

    def __setitem__(self, name, value):
        """Update a renderer state."""
        self._renderer.update_states({name: value})

    def __getitem__(self, name):
        """Get a state value"""
        return self._renderer.get_state(name)

    def app(self):
        return self._app

    @classmethod
    def with_status(cls, f):
        """
        A decorator for subclasses methods that will report the call
        on the 'status_text' state.
        """

        def decorated(*args, **kwargs):
            self = args[0]
            args_str = ", ".join(
                [str(i) for i in args[1:]] + [f"{k}={v!r}" for k, v in kwargs.items()]
            )
            self["status_text"] = f"{f.__name__}({args_str})"
            return f(*args, **kwargs)

        return decorated


class PlayerAppControler(Controler):
    def __init__(self, renderer):
        super().__init__(renderer)

    def get_blocking(self):
        return self["app/blocking"]

    def current_index(self):
        return self["current_index"]

    def set_current_index(self, i):
        medias = self.medias()
        try:
            medias[self.current_index()]["Status"] = "-"
        except IndexError:
            # The list may have been cleared since
            pass
        self["current_index"] = i
        try:
            self.medias()[i]["Status"] = "<->"
        except IndexError:
            # The list may be empty
            pass
        self.update_view()

    @Controler.with_status
    def refresh_media_list(self):
        path = self["media_folder"]
        if os.path.isdir(path):
            names = [n for n in os.listdir(path) if n.lower().endswith(".mp3")]
        else:
            names = []
        items = []
        for name in names:
            items.append(dict(Path=name, Status="-", Played=0))
        self["medias"] = items
        self.set_current_index(0)
        self.update_view()

    def medias(self):
        return self["medias"]

    def medias_folder(self):
        return self["media_folder"]

    def _offset_current(self, offset):
        current_index = self["current_index"]
        media_count = len(self["medias"])
        if not media_count:
            return
        current_index = (current_index + offset) % media_count
        self.set_current_index(current_index)

    @Controler.with_status
    def rewind(self):
        self.set_current_index(0)

    @Controler.with_status
    def prev(self):
        self._offset_current(-1)

    @Controler.with_status
    def next(self):
        self._offset_current(1)

    @Controler.with_status
    def play(self):
        current_media = self.current_index()
        media = self.medias()[current_media]
        old_status = media["Status"]
        media["Status"] = "Playing"
        self.update_view()
        media_path = os.path.join(self.medias_folder(), media["Path"])
        if self.get_blocking():
            self.enable_toolbar(False)
            playsound(media_path, True)
        else:
            playsound(media_path, False)
        media["Played"] += 1
        media["Status"] = old_status
        self.update_view()
        self.enable_toolbar(True)

    def update_view(self):
        self["medias"] = self.medias()

    def enable_toolbar(self, b):
        self["toolbar/enabled"] = b
        self.app().update()
