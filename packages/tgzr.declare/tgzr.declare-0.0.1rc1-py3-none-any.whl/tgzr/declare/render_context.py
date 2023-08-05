from functools import partial
from contextlib import contextmanager


class RenderContext(object):
    @classmethod
    def create_root_context(cls, renderer, **overrides):
        overrides["renderer"] = renderer
        return cls(None, overrides)

    def __init__(self, parent_context, overrides):
        self._parent_context = parent_context
        self._overrides = {}
        # use __setitem__ so that we only store
        # new values:
        for name, value in overrides.items():
            self[name] = value

    #
    #   PROPERTIES
    #
    def register_property(self, property_name, getter, setter):
        """
        Registers the setter and the getter for a property with the given name.
        Their signature must be like:
            `getter(context)`
            `setter(context, value)`
        The context parameter will receive the context in which the property was
        registered.

        Raises a ValueError if such a property has already been registered
        in this context. (Note that properties declared in parent context(s) are
        overridable, only the current context forbids registering on an existing
        property name.)

        """
        try:
            properties = self._overrides["__properties__"]
        except KeyError:
            properties = {}
            self._overrides["__properties__"] = properties

        if property_name in properties:
            raise ValueError("Property override is not allowed !!!")

        properties[property_name] = (getter, setter)

    def _find_property(self, property_name):
        """
        Returns the getter and the setter for the given property name.

        The lookup is delegated to the parent context if this no such
        property was registered in this context.

        Raise KeyError if no property with this name has been registered
        in this context and the parent contexts.
        """
        try:
            # Wow ! that actually the first time in my life I have
            # two lines inside a try, and it make complete sens !!! \o/
            # Achievment unlocked ^^
            # (Hint: both lines would raise a KeyError, so I can merge the two `try` statements)
            properties = self._overrides["__properties__"]
            return properties[property_name]
        except KeyError:
            if self._parent_context is None:
                raise KeyError(f'Could not find property "{property_name}".')
            return self._parent_context._find_property(property_name)

    def get_property(self, property_name):
        """
        Returns the value of this property.
        """
        getter, _ = self._find_property(property_name)
        return getter(self)

    def set_property(self, property_name, value):
        """
        Change the value of this property.
        """
        _, setter = self._find_property(property_name)
        setter(self, value)

    def touch_property(self, property_name):
        getter, setter = self._find_property(property_name=property_name)
        setter(self, getter(self))

    def bind_property(self, property_name, state_key):
        """
        Triggers a update of a property when the given state changes.
        """
        _, setter = self._find_property(property_name)
        self.bind_state(state_key, partial(setter, self))

    #
    #   STATES
    #

    def bind_state(self, state_key, update_callback, *default):
        """
        Calls the given callback when the given state changes.
        """
        return self["renderer"].bind_state(state_key, update_callback, *default)

    def set_state(self, name, value):
        self["renderer"].update_states({name: value})

    def get_state(self, name, *default):
        return self["renderer"].get_state(name, *default)

    def get_states(self, prefix=None, strip_prefix=True):
        return self["renderer"].get_states(prefix, strip_prefix)

    #
    #   ACTIONS
    #
    def get_handler(self, key, action="action"):
        """
        Returns a callable without argument that will
        perform the action.
        """
        renderer = self["renderer"]
        return partial(renderer.perform_action, key, action, self)

    #
    #   RENDER
    #
    def render_children(self, children, **context_overrides):
        renderer = self["renderer"]
        with self(INFO="children_context", **context_overrides) as context:
            for child in children:
                renderer.render(child, context)

    def render(self, ui):
        return self["renderer"].render(ui, self)

    #
    #   DATA
    #

    @contextmanager
    def __call__(self, **overrides):
        yield RenderContext(self, overrides)

    def __getitem__(self, name):
        try:
            return self._overrides[name]
        except KeyError:
            if self._parent_context is None:
                raise
            return self._parent_context[name]

    def __setitem__(self, name, value):
        try:
            parent_value = self._parent_context[name]
        except (TypeError, KeyError):
            # parent is None, or parent doesn't have this key
            pass
        else:
            if parent_value == value:
                try:
                    del self._overrides[name]
                except KeyError:
                    pass
                return
        self._overrides[name] = value

    def get(self, name, *default):
        try:
            return self[name]
        except KeyError:
            if default:
                return default[0]
            return None

    #
    #   TOOLS
    #

    def pprint(self, indent=0, overridden=None):
        """
        Prints the values in the context and parent context(s),
        with an arrow pointing a the final value (the ones
        returned when accessed thru this context).
        """
        if overridden is None:
            overridden = set()
        indent_str = "    "
        space = indent * indent_str
        print(f"{space}=== Context ===")
        for name, value in sorted(self._overrides.items()):
            r = repr(value)[:40]
            if name == "__properties__":
                r = "{" + ", ".join([repr(i) + ":..." for i in value.keys()]) + "}"
            f = "   "
            if name not in overridden:
                f = "-> "
                overridden.add(name)
            print(f"{space}{f}{name} = {r}")
        if self._parent_context is not None:
            self._parent_context.pprint(indent + 1, overridden)
