import re
from unittest import TestCase


class ValidateDictBase(TestCase):
    base_data_provider = None

    def setUp(self) -> None:
        self.base_data_provider = {
            "date_dict": {
                "pass": [
                    {"year": "4094", "month": "12", "day": "31"},   # Max date
                    {"year": "4095", "month": None, "day": None},   # Temporenc special
                    {"year": "2000", "month": "02", "day": "29"},   # Leap year div by 400
                    {"year": "9999", "month": "12", "day": "31"},   # Max ISO defined date
                    {"year": "4095", "month": "01", "day": "15"},   #
                    {"year": "1982", "month": "01", "day": "15"},   #
                ],
                "fail": [
                    {"year": "1", "month": "01", "day": "01"},      # Single char year
                    {"year": "12", "month": "01", "day": "01"},     # Two char year
                    {"year": "123", "month": "01", "day": "01"},    # Three char year
                    {"year": "1900", "month": "02", "day": "29"},   # Not a leap year
                    {"year": "2022", "month": "04", "day": "31"},   # Apr has 30 days
                    {"year": "2023", "month": "02", "day": "29"},   # Not a leap year
                    {"year": "2023", "month": "13", "day": "05"},   # Invalid month
                    {"year": "10000", "month": "01", "day": "01"},  # Five char year
                ]
            },
            "time_dict": {
                "pass": [
                    {"hour": "23", "minute": "59", "second": "59"},  # Max time
                    {"hour": "00", "minute": "00", "second": "00"},  # Min time
                    {"hour": "23", "minute": "59", "second": "59"},  # Max time
                    {"hour": "01", "minute": None, "second": None},  #
                    {"hour": "01", "minute": "02", "second": None},  #
                    {"hour": "18", "minute": "25", "second": "12"},  #
                    # Single char allowed in time
                    {"hour": "1", "minute": "01", "second": "01"},   # Single char hour
                    {"hour": "01", "minute": "1", "second": "01"},   # Single char minute
                    {"hour": "01", "minute": "01", "second": "1"},   # Single char second
                ],
                "fail": [
                    {"hour": "23", "minute": "59", "second": "60"},   # Leap Second
                    {"hour": "001", "minute": "01", "second": "01"},  # Three char hour
                    {"hour": "01", "minute": "001", "second": "01"},  # Three char minute
                    {"hour": "01", "minute": "01", "second": "001"},  # Three char second
                    {"hour": "59", "minute": "01", "second": "01"},   # Invalid char hour
                    {"hour": "01", "minute": "65", "second": "01"},   # Invalid minute
                    {"hour": "01", "minute": "01", "second": "65"},   # Invalid second
                ]},
            "precision_dict": {
                "pass": [
                    {"precision": "PRECISION_MICROSECOND", "subsecond": "1"},
                    {"precision": "PRECISION_MICROSECOND", "subsecond": "12"},
                    {"precision": "PRECISION_MICROSECOND", "subsecond": "123"},
                    {"precision": "PRECISION_MILLISECOND", "subsecond": "123"},
                    {"precision": "PRECISION_MILLISECOND", "subsecond": "1234"},
                    {"precision": "PRECISION_MILLISECOND", "subsecond": "12345"},
                    {"precision": "PRECISION_MILLISECOND", "subsecond": "123456"},
                    {"precision": "PRECISION_NANOSECOND", "subsecond": "1234567"},
                    {"precision": "PRECISION_NANOSECOND", "subsecond": "12345678"},
                    {"precision": "PRECISION_NANOSECOND", "subsecond": "123456789"},
                    {"precision": "PRECISION_NONE", "subsecond": None},
                    {"precision": "PRECISION_NON_PRECISE", "subsecond": None},
                ],
                "fail": [
                    {"precision": "foo", "subsecond": "123456"},
                    {"precision": "PRECISION_MICROSECOND", "subsecond": None},
                    {"precision": "PRECISION_MICROSECOND", "subsecond": "1234"},
                    {"precision": "PRECISION_NANOSECOND", "subsecond": "1234567891"},
                ]
            }
        }

    @staticmethod
    def join_dict_values(d: dict, glue: str = "-", normalize: bool = True) -> str:
        """
        Join all dictionary values.

        :param d:         {dict} source dictionary
        :param glue:      {str}  character to join values, defaults to "-"
        :param normalize: {bool} normalize returned string by removing 'None' values,
                                 defaults to True

        :return: {str}

        # >>> cls = TestValidateTimeDict
        # >>> date_dict = {"year": "1983", "month": "01", "day": "15"}
        # >>> none_dict = {"year": "1983", "month": "01", "day": None}
        # >>> time_dict = {"hour": "23", "minute": "59", "second": "59"}
        # >>> cls.join_dict_values(date_dict) == '1983-01-15'
        # True
        # >>> cls.join_dict_values(none_dict) == '1983-01'
        # True
        # >>> cls.join_dict_values(none_dict, "-", False) == '1983-01-None'
        # True
        # >>> cls.join_dict_values(time_dict, ":") == '23:59:59'
        # True
        """
        # TODO: Move to Utility Class
        ret_str = glue.join([str(x) for x in d.values()])
        if normalize:
            ret_str = ValidateDictBase.normalize_none(ret_str)
        return ret_str

    @staticmethod
    def normalize_none(iso) -> str:
        """
        Removes "None" from ISO strings

        :param iso: {str} an ISO string
        :return: {str}

        # >>> TestValidateTimeDict.normalize_none("1983-01-None") == '1983-01'
        # True
        # >>> TestValidateTimeDict.normalize_none("1983-None-None") == '1983'
        # True
        # >>> TestValidateTimeDict.normalize_none("13:01:None") == '13:01'
        # True
        """
        # TODO: Move to Utility Class
        rx = r"([-:]None){1,2}$"
        iso_str = re.sub(rx, "", iso)
        return iso_str
