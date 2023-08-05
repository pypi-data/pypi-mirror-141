from .render_context import RenderContext
from .state_store import StateStore


class Renderer(object):
    schema = None
    _renderers = {}

    #
    #   TOOLS
    #
    @classmethod
    def ui_from_json(cls, json_string):
        return cls.schema.from_json(json_string)

    @classmethod
    def ui_from_dict(cls, d):
        return cls.schema.from_dict(d)

    #
    #   RENDERERS
    #
    @classmethod
    def register(cls, func):
        """
        Decorator to set the renderer to use with the
         model in schema having the same name.

        The decorated func must accept two arguments:
            renderer(context: RenderContext, params: <the_renderer_model>)

        """
        renderer = func
        name = func.__name__
        try:
            model = getattr(cls.schema, name)
        except AttributeError:
            raise AttributeError(
                f"Error registering renderer {renderer}: the schema {cls.schema} does not have a model named {name!r}."
            )
        cls._renderers[model] = renderer
        return renderer

    @classmethod
    def get_renderer(cls, component_type):
        model = getattr(cls.schema, component_type)
        return cls._renderers[model]

    @classmethod
    def assert_schema_complete(cls):
        # TODO: maybe assert renderer signature too ?
        missing = set()
        for name, params in cls.schema.params_models():
            try:
                cls._renderers[params]
            except KeyError:
                missing.add(name)
        if missing:
            raise Exception(
                f"The renderer {cls} is missing support for {missing} components !"
            )

    #
    #   INIT
    #
    def __init__(self, host, check_schema=True):
        super().__init__()
        if check_schema:
            self.assert_schema_complete()
        self._root_context_items = dict()
        self.update_root_context(renderer=self)
        self.set_host(host)
        self._state_store = StateStore()
        self._handlers = {}

    #
    #   RENDERER
    #
    def set_host(self, host):
        self.update_root_context(
            widget=host,
            root_widget=host,
            layout_parent=host,
        )

    def update_root_context(self, **name_values):
        self._root_context_items.update(**name_values)

    def create_root_context(self):
        context = RenderContext.create_root_context(**self._root_context_items)
        return context

    def render(self, ui, parent_context=None):
        if parent_context is None:
            # We are rendering the root UI here, let's clean up previous render data:
            parent_context = self.create_root_context()
            self._state_store.clear_bindings()

        params = ui
        TYPE = params.TYPE
        ID = params.ID
        # print("--> rendering", TYPE)

        try:
            model = getattr(self.schema, TYPE)
        except Exception:
            # print("=============")
            # pprint.pprint(ui.dict(), indent=True)
            # print("=============")
            raise
        renderer = self._renderers[model]

        with parent_context(TYPE=TYPE, ID=ID) as sub_context:
            renderer(context=sub_context, params=params)
        return sub_context

    #
    #   ACTIONS
    #
    def set_handler(self, handler, key=None, action=None):
        self._handlers[(key, action)] = handler

    def perform_action(self, key, action, context, *args, **kwargs):
        # TODO: store a list instead of a single handler and trigger until one of them
        # doen't return True ?
        # => No, action namespace set by  the Group component should be enough.
        try:
            handler = self._handlers[(key, action)]
        except KeyError:
            try:
                handler = self._handlers[(key, None)]
            except KeyError:
                try:
                    handler = self._handlers[(None, action)]
                except KeyError:
                    try:
                        handler = self._handlers[(None, None)]
                    except KeyError:
                        handler = self._default_handler
        handler(self, key, action, context, *args, **kwargs)

    def _default_handler(self, renderer, action_key, action_type, *args, **kwargs):
        print(
            f"!! Warning !! Action not handled: type={action_type!r}, key={action_key!r}"
        )

    #
    #   STATES
    #

    def bind_state(self, state_key, update_callback, *default):
        """
        Returns an updater and and a setter for the state at `state_key`.

        The updater is callable without argument. It will fetch the state
        value and call `update_callback(state_value)` with it.

        The setter is a callable with one argument. It will store
        the argument as the new state, which will trigger all updaters
        for this value.
        """
        # TODO: see why we still have *default, is it usefull since nobody seams to uses it ?
        updater, setter = self._state_store.bind(state_key, update_callback, *default)
        return updater, setter

    def get_state(self, key, *default):
        return self._state_store.get(key, *default)

    def get_states(self, prefix=None, strip_prefix=True):
        return self._state_store.get_namespace(prefix=prefix, strip_prefix=strip_prefix)

    def update_states(self, values):
        return self._state_store.update(values)
