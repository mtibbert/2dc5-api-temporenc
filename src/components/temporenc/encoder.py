from temporenc import temporenc

from type_ext.temporenc_arg_dict import TemporencArgDict


class Encoder:

    @classmethod
    def encode_arg_dict(cls, arg_dict: TemporencArgDict) -> str:
        """
        Encodes arg_dict as an uppercase hexadecimal string.

        :param arg_dict: {TemporencArgDict} dictionary of arguments to encode

        :return: {str} an uppercase hexadecimal string.
        """
        if (arg_dict["microsecond"] is not None and
                arg_dict["millisecond"] is not None):
            pass
        if (arg_dict["microsecond"] is not None and
                arg_dict["nanosecond"] is not None):
            pass
        if (arg_dict["millisecond"] is not None and
                arg_dict["nanosecond"] is not None):
            pass
        hex_str = temporenc.packb(
            value=arg_dict["value"],
            type=arg_dict["type"],
            year=arg_dict["year"],
            month=arg_dict["month"],
            day=arg_dict["day"],
            hour=arg_dict["hour"],
            minute=arg_dict["minute"],
            second=arg_dict["second"],
            millisecond=arg_dict["millisecond"],
            microsecond=arg_dict["microsecond"],
            nanosecond=arg_dict["nanosecond"],
            tz_offset=arg_dict["tz_offset"]).hex()
        return hex_str.upper()
