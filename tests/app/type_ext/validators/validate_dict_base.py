import re
from unittest import TestCase


class ValidateDictBase(TestCase):
    data_provider = None

    def setUp(self) -> None:
        self.data_provider = {"time_dict": {
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
                {"hour": "01", "minute": "65", "second": "01"},   # Invalid char minute
                {"hour": "01", "minute": "01", "second": "65"},   # Invalid char second
            ]}
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
