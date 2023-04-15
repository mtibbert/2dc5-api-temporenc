from datetime import date, time


class Utilities:

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
