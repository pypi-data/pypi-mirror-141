from ...render_context import RenderContext
from ..renderer import QtRenderer


@QtRenderer.register
def PrintStatesButton(context: RenderContext, params={}):

    S = QtRenderer.schema
    with S.Group(namespace="__debug__") as content:
        with S.Button() as b:
            b.label = "[ Print States ]"
            b.action_key = "print_states"
            S.Handle(
                key="print_states",
                action="clicked",
                script="import pprint; pprint.pprint(renderer.get_states(), indent=True)",
            )
    context.render(content)


@QtRenderer.register
def PrintContextButton(context: RenderContext, params={}):

    S = QtRenderer.schema
    with S.Group(namespace="__debug__") as content:
        with S.Button() as b:
            b.label = "[ Print Context ]"
            b.action_key = "print_context"
            S.Handle(key="print_context", action="clicked", script="context.pprint()")

    context.render(content)
