from type_ext import IsoDict, temporenc_arg_dict, PrecisionType
from type_ext.temporenc_arg_dict import TemporencArgDict


class Utilities:
    @classmethod
    def iso_dict_to_arg_dict(cls, iso_dict: IsoDict) -> TemporencArgDict:
        """
        Extract Temporenc encoding information from IsoDict components.

        :param iso_dict: {IsoDict}
        :return: {TemporencArgDict}
        """
        arg_dict: TemporencArgDict = temporenc_arg_dict.factory()
        if (iso_dict["components"]["date"] is not None or
                iso_dict["components"]["date"] is not None):
            if iso_dict["components"]["date"] is not None:
                arg_dict["year"] = iso_dict["components"]["date"]["year"]
                arg_dict["month"] = iso_dict["components"]["date"]["month"]
                arg_dict["day"] = iso_dict["components"]["date"]["day"]
            if iso_dict["components"]["time"] is not None:
                arg_dict["hour"] = iso_dict["components"]["time"]["hour"]
                arg_dict["minute"] = iso_dict["components"]["time"]["minute"]
                arg_dict["second"] = iso_dict["components"]["time"]["second"]
            if iso_dict["components"]["precision"] is not None:
                precision = iso_dict["components"]["precision"]["precision"]
                if precision == PrecisionType.PRECISION_NANOSECOND.name:
                    arg_dict["nanosecond"] = \
                        int(iso_dict["components"]["precision"]["subsecond"])
                    arg_dict["microsecond"] = None
                    arg_dict["millisecond"] = None
                elif precision == PrecisionType.PRECISION_MICROSECOND.name:
                    arg_dict["microsecond"] = \
                        int(iso_dict["components"]["precision"]["subsecond"])
                    arg_dict["millisecond"] = None
                    arg_dict["nanosecond"] = None
                elif precision == PrecisionType.PRECISION_MILLISECOND.name:
                    arg_dict["millisecond"] = \
                        int(iso_dict["components"]["precision"]["subsecond"])
                    arg_dict["microsecond"] = None
                    arg_dict["nanosecond"] = None
            if iso_dict["components"]["tz"]["offset"] is not None:
                arg_dict["tz_offset"] = int(iso_dict["components"]["tz"]["offset"])
        arg_dict = ({k: v for k, v in arg_dict.items() if v is None} |
                    {k: int(v) for k, v in arg_dict.items() if v is not None})
        return arg_dict
