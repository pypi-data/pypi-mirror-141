from functools import reduce
import json

from .enums import Enums, JSON_ENCODE_TAG


class JSON:
    class Encoder(json.JSONEncoder):
        """
        Uses `obj.__json__` for serialization.
        """

        def default(self, obj):
            try:
                return obj.__json__()
            except Exception:
                return json.JSONEncoder.default(self, obj)

    class Decoder(json.JSONDecoder):
        """
        Deserializes _Enum and _Flag from
        """

        def decode(self, s):
            object = super().decode(s)
            return self.decode_enums(object)

        @classmethod
        def decode_enums(cls, value):
            if isinstance(value, dict):
                for k, v in value.items():
                    value[k] = cls.decode_enums(v)
                return value
            elif isinstance(value, list):
                return [cls.decode_enums(i) for i in value]

            try:
                before_tag, as_string = value.split(JSON_ENCODE_TAG, 1)
            except (AttributeError, ValueError, TypeError):
                return value
            else:
                if before_tag:
                    return value
                name, member = as_string.split(".")
                enum_type = getattr(Enums, name)
                # Flags may be a list of ored values, rebuild it:
                ored = lambda a, b: a | b  # noqa: E731
                # NB: this does nothing if there's no | in member, so we're
                # cool with Enum (not Flags) too:
                return reduce(ored, (enum_type[m] for m in member.split("|")))


def test():
    test_values = (
        Enums.Orientation.VERTICAL,
        Enums.Alignment.LEFT,
        Enums.Alignment.LEFT | Enums.Alignment.TOP,
        [Enums.Orientation.VERTICAL, Enums.Orientation.HORIZONTAL],
        dict(
            orientation=Enums.Orientation.VERTICAL,
            align=Enums.Alignment.RIGHT,
            valign=Enums.Alignment.VCENTER,
        ),
    )

    for v in test_values:
        print("=============")
        print("    ", v)

        s = json.dumps(v, cls=JSON.Encoder)
        print("    ", s)

        d = json.loads(s, cls=JSON.Decoder)
        print("    ", d)

        equ = v == d
        idt = v is d
        print("Equality:", v == d and "Ok" or "!!! NOPE !!!")
        print("Identity:", v is d and "Ok" or "Nope :/")
        if not equ:
            raise AssertionError("should be equal")
        if not idt:
            print("! Not identic, is it Ok ?")


if __name__ == "__main__":
    test()
