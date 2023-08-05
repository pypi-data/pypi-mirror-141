from collections import defaultdict
from copy import deepcopy


class StateStore(object):
    def __init__(self):
        super(StateStore, self).__init__()
        self._data = dict()
        self._bindings = defaultdict(list)

    def clear_bindings(self):
        self._bindings.clear()

    def add_binding(self, key, update_callback):
        self._bindings[key].append(update_callback)

    def get_bindings(self, key):
        return self._bindings[key]

    def bind(self, key, update_callback, *default):
        # TODO: see why we still have *default, is it usefull since nobody seams to uses it ?
        self._bindings[key].append(update_callback)

        def updater():
            try:
                state = self.get(key, *default)
            except KeyError:
                print(
                    f"!! Warning !! Could not get binded state {key} without default value."
                )
                pass
            else:
                # trigger an update on all binders:
                for cb in self._bindings[key]:
                    cb(state)

        def setter(state):
            self.update({key: state})

        # If a state already exists, send its value to this callback:
        # (only this one, avoid update everyone everytime someone registers !)
        try:
            value = self.get(key)
        except KeyError:
            pass
        else:
            update_callback(value)

        return updater, setter

    def __getitem__(self, key):
        return self._data[key]

    def get(self, key, *default):
        if default:
            return self._data.get(key, *default)
        else:
            return self[key]

    def get_namespace(self, prefix=None, strip_prefix=True):
        if prefix is None:
            # Return a copy ! set and get should only happen thru us
            # in order to trigger the callbacks.
            return deepcopy(self._data)

        if strip_prefix:
            prefix_len = len(prefix)
        else:
            prefix_len = 0
        states = {}
        for k, v in self._data.items():
            if k.startswith(prefix):
                states[k[prefix_len:]] = v  # FIXME: we should deepcopy `v` too !!!!
        return states

    def update(self, mapping):
        for k, v in mapping.items():
            self._data[k] = v
            try:
                update_callbacks = self._bindings[k]
            except KeyError:
                print(f"!! Warning !! Updating state with no binding: {k}")
            else:
                # Use `get()` because subclasses may
                # altered the value in __setitem__:
                value = self.get(k)
                for update_callback in update_callbacks:
                    update_callback(value)
