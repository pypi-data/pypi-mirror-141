from qtpy import QtWidgets

from .renderer import QtRenderer


class App(object):
    """
    Usage:
        from tgzr.declare.qt.app import App

        my_app = App()

        @my_app.setup
        def setup(renderer):
            renderer = my_app.renderer
            # setup state store, handler, etc...

            # do you render:
            renderer.render(some_UI)

        if __name__ == '__main__':
            my_app.run()

    """

    def __init__(self, title="My App, my title.", check_schema=True):
        super().__init__()
        self._title = title
        self._check_schema = check_schema
        self._qt_app = None
        self._renderer = None
        self._setup_function = None

    def setup(self, f):
        self._setup_function = f
        return f

    def _create_renderer(self, host):
        renderer = QtRenderer(host, self._check_schema)
        host.setWindowTitle(self._title)
        host.show()
        return renderer

    def run(self):
        """
        Run the App in standalone mode, creating a QApplication and
        a host widget for it.
        """
        if self._renderer is not None:
            raise Exception("It looks like this app has already had a life.")

        self._qt_app = QtWidgets.QApplication([])
        host = QtWidgets.QWidget()
        self._renderer = self._create_renderer(host)
        self._renderer.update_root_context(app=self)

        self._setup_function(self._renderer)
        self._qt_app.exec_()

    def embed(self, host):
        self._qt_app = QtWidgets.QApplication.instance()
        if self._renderer is None:
            self._renderer = self._create_renderer(host)
        self._renderer.update_root_context(app=self)

        self._setup_function(self._renderer)

    def update(self):
        self._qt_app.processEvents()

    def quit(self):
        widget = self._renderer.create_root_context()["root_widget"]
        widget.close()
