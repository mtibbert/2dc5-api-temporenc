import re
from type_ext import PrecisionType
from type_ext import DateDict, IsoDict, PrecisionDict, TimeDict, TzDict
from type_ext.validators import ValidateDict


class Parse:

    @classmethod
    def iso_to_iso_dict(cls, iso: str) -> IsoDict:
        """
        Parse an ISO string and return component metadata.

        Recognized ISO strings:
            * Dates: YYYY, YYYY-MM, YYYY-MM-DD
            * Times: HH, HH:MM, HH:MM:SS
            * Subsecond: YYYY-MM-DDTHH:MM:SS.sss (Must be 1 to 9 characters)
            * TZ Aware:  YYYY-MM-DDTHH:MM:SS[+-]HH:MM or
                         YYYY-MM-DDTHH:MM:SS.sss[+-]HH:MM

        :param iso: an ISO string

        :return: {IsoDict}
        """
        meta = cls._get_meta(iso)
        return meta

    @classmethod
    def extract_date_str(cls, iso_str: str) -> str:
        """
        Extract and return an ISO date string from provided string.

        :param iso_str: {str} string to search
        :return:        {str} the date string if found, else an empty string.

        >>> Parse.extract_date_str("1983-01-15T18:25:12") == "1983-01-15"
        True
        >>> Parse.extract_date_str("18:25:12") == ""
        True

        """
        found_str = ""
        rx = r"(\d{4}-[01]\d-[0-3]\d)T?"
        match = re.search(rx, iso_str)
        if (match is not None
                and len(iso_str.split("T")[0]) <= len("YYYY-MM-DD")):
            found_str = match.group(1)
        return found_str

    @classmethod
    def extract_precision_str(cls, iso_str: str) -> str:
        """
        Extract and return precision portion from provided ISO string.

        :param iso_str: {str} string to search

        :return:        {str} the precision portion if found,
                              else an empty string is returned.

        >>> Parse.extract_precision_str("1983-01-15T18:25:12.123") == "123"
        True

        >>> Parse.extract_precision_str("1983-01-15T18:25:12") == ""
        True

        """
        found_str = ""
        rx = r"\.(\d{1,9}):?"
        match = re.search(rx, iso_str)
        if match is not None:
            found_str = match.group(1)
        return found_str

    @classmethod
    def extract_time_str(cls, iso_str: str) -> str:
        """
        Extract and return an ISO time string from provided string.

        :param iso_str: {str} string to search
        :return: {str} the time string if found, else an empty string is returned.

        >>> Parse.extract_time_str("18:25:12") == "18:25:12"
        True
        >>> Parse.extract_time_str("18:25:12") == "18:25:12"
        True
        >>> Parse.extract_time_str("T18:25:12") == "18:25:12"
        True
        >>> Parse.extract_time_str("1983-01-15T18:25:12") == "18:25:12"
        True
        >>> Parse.extract_time_str("1983-01-15T18:25:12.123") == "18:25:12"
        True
        >>> Parse.extract_time_str("1983-01-15T18:25:12+01:00") == "18:25:12"
        True
        >>> Parse.extract_time_str("1983-01-15T18:25:12.123+01:00") == "18:25:12"
        True

        """
        found_str = ""
        rx = r"(\d{2}:\d{2}:\d{2})"
        match = re.search(rx, iso_str)
        if match is not None:
            found_str = match.group(1)
        return found_str

    @classmethod
    def extract_tz_str(cls, iso_str: str) -> str:
        """
        Extract and return time zone info string from provided string.

        :param iso_str: {str} string to search
        :return:        {str} the time zone info if found,
                              else an empty string is returned.

        >>> Parse.extract_tz_str("1983-01-15T18:25:12+01:00") == "+01:00"
        True
        >>> Parse.extract_tz_str("1983-01-15T18:25:12-01:00") == "-01:00"
        True

        """
        found_str = ""
        rx = r"(?:\d{2}:\d{2})?([\-+]\d{2}:\d{2})"
        match = re.search(rx, iso_str)
        if match is not None:
            found_str = match.group(1)
        return found_str

    #
    # Class private helpers
    #

    @classmethod
    def _date_2_dict(cls, date_str) -> DateDict:
        """
        Create date component metadata dict

        :param date_str:

        :return: DateDict
        """
        dict_obj = {
            "year": None,
            "month": None,
            "day": None
        }
        parts = []
        normalized_date_str = Parse.extract_date_str(date_str)
        if normalized_date_str != "":
            parts = normalized_date_str.split("-")
        if (normalized_date_str != ""
                and (len(parts) < 1 or len(parts) > 3)):
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
        return dict_obj

    @classmethod
    def _get_meta(cls, iso: str) -> IsoDict:
        """
        Create metadata describing ISO string properties.

        :param iso:

        :return: IsoDict
        """
        date_component: DateDict = cls._date_2_dict(iso)
        time_component: TimeDict = cls._time_2_dict(iso)
        precision_component: PrecisionDict = cls._subsecond_from_iso(iso)
        tz_component: TzDict = cls._tz_from_iso(iso)
        has_date = (date_component["year"] is not None
                    and ValidateDict.validate_date_dict(date_component))
        has_time = (time_component["hour"] is not None
                    and ValidateDict.validate_time_dict(time_component))
        has_date_time = has_date and has_time
        is_precise = (precision_component["precision"] !=
                      PrecisionType.PRECISION_NON_PRECISE.name)
        is_tz_aware = tz_component["direction"] is not None
        iso_dict: IsoDict = {
            "iso": iso,
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
        return iso_dict

    @classmethod
    def _subsecond_from_iso(cls, iso_str: str) -> PrecisionDict:
        """
        Create time component metadata dict

        :param iso_str:

        :return: PrecisionDict
        """
        dict_obj: PrecisionDict = {
            "precision": None,
            "subsecond": None
        }
        normalized_precision = cls.extract_precision_str(iso_str)
        if normalized_precision == "":
            # Subsecond not present
            dict_obj["precision"] = str(PrecisionType.PRECISION_NON_PRECISE.name)
        else:
            dict_obj["subsecond"] = normalized_precision
            chars = len(dict_obj["subsecond"])
            if chars < 4:
                dict_obj["precision"] = str(PrecisionType.PRECISION_MILLISECOND.name)
            elif chars < 7:
                dict_obj["precision"] = str(PrecisionType.PRECISION_MICROSECOND.name)
            else:
                dict_obj["precision"] = str(PrecisionType.PRECISION_NANOSECOND.name)
        return dict_obj

    @classmethod
    def _time_2_dict(cls, time_str) -> TimeDict:
        """
        Create time component metadata dict. If an invalid string is passed the TimeDict
        properties will all be None.

        :param time_str: {str}

        :return: TimeDict
        """
        dict_obj = {
            "hour": None,
            "minute": None,
            "second": None
        }
        parsed_time_str = Parse.extract_time_str(time_str)
        if len(parsed_time_str) > 0:
            parts = parsed_time_str.split(":")
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
    def _tz_from_iso(cls, iso_str: str) -> TzDict:
        """
        Create timezone component metadata dict

        :param iso_str:

        :return: TzDict
        """
        dict_obj: TzDict = {
            "direction": None,
            "hour": None,
            "minute": None,
            "offset": None,
        }
        normalized_tz_str = cls.extract_tz_str(iso_str)  # Expected similar to '-06:00'
        rx = r"((?P<direction>[\-+])(?P<hour>\d{2}):(?P<minute>\d{2}))"
        match = re.search(rx, normalized_tz_str)
        if match:
            dict_obj: TzDict = {
                "direction": match.group(2),
                "hour": match.group(3),
                "minute": match.group(4),
                "offset": None
            }
            tz_offset = str((int(f'{dict_obj["direction"]}{dict_obj["hour"]}') * 60) +
                            (int(dict_obj["minute"])))
            dict_obj["offset"] = tz_offset
        return dict_obj
