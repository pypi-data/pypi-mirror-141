from qtpy import QtWidgets

from ..renderer import QtRenderer


class RenderView(QtWidgets.QWidget):
    def __init__(self, parent, editor):
        super().__init__(parent)
        self.editor = editor

        lo = QtWidgets.QVBoxLayout()
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)
        self.setLayout(lo)

        top_lo = QtWidgets.QHBoxLayout()
        lo.addLayout(top_lo)

        top_lo.addStretch()

        b = QtWidgets.QPushButton(self)
        b.setText("Clear")
        b.clicked.connect(self._rebuild_host)
        top_lo.addWidget(b)

        self._host = None

        self._host_parent = QtWidgets.QFrame(self)
        self._host_parent.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken)
        self._host_parent.setLayout(QtWidgets.QVBoxLayout())
        lo.addWidget(self._host_parent)

        self._renderer = None

    def get_renderer(self):
        if self._renderer is None:
            if self._host is None:
                self._host = QtWidgets.QWidget(self._host_parent)
                self._host_parent.layout().addWidget(self._host)
                self._host.show()
            self._renderer = QtRenderer(self._host)
        return self._renderer

    def clear(self):
        print("CLEAR RENDER")

    def _rebuild_host(self):
        if self._renderer is None:
            # Nothing to clear if we ain't got any renderer
            return
        if self._host is not None:
            self._host.deleteLater()

        self._host = QtWidgets.QWidget(self)
        self._host_parent.layout().addWidget(self._host)
        self._renderer.set_host(self._host)

    def render(self, ui):
        self._rebuild_host()
        self.get_renderer().render(ui)
