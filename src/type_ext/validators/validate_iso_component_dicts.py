import re
from datetime import datetime
from type_ext import PrecisionType
from type_ext import DateDict, TimeDict, PrecisionDict, TzDict


class ValidateDict:

    @staticmethod
    def validate_date_dict(date_dict: DateDict, allow_year_zero: bool = True):
        """
        Validate DateDict members parse to a valid date.

        Notes: * ISO strings in the form YYYY, are validated against YY-01-01
               * ISO strings in the form YYYY-MM, are validated against YY-MM-01

        :param date_dict:        {DateDict} DateDict to evaluate
        :param allow_year_zero:  {bool} Allow/disallow validation where ISO string
                                            YYYY is "0000"
        :return:                 {bool} True if DateDict members parse to a valid date.
        """
        date = None
        if allow_year_zero and date_dict["year"] == "0000":
            date_dict["year"] = "0004"
        iso = (f'{date_dict["year"]}-' +
               f'{date_dict["month"]}-' +
               f'{date_dict["day"]}') \
            .replace("None", "01")
        try:
            date = datetime.fromisoformat(iso)
        finally:
            return date is not None

    @staticmethod
    def validate_precision_dict(precision_dict: PrecisionDict):
        """
        Validate PrecisionDict members
            * precision: Must be a member of PrecisionType enum
            * subsecond: Must be:
                             =< 3 for microsecond precision
                             =< 6 for millisecond precision
                             =< 9 for nanosecond precision
                             == 0 for none, or not precise precision

        :param precision_dict: {PrecisionDict} DateDict to evaluate
        :return:               {bool} True if PrecisionDict members are valid

        >>> cls = ValidateDict
        >>> valid_dict = {"precision": "PRECISION_MICROSECOND", "subsecond": "1"}
        >>> invalid_dict = {"precision": "PRECISION_MICROSECOND", "subsecond": "1234"}
        >>> none_dict = {"precision": "PRECISION_NONE", "subsecond": None}
        >>> cls.validate_precision_dict(valid_dict) == True
        True
        >>> cls.validate_precision_dict(invalid_dict) == False
        True
        """
        # Validate precision
        precision_name = precision_dict["precision"]
        is_valid = precision_name in list(PrecisionType.__members__)
        # Validate subsecond
        if is_valid:
            if precision_name == PrecisionType.PRECISION_NONE.name or \
                    precision_name == PrecisionType.PRECISION_NON_PRECISE.name:
                is_valid = precision_dict["subsecond"] is None
            elif precision_dict["subsecond"] is not None:
                match precision_name:
                    case PrecisionType.PRECISION_MICROSECOND.name:
                        is_valid = len(precision_dict["subsecond"]) <= 3
                    case PrecisionType.PRECISION_MILLISECOND.name:
                        is_valid = len(precision_dict["subsecond"]) <= 6
                    case PrecisionType.PRECISION_NANOSECOND.name:
                        is_valid = len(precision_dict["subsecond"]) <= 9
                    case _:
                        is_valid = False
            else:
                is_valid = False
        return is_valid

    @staticmethod
    def validate_time_dict(time_dict: TimeDict):
        """
        Validate TimeDict members parse to a valid time.

        Notes: * ISO strings in the form HH, are validated against HH:01:01
               * ISO strings in the form HH:MM, are validated against HH:MM:01

        :param time_dict:        {TimeDict} TimeDict to evaluate
        :return:                 {bool} True if TimeDict members parse to a valid time.

        >>> cls = ValidateDict
        >>> cls.validate_time_dict({"hour": "23", "minute": "59", "second": "59"})
        True
        >>> cls.validate_time_dict({"hour": "23", "minute": "59", "second": None})
        True
        """
        time = None
        time_str = (f'{time_dict["hour"]}:' +
                    f'{time_dict["minute"]}:' +
                    f'{time_dict["second"]}').replace("None", "01")
        try:
            time = datetime.strptime(time_str, '%H:%M:%S')
        finally:
            return time is not None

    @staticmethod
    def validate_tz_dict(tz_dict: TzDict):
        """
        Validate TzDict member.

        Notes
            * Direction: Should be "+" or "-"
            * Hour:      Hour should be "00" to "12",
                         If Direction is "+", "13" and "14" is allowed
            * Minute:    "00", "15", "30", "45" or "60"
            * Offset:     Should match calculated offset

        :param tz_dict: {TzDict} TimeDict to evaluate
        :return:        {bool}   True if TzDict members are valid.

        >>> cls = ValidateDict
        >>> l = [
        ... {"direction": "+", "hour": "01", "minute": "30", "offset": "90"},
        ... {"direction": "+", "hour": "01", "minute": "30", "offset": "+90"},
        ... {"direction": "-", "hour": "01", "minute": "30", "offset": "-90"},
        ... {"direction": "-", "hour": "01", "minute": "31", "offset": "-91"},
        ... ]
        >>> cls.validate_tz_dict(l[0]) == True
        True
        >>> cls.validate_tz_dict(l[1]) == True
        True
        >>> cls.validate_tz_dict(l[2]) == True
        True
        >>> cls.validate_tz_dict(l[3]) == False
        True
        """
        # Validate Direction: Should be "+" or "-"
        dir_is_val = tz_dict["direction"] in ["+", "-"]
        #
        # Validate Hour - Hour should be "00" to "12",
        #                 If Direction is "+", "13" and "14" is allowed
        #
        hh_is_valid = re.match(r"^0[0-9]|1[0-4]$", tz_dict["hour"]) is not None
        #
        # Validate Minute - Should be "00", "15", "30", "45" or "60"
        mm_is_valid = tz_dict["minute"] in ["00", "15", "30", "45", "60"]
        #
        # Validate Offset - tz_dict["offset"] should match calculated offset
        #
        offset_is_valid = (re.match(r"^[+-]?\d{1,3}$", tz_dict["minute"]) is not None
                           and hh_is_valid and mm_is_valid)
        if offset_is_valid:
            # Calculate offset and compare to tz_dict["offset"]
            offset_expected = tz_dict["direction"] + str(
                (int(tz_dict["hour"]) * 60) + int(tz_dict["minute"]))\
                .zfill(2)
            if tz_dict["offset"][0] in ["+", "-"]:
                offset_actual = tz_dict["offset"]
            else:
                offset_actual = f'{tz_dict["direction"]}{tz_dict["offset"]}'
            offset_is_valid = offset_actual == offset_expected

        return dir_is_val and hh_is_valid and mm_is_valid and offset_is_valid
