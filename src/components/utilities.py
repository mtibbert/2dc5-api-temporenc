import re
from datetime import date, time


class Utilities:

    @classmethod
    def is_iso_date_str(cls, str_2_evaluate: str) -> bool:
        """
        Evaluate if string parses to a Date object.

        :param str_2_evaluate:

        :return: {bool} True if string parses to a Date object; else False.

        >>> Utilities.is_iso_date_str("1983-01-15") == True
        True
        >>> Utilities.is_iso_date_str("19830229") == False
        True
        >>> Utilities.is_iso_date_str("1983-02-29") == False
        True

        """
        ret_val = False

        if len(str_2_evaluate) <= len("YYYY-MM-DD"):
            parts = [int(x) for x in str_2_evaluate.split("-")]
            match len(parts):
                case 3:
                    pass  # Year, month and day
                case 2:
                    parts += [0]  # Year & month; append second
                case 1:
                    parts += [0, 0]  # Year; append hour and minute
                case _:
                    parts[0] = -1  # Invalid results, force ValueError
            try:
                ret_val = date(parts[0], parts[1], parts[2]) is not None
            except ValueError:
                ret_val = False

        return ret_val

    @classmethod
    def is_iso_time_str(cls, str_2_evaluate: str) -> bool:
        """
        Evaluate if string parses to a Time object.

        :param str_2_evaluate:

        :return: {bool} True if string parses to a Time object; else False.

        >>> Utilities.is_iso_time_str("18:25:12") == True
        True
        >>> Utilities.is_iso_time_str("182512") == False
        True
        >>> Utilities.is_iso_time_str("18:25:63") == False
        True

        """
        # noinspection PyUnusedLocal
        ret_val: bool = False
        # Remove "T" if present, then split string on colon(s)
        if str_2_evaluate[0] == "T":
            str_2_evaluate = str_2_evaluate.replace("T", "")
        parts = [int(x) for x in str_2_evaluate.split(":")]
        match len(parts):
            case 3:
                pass  # Hour, minute and second
            case 2:
                parts += [0]  # Hour & minutes; append second
            case 1:
                parts += [0, 0]  # Hour only; append hour and minute
            case _:
                parts[0] = -1  # Invalid results, force ValueError
        try:
            ret_val = time(parts[0], parts[1], parts[2]) is not None
        except ValueError:
            ret_val = False
        return ret_val

    @classmethod
    def normalize_iso_str(cls, iso_str: str) -> str:
        """
        Normalizes ISO strings by removing trailing precision zeros.

        :param iso_str: {str}

        :return: {str}

        >>> u = Utilities
        >>> u.normalize_iso_str('1983-01-15T18:25:12.120') == '1983-01-15T18:25:12.12'
        True
        """
        normalized_iso = iso_str
        parts = iso_str.split(".")
        if len(parts) == 2:
            regex = r"([1-9]{1,9})(0{1,89})([+-]*?)"
            subst = "\\g<1>"
            result = re.sub(regex, subst, parts[1], 0)
            if result and int(re.split(r'\W+', result, 1)[0]) > 0:
                normalized_iso = f'{parts[0]}.{result}'
            elif result:
                # Remove precision when ISO in form of "1983-01-15T18:25:12.0"
                normalized_iso = f'{parts[0]}'
        return normalized_iso

    @classmethod
    def packb_args_to_iso(cls,
                          year: int = None, month: int = None, day: int = None,
                          hour: int = None, minute: int = None, second: int = None,
                          precision: int = None, tz_offset: int = None):
        """
        Parse Date, Time, Datetime like arguments into an ISO string format.

        Note: No validation of the resulting string occurs.

        :param year: {int} Default is None
        :param month:  {int} Default is None
        :param day:  {int} Default is None
        :param hour:  {int} Default is None
        :param minute:  {int} Default is None
        :param second:  {int} Default is None
        :param precision:  {int} Default is None
        :param tz_offset:  {int} Default is None

        :return: {str}

        >>> u = Utilities
        >>> expected = '1983-01-15T18:25:12.123+01:00'
        >>> u.packb_args_to_iso(1983, 1, 15, 18, 25,12, 123, 60) == expected
        True

        """
        tz_sfx = ""

        iso = re.sub(
            r"(-?None)", "",
            f'{str(year).zfill(4)}-{str(month).zfill(2)}-{str(day).zfill(2)}')

        time_str = re.sub(
            r"(:?None)", "",
            f'{str(hour).zfill(2)}:{str(minute).zfill(2)}:{str(second).zfill(2)}')

        precision = "" if precision is None else f'.{precision}'

        if tz_offset is not None:
            tz_dir = "+" if tz_offset >= 0 else "-"
            tz_sfx = f'{tz_dir}' + \
                     f'{str(abs(int(tz_offset/60))).zfill(2)}:' + \
                     f'{str(int(tz_offset % 60)).zfill(2)}'

        if iso == "":             # Type T
            iso = f'{time_str}'
        elif time_str != "":      # Type D, DT, DTS, DTZ, or DTSZ
            iso += f'T{time_str}{precision}{tz_sfx}'
        return iso
