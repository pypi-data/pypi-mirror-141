import json

from ..serialization import JSON
from . import Collection, ComponentModel


class RootSchema(Collection):
    """
    Base class for all schemas.

    Schemas are namespaces containing component param models:
    ```
    class MySchema(ParentSchema):
        SomeComponent = other_schema.SomeComponent
        MyComponent = MyComponent
        ...

    It is used by renderers to assert they support a whole set of
    component, and prevent registration of render functions for
    un-supported components.

    Two renderers using the same schema are compatible.

    Schemas inherit other schemas to include the component from
    thoses schemas.

    ```


    """

    @classmethod
    def params_models(cls):
        ret = []
        for name in dir(cls):
            if name.startswith("_"):
                continue
            object = getattr(cls, name)
            # There is a (nasty) bug in pydantic preventing the use
            # of issubclass, so I go the poor way with __mro__:
            try:
                mro = object.__mro__
            except AttributeError:
                continue

            if ComponentModel in mro:
                ret.append((name, object))
        return ret

    @classmethod
    def cast_model(cls, model, to_type):
        src = model.copy()
        src.TYPE = to_type.__name__
        return cls.from_dict(src.dict())

    @classmethod
    def from_json(cls, json_string):
        return cls.from_dict(json.loads(json_string, cls=JSON.Decoder))

    @classmethod
    def from_dict(cls, d, passtru_non_ui=False):
        # There should be a nice and easy pydantic way to do this, but I can't find it :/

        try:
            TYPE = d["TYPE"]
        except (TypeError, KeyError):
            if passtru_non_ui:
                return d
            raise Exception(
                f"Error building UI from dict: no 'TYPE' key (keys were: {[k for k in d.keys()]})."
            )
        try:
            component_type = getattr(cls, TYPE)
        except AttributeError:
            raise Exception(
                f"Error building UI from dict: unkown root component '{TYPE}'."
            )

        component = component_type()
        for name in component_type.__fields__.keys():
            default = getattr(component, name)
            value = d.get(name, default)
            if isinstance(value, (list, tuple)):
                value = [cls.from_dict(i, True) for i in value]
            elif value is not None and name not in ("ID", "TYPE"):
                value = cls.from_dict(value, passtru_non_ui=True)
            setattr(component, name, value)

        return component
