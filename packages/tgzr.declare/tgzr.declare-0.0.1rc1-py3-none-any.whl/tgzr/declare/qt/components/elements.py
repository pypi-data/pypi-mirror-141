import pygments.formatters
import markdown as markdown_lib

from ...render_context import RenderContext
from ..renderer import QtRenderer
from ._qt_utils import make_widget_property


@QtRenderer.register
def Label(context: RenderContext, params: QtRenderer.schema.Label):
    def get_format(context):
        label = context["widget"]
        value = getattr(label, "_prop_format", None)
        return value

    def set_format(context, value):
        label = context["widget"]
        label._prop_format = value
        context.touch_property("text")

    def set_text(context, value):
        label = context["widget"]
        label._prop_text = value
        format = get_format(context)
        if format is not None:
            value = format.format(text=value)
        else:
            value = str(value)
        label.setText(value)

    def get_text(context):
        label = context["widget"]
        value = getattr(label, "_prop_text", "")
        return value

    # classic properties
    context.register_property("format", get_format, set_format)
    context.register_property("text", get_text, set_text)

    # qt auto properties
    make_widget_property("word_wrap", bool, context, qproperty_name="wordWrap")
    make_widget_property("fixed_width", int, context, qproperty_name="fixedWidth")

    # create widget and setup property value
    with params.widget as widget:
        widget.widget_class = "QLabel"
        QtRenderer.schema.set_or_bind(
            context,
            property_name="format",
            param=params.format,
            default=None,
        )
        QtRenderer.schema.set_or_bind(
            context,
            property_name="text",
            param=params.text,
            default=params.ID or "Label",
        )
        QtRenderer.schema.set_or_bind(
            context,
            property_name="word_wrap",
            param=params.word_wrap,
            default=False,
        )
        if params.fixed_width is not None:
            # TODO: is -1 really the right default for this ?!
            QtRenderer.schema.set_or_bind(
                context,
                property_name="fixed_width",
                param=params.fixed_width,
                default=-1,
            )
    context.render(widget)


@QtRenderer.register
def Text(context: RenderContext, params: QtRenderer.schema.Text):
    with QtRenderer.schema.cast_model(params, Label) as label:
        label.word_wrap = True
    context.render(label)


@QtRenderer.register
def H1(context: RenderContext, params: QtRenderer.schema.H1):
    with QtRenderer.schema.cast_model(params, Label) as label:
        label.format = "<H1>{text}</H1>"
    context.render(label)


@QtRenderer.register
def H2(context: RenderContext, params: QtRenderer.schema.H1):
    with QtRenderer.schema.cast_model(params, Label) as label:
        label.format = "<H2>{text}</H2>"
    context.render(label)


@QtRenderer.register
def H3(context: RenderContext, params: QtRenderer.schema.H1):
    with QtRenderer.schema.cast_model(params, Label) as label:
        label.format = "<H3>{text}</H3>"
    context.render(label)


@QtRenderer.register
def H4(context: RenderContext, params: QtRenderer.schema.H1):
    with QtRenderer.schema.cast_model(params, Label) as label:
        label.format = "<H4>{text}</H4>"
    context.render(label)


@QtRenderer.register
def Markdown(context: RenderContext, params: QtRenderer.schema.Markdown):
    context["_md"] = ""

    def get_md(context):
        return context["_md"]

    def set_md(context, md):
        context["_md"] = md
        te = context["widget"]
        doc = te.document()
        doc.setDefaultStyleSheet(
            pygments.formatters.HtmlFormatter(style="colorful").get_style_defs()
        )
        html = markdown_lib.markdown(md, extensions=["codehilite", "fenced_code"])
        te.setHtml(html)

    context.register_property("md", get_md, set_md)

    with params.widget as te:
        te.widget_class = "QTextEdit"
        QtRenderer.schema.set_or_bind(context, "md", params.text, "")

    te = context.render(te)["widget"]
    te.setReadOnly(True)
    if params.min_width is not None:
        te.setMinimumWidth(params.min_width)
    if params.min_height is not None:
        te.setMinimumHeight(params.min_height)
