import traceback
from ..render_context import RenderContext
from .renderer import BaseRenderer


@BaseRenderer.register
def Group(context: RenderContext, params: BaseRenderer.schema.Group):

    children_overrides = dict()

    namespace = params.namespace or params.ID
    # print(
    #     "================================== +",
    #     namespace,
    #     params.affect_actions,
    #     params.affect_states,
    # )
    if namespace:
        if params.affect_actions:
            # print("================ ACTION+", namespace)
            children_overrides.update(
                BaseRenderer.schema._namespaces.make_action_namespace(
                    context, namespace
                )
            )
        if params.affect_states:
            # print("================ STATE+", namespace)
            children_overrides.update(
                BaseRenderer.schema._namespaces.make_state_namespace(context, namespace)
            )

    context.render_children(params.children, **children_overrides)


@BaseRenderer.register
def Bind(context: RenderContext, params: BaseRenderer.schema.Bind):
    # Support Group namespaces:
    state_key = BaseRenderer.schema._namespaces.get_state_key(context, params.state_key)
    # print("BINDING", params.property_name, "TO", state_key)
    context.bind_property(property_name=params.property_name, state_key=state_key)

    # just in case:
    context.render_children(params.children)


@BaseRenderer.register
def Handle(context: RenderContext, params: BaseRenderer.schema.Handle):
    """
    Define an action handler directly in the ui declaration.

    The python code in `script` will be executed when an
    action of type `action` with the key `key` is triggered.

    This code can access this local values:

        - `renderer`: the renderer on which the action is triggered.
        - `context`: the context in which this component was renderer.
        - `key`: the action key.
        - `action`: the action type.
        - `args` and `kwargs`: the opionnal extra args and keyword args sent to the action
        - `get_state(name[, default])`: a function to get the value of a state
        - `set_state(name, value)`: a function to set a state

    """
    if params.action is None:
        raise ValueError("Cannot handle action without `action` parameter !")

    def component_handler(renderer, key, action, context, *args, **kwargs):
        # TODO: get ride of the renderer here, it's not needed now that we added the context
        # (and make context the first arg)
        def set_state(name, value):
            context.set_state(name, value)

        def get_state(name, *default):
            return context.get_state(name, *default)

        def get_states(prefix=None, strip_prefix=True):
            return context.get_states(prefix, strip_prefix)

        env = {}
        env["locals"] = None
        env["globals"] = None
        env["__name__"] = None
        env["__file__"] = None
        # env["__builtins__"] = None
        env["print"] = print
        env["renderer"] = renderer
        env["key"] = key
        env["action"] = action
        env["context"] = context
        env["args"] = args
        env["kwargs"] = kwargs
        env["get_state"] = get_state
        env["get_states"] = get_states
        env["set_state"] = set_state
        try:
            exec(params.script, env, env)
        except Exception:
            traceback.print_exc()
            print(
                f"!! CRITIAL !! Error while handling Action in handler component {context['ID']}:",
                key,
                action,
            )
            print("!! CRITICAL !! Script was: \n" + params.script)

    action = BaseRenderer.schema._namespaces.get_action_name(context, params.action)
    context["renderer"].set_handler(component_handler, params.key, action)


@BaseRenderer.register
def Set(context: RenderContext, params: BaseRenderer.schema.Set):
    context.set_property(
        params.name,
        params.value,
    )

    # just in case:
    context.render_children(params.children)


@BaseRenderer.register
def States(context: RenderContext, params: BaseRenderer.schema.States):

    group = BaseRenderer.schema.Group(
        namespace=params.namespace or params.ID,
        affect_actions=False,
        affect_states=True,
    )
    group.children += params.children
    context.render(group)


@BaseRenderer.register
def State(context: RenderContext, params: BaseRenderer.schema.State):
    name = params.name or params.ID
    if name is None:
        raise ValueError(
            "No `name` nor `ID` given for `State` component, cannot update state."
        )

    name = BaseRenderer.schema._namespaces.get_state_key(context, name)
    # /!\ This is peculiar: we are rendering children first because `set_state`
    # should be called only once the state value is finilized. See comment in the list_state
    # component for more on this...
    context.render_children(params.children)
    context.set_state(name, params.value)


@BaseRenderer.register
def ListState(context: RenderContext, params: BaseRenderer.schema.ListState):
    # We use to create a list, set it as stat value, and let child components
    # add the value to the list directly.
    # But adding a value to the list does not trigger the state update callback
    # so we need to build the complete list first, and only then set it as the state.
    # (This has the advantage to trigger updates only when the list is complete instead
    # of triggering updates everytime an item is added to the list)

    name = params.name or params.ID
    list_state = []
    context["list_state"] = list_state
    context.render_children(params.children, list_state=list_state)

    # Support already existing value:
    # (user should use the State component to clear the list if they
    # only want new items.)
    print("+ ", params.name, list_state)
    get_name = BaseRenderer.schema._namespaces.get_state_key(context, name)
    value = context.get_state(get_name, [])
    value += list_state

    state = BaseRenderer.schema.State(name=name, value=value)
    context.render(state)


@BaseRenderer.register
def ListStateAppend(
    context: RenderContext, params: BaseRenderer.schema.ListStateAppend
):
    value = params.value or params.ID
    list_state = context["list_state"]
    list_state.append(value)
    context.render_children(params.children)
