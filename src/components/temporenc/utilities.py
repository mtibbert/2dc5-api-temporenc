from type_ext import IsoDict, temporenc_arg_dict, PrecisionType
from type_ext.temporenc_arg_dict import TemporencArgDict
from type_ext.utilities import join_dict_values
from type_ext.validators import ValidateDict


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

    @classmethod
    def iso_dict_as_iso_str(cls, iso_dict: IsoDict) -> str:
        """
        Parse iso_dict as an ISO string.

        :param iso_dict: {IsoDict} dictionary of arguments to parse

        :return: {str}
        """
        iso_str = ""
        date_str = ""
        time_str = ""
        precision_str = ""
        tz_str = ""
        if ValidateDict.validate_date_dict(iso_dict["components"]["date"]):
            date_str = join_dict_values(iso_dict["components"]["date"])
            iso_str = date_str
        if ValidateDict.validate_time_dict(iso_dict["components"]["time"]):
            time_str = join_dict_values(iso_dict["components"]["time"], ":")
            if time_str != "None" and iso_str != "":
                iso_str += f'T{time_str}'
            elif time_str != "None":
                iso_str += time_str
        if date_str == "" and time_str == "":
            # Must have date or time; return empty string
            iso_str = ""
        if date_str == "" or time_str == "":
            # TYPE_D or TYPE_T
            pass
        elif date_str != "" and time_str != "None":
            # iso_str is TYPE_DT
            precision_dict = iso_dict["components"]["precision"]
            non_precise_type = PrecisionType.PRECISION_NON_PRECISE.name
            if ValidateDict.validate_precision_dict(precision_dict):
                if precision_dict["precision"] != non_precise_type:
                    # TYPE_DTS or TYPE_DTSZ
                    precision_str = iso_dict["components"]["precision"]["subsecond"]
                    iso_str += f'.{precision_str}'
            if (not any(v is None for v in iso_dict['components']['tz'].values()) and
                    ValidateDict.validate_tz_dict(iso_dict["components"]["tz"])):
                # TYPE_DTZ or TYPE_DTSZ
                tz_str = (f'{iso_dict["components"]["tz"]["direction"]}'
                          f'{iso_dict["components"]["tz"]["hour"]}:'
                          f'{iso_dict["components"]["tz"]["minute"]}')
                iso_str += f'{tz_str}'
        return iso_str
