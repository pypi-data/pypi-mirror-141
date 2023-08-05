from typing import Union, Optional, Any, List

from ..models import ComponentModel, Binded
from ..enums import Enums
from ..models.root_schema import RootSchema


class NamespaceManager(object):
    """
    Utility to deal with state and action namespaces.
    """

    _NAMESPACE_SEP = "/"
    _ACTION_NAMESPACE_VAR = "action_namespace"
    _STATE_NAMESPACE_VAR = "state_namespace"

    def make_action_namespace(self, context, namespace):
        """
        Returns a dict of overrides to use in sub-contexts for them
        to have an additionnal action namespace `namespace`.
        """
        parent_namespace = context.get(self._ACTION_NAMESPACE_VAR, None)
        if parent_namespace:
            namespace = parent_namespace + self._NAMESPACE_SEP + namespace
        return {self._ACTION_NAMESPACE_VAR: namespace}

    def make_state_namespace(self, context, namespace):
        """
        Returns a dict of overrides to use in sub-contexts for them
        to have an additionnal state namespace `namespace`.
        """
        parent_namespace = context.get(self._STATE_NAMESPACE_VAR, None)
        if parent_namespace:
            namespace = parent_namespace + self._NAMESPACE_SEP + namespace
        return {self._STATE_NAMESPACE_VAR: namespace}

    def get_action_name(self, context, action_name):
        ns = context.get(self._ACTION_NAMESPACE_VAR, None)
        if ns is not None:
            action_name = ns + self._NAMESPACE_SEP + action_name
        return action_name

    def get_state_key(self, context, state_key):
        if state_key is None:
            return None
        ns = context.get(self._STATE_NAMESPACE_VAR, None)
        if ns is not None:
            state_key = ns + self._NAMESPACE_SEP + state_key
        return state_key


class Group(ComponentModel):
    """
    A Group of components.

    Use the `namespace` param to affect state keys and/or action names
    of all sub-components.
    """

    namespace: str = None
    affect_states: bool = True
    affect_actions: bool = True


class Set(ComponentModel):
    """
    Sets the value of a property.
    """

    name: str = None
    value: Union[
        bool, int, float, str, List, Enums.Orientation, Enums.Alignment, None
    ] = None


class Bind(ComponentModel):
    """
    Binds a component property to a state.
    """

    # TODO: Shouldnt we get ride of this (which doesnt work) since we have the Binded param stuff ?
    property_name: str = None
    state_key: str = None


class Handle(ComponentModel):
    """
    Runs a python script when an action is triggerer.
    """

    script: str = None
    key: str = None
    action: str = None


class Include(ComponentModel):
    """
    Includes UI as declared in a state.
    """

    source_state: str = None
    trigger_state: str = None


class States(ComponentModel):
    """
    Adds a namespace to all `State` sub-components.
    """

    namespace: Optional[str] = None


class State(ComponentModel):
    """
    Sets a value in the state store.
    """

    name: str = None
    value: Any = None


class ListState(ComponentModel):
    """
    Adds all `ListStateAppend` chidren value to a state in the state store.

    If the state under `name` already exists and is a list, the values
    from the child components will be appended.

    In other cases, the state value is overwritten with a list of all sub-components values.
    """

    name: str = None


class ListStateAppend(ComponentModel):
    """
    Adds a value to the first `ListState` ancestor.
    """

    value: Any = None


class Utils:
    Group = Group
    Binded = Binded
    Handle = Handle
    Set = Set
    Bind = Bind
    Include = Include

    _namespaces = NamespaceManager()


class StateTools:
    States = States
    State = State
    ListState = ListState
    ListStateAppend = ListStateAppend


class BaseSchema(Utils, StateTools, RootSchema):
    """
    The BaseSchema contains all component needed to be supported by all
    renderers.
    """

    @classmethod
    def set_or_bind(
        cls,
        context,
        property_name,
        param,
        default=None,
        SetComponent=None,
        BindComponent=None,
    ):
        """
        This helper will create a Bind component or a Set component depending
        on params (if params.value.state_key exists, bind to this state. Only set the property
        in other case.) and return the state_key used for binding or None.


        I.e.: This handles Component parameters of type `tgzr.declare.models.property.Bindable*`

        You must use it in a component context:
        ```
            with SomeComponent():
                Schema.set_or_bind(context, 'value', params.value)
        ```

        The SetComponent and BindComponent respectively default to the `Set` and `Bind`
        components is this Schema.
        """
        do_bind = True
        try:
            state_key = param.state_key
        except AttributeError:
            value = param
            if param is None:
                value = default
            auto_bind_prefix = "@binded:"
            if isinstance(value, str) and value.lower().startswith(auto_bind_prefix):
                state_key = value[len(auto_bind_prefix) :]
            else:
                do_bind = False
        else:
            try:
                value = context.get_state(state_key)
            except KeyError:
                context.set_state(state_key, default)
                value = default

        if do_bind:
            if BindComponent is None:
                BindComponent = getattr(cls, "Bind")
            BindComponent(property_name=property_name, state_key=state_key)
            return cls._namespaces.get_state_key(context, state_key)
        else:
            if SetComponent is None:
                SetComponent = getattr(cls, "Set")
            SetComponent(name=property_name, value=value)
            return None
