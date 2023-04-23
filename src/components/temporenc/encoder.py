from temporenc import temporenc
from type_ext.temporenc_arg_dict import TemporencArgDict


class Encoder:

    # TODO: NEXT - encode_iso_str
    @classmethod
    def encode_arg_dict(cls, arg_dict: TemporencArgDict) -> str:
        """
        Encodes arg_dict as an uppercase hexadecimal string.

        :param arg_dict: {TemporencArgDict} dictionary of arguments to encode

        :return: {str} an uppercase hexadecimal string.
        """
        # Prefer greater precision
        if ((arg_dict["millisecond"] is not None and
             arg_dict["microsecond"] is not None) or
                (arg_dict["millisecond"] is not None and
                 arg_dict["nanosecond"] is not None)):
            arg_dict["millisecond"] = None
        if arg_dict["tz_offset"] is not None:
            arg_dict["hour"] += int(arg_dict["tz_offset"] / 60)
            arg_dict["minute"] += arg_dict["tz_offset"] % 60
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
