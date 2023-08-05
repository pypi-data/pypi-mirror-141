import inspect
import pprint

from qtpy import QtWidgets, QtGui
import pygments.formatters
import markdown

from ...models import ParamsModel, ComponentModel, RootModel


class _DocMode(object):
    def __init__(self, view):
        super().__init__()
        self.view = view

    def label(self):
        return self.__class__.__name__

    def get_html(self, component_type):
        raise NotImplementedError


class Documentation(_DocMode):
    def get_md(self, component_type, title=None, header_string="##"):
        title = title or component_type
        schema = self.view.get_renderer().schema
        model = getattr(schema, component_type)
        # source = pprint.pformat(model())
        source = inspect.getsource(model)
        md = f"{header_string} {title}\n```python\n{source}```"

        #
        # Add base types doc:
        #
        for base in model.__mro__[1:]:
            if base in (ParamsModel, ComponentModel, RootModel):
                continue
            if issubclass(base, ParamsModel):
                component_type = base.__name__
                source = inspect.getsource(base)
                md += f"\n\nWith inherited members from **{component_type}**:\n```python\n{source}\n```"

        #
        # Add params type doc:
        #
        for name, value in model():
            if isinstance(value, ParamsModel):
                component_type = value.__class__.__name__
                md += "\n\n" + self.get_md(
                    component_type,
                    title + "." + name,
                    header_string="### ",
                )

        return md

    def get_html(self, component_type):
        md = self.get_md(component_type)
        html = markdown.markdown(md, extensions=["codehilite", "fenced_code"])
        return html


class Source(_DocMode):
    def get_html(self, component_type):
        renderer = self.view.get_renderer()
        try:
            R = renderer.get_renderer(component_type)
        except AttributeError:
            md = f"## Unknown component type `{component_type}`"
        else:
            source = inspect.getsource(R)
            md = f"## {component_type}\n\n```python\n{source}```"

        html = markdown.markdown(md, extensions=["codehilite", "fenced_code"])
        return html


class DocView(QtWidgets.QWidget):
    def __init__(self, parent, editor):
        super().__init__(parent)
        self.editor = editor

        self._modes = [Documentation(self), Source(self)]
        self._mode_index = -1

        self._component_type = None

        lo = QtWidgets.QVBoxLayout()
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)
        self.setLayout(lo)

        top_lo = QtWidgets.QHBoxLayout()
        lo.addLayout(top_lo)

        self._mode_button = QtWidgets.QPushButton(self)
        self._mode_button.clicked.connect(self.toggle_mode)
        top_lo.addWidget(self._mode_button)

        self._te = QtWidgets.QTextEdit(self)
        doc = self._te.document()
        doc.setDefaultStyleSheet(pygments.formatters.HtmlFormatter().get_style_defs())
        self._te.setAcceptRichText(False)
        self._te.setWordWrapMode(QtGui.QTextOption.NoWrap)
        lo.addWidget(self._te)

        self.toggle_mode()
        self.update_content()

    def get_renderer(self):
        return self.editor.get_renderer()

    def get_mode(self):
        return self._modes[self._mode_index]

    def toggle_mode(self):
        self._mode_index = (self._mode_index + 1) % len(self._modes)
        self._mode_button.setText(self.get_mode().label())
        self.update_content()

    def clear(self):
        self._te.clear()

    def load_component_type(self, component_type):
        self.clear()
        self._component_type = component_type
        self.update_content()

    def update_content(self):
        print("Update Doc")
        if self._component_type is None:
            self._te.setText("No component type selected")
            return

        self._te.setHtml(self.get_mode().get_html(self._component_type))
