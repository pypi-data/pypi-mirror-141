from qtpy import QtWidgets

from .doc_view import DocView
from .components_view import ComponentsView
from .text_view import TextView
from .render_view import RenderView


class Editor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__(None)

        self._presets = []

        self.resize(1200, 600)
        lo = QtWidgets.QVBoxLayout()
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)
        self.setLayout(lo)

        toolbar = QtWidgets.QToolBar(self)
        lo.addWidget(toolbar)

        splitter = QtWidgets.QSplitter(self)
        lo.addWidget(splitter)

        self._doc_view = DocView(splitter, self)
        splitter.addWidget(self._doc_view)
        self._add_view_toggle("Doc", self._doc_view, toolbar)

        self._components_view = ComponentsView(splitter, self)
        self._components_view.current_component_type_changed.connect(
            self._doc_view.load_component_type
        )
        splitter.addWidget(self._components_view)
        self._add_view_toggle("Tree", self._components_view, toolbar)

        self._text_view = TextView(splitter, self)
        splitter.addWidget(self._text_view)
        self._add_view_toggle("Text", self._text_view, toolbar)

        self._render_view = RenderView(splitter, self)
        splitter.addWidget(self._render_view)
        self._add_view_toggle("Render", self._render_view, toolbar)

        toolbar.addSeparator()
        self._presets_cb = QtWidgets.QComboBox(self)
        self._presets_cb.currentTextChanged.connect(self.load_preset)
        toolbar.addWidget(self._presets_cb)

    def _add_view_toggle(self, label, view, toolbar, visible=True):
        a = toolbar.addAction(label)
        a.setCheckable(True)
        a.setChecked(visible)
        a.triggered.connect(lambda checked: view.setVisible(checked))
        view.setVisible(visible)

    def get_renderer(self):
        return self._render_view.get_renderer()

    def add_preset(self, name, UI):
        self._presets.append((name, UI))
        self._presets_cb.clear()
        self._presets_cb.addItems([name for name, ui in self._presets])

    def load_preset(self, preset_name):
        for name, ui in self._presets:
            if name == preset_name:
                self.load_ui(ui)
                return

    def load_ui(self, ui):
        self._doc_view.clear()
        self._components_view.load_ui(ui)
        self._text_view.load_ui(ui)
        self._render_view.clear()
