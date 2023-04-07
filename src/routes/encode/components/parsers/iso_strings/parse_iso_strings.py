import re
from src.types.precision_type import PrecisionType


class Parse:

    @classmethod
    def tz_aware_iso_string(cls, iso: str) -> dict:
        meta = cls._get_meta(iso)
        return meta

    @classmethod
    def _get_meta(cls, iso):
        has_date_time = "T" in iso
        is_precise = "." in iso
        is_tz_aware = False
        if has_date_time:
            is_tz_aware = re.search(r"[+-]", iso.split("T")[1]) is not None
        date_component = cls._date_2_dict(iso.split("T")[0])
        precision_component = cls._subsecond_from_iso(iso)
        time_component = cls._time_2_dict(iso.split("T")[1][:8])
        tz_component = cls._tz_from_iso(iso)
        return {"iso": iso,
                "meta": {
                    "has_date_time": has_date_time,
                    "is_precise": is_precise,
                    "is_tz_aware": is_tz_aware
                },
                "components": {
                    "date": date_component,
                    "precision": precision_component,
                    "time": time_component,
                    "tz": tz_component
                }}

    @classmethod
    def _date_2_dict(cls, date_str):
        dict_obj = {
            "year": None,
            "month": None,
            "day": None
        }
        if "-" in date_str:
            parts = date_str.split("-")
            if len(parts) < 1 or len(parts) > 3:
                raise ValueError(f"ValueError: {date_str} - Expected string in "
                                 f"YYYY-MM-DD format")
            for idx, part in enumerate(parts):
                match idx:
                    case 0:
                        dict_obj["year"] = part
                    case 1:
                        dict_obj["month"] = part
                    case 2:
                        dict_obj["day"] = part
                    case _:
                        raise ValueError(f"{date_str} - " +
                                         f"Expected string in YYYY-MM-DD format")
        else:
            raise ValueError(f"ValueError: {date_str} - " +
                             f"Expected string in YYYY-MM-DD format")
        return dict_obj

    @classmethod
    def _subsecond_from_iso(cls, iso_str: str):
        dict_obj = {
            "precision": None,
            "subsecond": None
        }

        if len(iso_str.split(".")) == 1:
            # Subsecond separator not found
            dict_obj["precision"] = PrecisionType.PRECISION_NON_PRECISE.name
        else:
            # Strip off timezone ifo
            iso_str = iso_str[:re.search(r'\.\d+', iso_str).regs[0][1]]
            dict_obj["subsecond"] = iso_str.split(".")[1][:9]
            chars = len(dict_obj["subsecond"])
            if chars < 4:
                dict_obj["precision"] = PrecisionType.PRECISION_MICROSECOND.name
            elif chars < 7:
                dict_obj["precision"] = PrecisionType.PRECISION_MILLISECOND.name
            else:
                dict_obj["precision"] = PrecisionType.PRECISION_NANOSECOND.name
        return dict_obj

    @classmethod
    def _time_2_dict(cls, time_str):
        dict_obj = {
            "hour": None,
            "minute": None,
            "second": None
        }
        if re.search(r"^T?\d{2}:\d{2}:\d{2}(\.\d{1,9})?\+?-?", time_str) is None:
            raise ValueError(f"{time_str} - Expected string in "
                             f"HH:SS:SS format")
        if time_str.startswith("T"):
            time_str = time_str[1:9]
        else:
            time_str = time_str[:8]
        parts = time_str.split(":")
        if len(parts) < 1 or len(parts) > 3:
            raise ValueError(f"ValueError: {time_str} - Expected string in "
                             f"HH:SS:SS format")
        for idx, part in enumerate(parts):
            match idx:
                case 0:
                    dict_obj["hour"] = part
                case 1:
                    dict_obj["minute"] = part
                case 2:
                    dict_obj["second"] = part
                case _:
                    raise ValueError(f"{time_str} - " +
                                     f"Expected string in HH:SS:SS format")
        return dict_obj

    @classmethod
    def _tz_from_iso(cls, iso_str: str):
        dict_obj = {
            "direction": None,
            "hour": None,
            "minute": None,
            "offset": None,
        }

        regex = r".*([\+-]\d{2}:\d{2})$"
        matches = re.findall(regex, iso_str)
        # Expected similar to ['-06:00']
        if len(matches) > 0 and len(matches[0]) == 6:
            tz_component = matches[0]
            dict_obj = {
                "direction": tz_component[:1],
                "hour": tz_component[1:3],
                "minute": tz_component[4:],
                "tz_offset": None,
            }
            offset = f'{dict_obj["direction"]}{dict_obj["hour"]}.' +\
                     f'{int((int(dict_obj["minute"]) / 60)).__str__().zfill(2)}'
            tz_offset = f'{int(float(offset) * 60)}'
            dict_obj["tz_offset"] = tz_offset
        return dict_obj
