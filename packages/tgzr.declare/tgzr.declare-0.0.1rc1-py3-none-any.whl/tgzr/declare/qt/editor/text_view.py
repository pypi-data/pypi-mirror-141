import pprint
import json

from qtpy import QtWidgets, QtGui
import pygments.formatters
import markdown

from ...default.schema import DefaultSchema
from ...enums import _EnumMixin, Enums
from ...serialization import JSON as JSON_serialization


class TextMode(object):
    @classmethod
    def label(cls):
        return cls.__name__.replace("_", " ")

    def __init__(self):
        super().__init__()

    def ui_to_html(self, ui):
        raise NotImplementedError()

    def text_to_ui(self, text):
        raise NotImplementedError()


class JSON(TextMode):
    MIN = False

    def ui_to_html(self, ui):
        kwargs = {}
        if not self.MIN:
            kwargs["indent"] = 2
        else:
            kwargs["separators"] = (",", ":")
        as_text = ui.json(exclude_defaults=True, **kwargs)
        md = f"```json\n{as_text}\n```"
        html = markdown.markdown(md, extensions=["codehilite", "fenced_code"])
        return html

    def text_to_ui(self, text):
        return DefaultSchema.from_dict(json.loads(text, cls=JSON_serialization.Decoder))


class JSON_Min(JSON):
    MIN = True


class Dict(TextMode):
    def ui_to_html(self, ui):
        as_text = pprint.pformat(ui.dict(), indent=True)
        md = f"```python\n{as_text}\n```"
        html = markdown.markdown(md, extensions=["codehilite", "fenced_code"])
        return html

    def text_to_ui(self, text):
        # namespace = {"schema": DefaultSchema, "S": DefaultSchema}
        as_dict = eval(text)  # , namespace, namespace)
        return DefaultSchema.from_dict(as_dict)


class Python(TextMode):
    def ui_dict_to_python_code(
        self,
        ui_dict,
        schema_name,
        parent_context_name,
        lines,
        new_context_name=None,
        indent=0,
    ):
        on_indent = "    "
        indent_str = indent * on_indent

        params = ui_dict.copy()
        TYPE = params.pop("TYPE", "?!?!")
        ID = params.pop("ID", None)

        sub_params = []

        def extract_sub_params(params, sub_params, parent_name):
            if not isinstance(params, dict):
                return
            for name, value in list(params.items()):
                if isinstance(value, dict) and "TYPE" in value:
                    params.pop(name)
                    extract_sub_params(value, sub_params, name)
                    for k, v in value.items():
                        if k == "TYPE":
                            continue
                        sub_param_name = name + "." + k
                        if parent_name is not None:
                            sub_param_name = parent_name + "." + sub_param_name
                        sub_params.append(
                            (sub_param_name.count("."), sub_param_name, v)
                        )

        extract_sub_params(params, sub_params, None)

        def erepr(v):
            if isinstance(v, _EnumMixin):
                return "Enums." + str(v)
            return repr(v)

        ID_arg = ""
        if ID is not None:
            ID_arg = f"{ID!r}"
        children = params.pop("children", [])
        kwargs_str = ""
        if params:
            kwargs_str = ", ".join(f"{k}={erepr(v)}" for k, v in params.items())
            if ID is not None:
                kwargs_str = ", " + kwargs_str
        if children or sub_params:
            new_context_name = new_context_name or TYPE.lower()
            lines.append(
                f"{indent_str}with {schema_name}.{TYPE}({ID_arg}{kwargs_str}) as {new_context_name}:"
            )
            for rank, name, value in sorted(sub_params):
                lines.append(
                    f"{indent_str}{on_indent}{new_context_name}.{name} = {erepr(value)}"
                )
            for component in children:
                self.ui_dict_to_python_code(
                    component, schema_name, new_context_name, lines, None, indent + 1
                )
        else:
            lines.append(f"{indent_str}{schema_name}.{TYPE}({ID_arg}{kwargs_str})")
        return "\n".join(lines)

    def ui_to_html(self, ui):
        lines = []
        self.ui_dict_to_python_code(
            ui.dict(exclude_defaults=True), "S", None, lines, "UI", 0
        )
        as_text = "\n".join(lines)
        md = f"```python\n{as_text}\n```"
        html = markdown.markdown(md, extensions=["codehilite", "fenced_code"])
        return html

    def text_to_ui(self, text):
        namespace = {"schema": DefaultSchema, "S": DefaultSchema, "Enums": Enums}
        exec(text, namespace, namespace)
        UI = namespace["UI"]
        return UI


class TextView(QtWidgets.QWidget):
    def __init__(self, parent, editor):
        super().__init__(parent)
        self.editor = editor

        self._modes = [JSON(), Python(), JSON_Min()]
        self._mode_index = 0  # will be incremented a the end of __init__ to sync stuff.

        lo = QtWidgets.QVBoxLayout()
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)
        self.setLayout(lo)

        top_lo = QtWidgets.QHBoxLayout()
        lo.addLayout(top_lo)

        b = QtWidgets.QPushButton(self)
        b.setText("<")
        b.clicked.connect(self.send_to_component_view)
        top_lo.addWidget(b)

        self._mode_button = QtWidgets.QPushButton(self)
        self._mode_button.clicked.connect(self.toggle_mode)
        top_lo.addWidget(self._mode_button)

        b = QtWidgets.QPushButton(self)
        b.setText(">")
        b.clicked.connect(self.send_to_render_view)
        top_lo.addWidget(b)

        self._te = QtWidgets.QTextEdit(self)
        lo.addWidget(self._te)
        doc = self._te.document()
        doc.setDefaultStyleSheet(pygments.formatters.HtmlFormatter().get_style_defs())
        self._te.setAcceptRichText(False)
        self._te.setWordWrapMode(QtGui.QTextOption.NoWrap)
        # self._te.textChanged.connect(self._on_text_changed)

        self.toggle_mode()

    # def _on_text_changed(self):
    #     self.validate_text()

    def toggle_mode(self):
        UI = self.get_ui()
        self._mode_index = (self._mode_index + 1) % len(self._modes)
        self._mode_button.setText(self._get_mode().label())
        if UI is not None:
            self.load_ui(UI)

    def _get_mode(self) -> TextMode:
        return self._modes[self._mode_index]

    def load_ui(self, ui):
        self._te.clear()
        html = self._get_mode().ui_to_html(ui)
        self._te.setHtml(html)

    def get_ui(self):
        text = self._te.toPlainText()
        if not text.strip():
            return None
        return self._get_mode().text_to_ui(text)

    def send_to_component_view(self):
        self.editor._components_view.load_ui(self.get_ui())

    def send_to_render_view(self):
        ui = self.get_ui()
        self.editor._render_view.render(ui)
