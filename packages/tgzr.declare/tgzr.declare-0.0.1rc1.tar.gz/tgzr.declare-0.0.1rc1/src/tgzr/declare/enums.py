import enum as _enum  # avoid puluting this namespace


JSON_ENCODE_TAG = "@Enum:"


class _EnumMixin:
    def is_enum(self):
        return True

    def _generate_next_value_(name, start, count, last_values):
        return name

    def __json__(self):
        return f"{JSON_ENCODE_TAG}{str(self)}"


class _Enum(_EnumMixin, _enum.Enum):
    pass


class _Flag(_EnumMixin, _enum.Flag):
    pass


class Enums:
    class Orientation(_Enum):
        VERTICAL = _enum.auto()
        HORIZONTAL = _enum.auto()

    class Alignment(_Flag):
        LEFT = _enum.auto()
        RIGHT = _enum.auto()
        HCENTER = _enum.auto()
        TOP = _enum.auto()
        BOTTOM = _enum.auto()
        VCENTER = _enum.auto()
