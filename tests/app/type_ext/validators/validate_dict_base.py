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
                    {"year": "1900", "month": "02", "day": "29"},   # Not leap year
                    {"year": "2022", "month": "04", "day": "31"},   # Apr has 30 days
                    {"year": "2023", "month": "02", "day": "29"},   # Not leap year
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
            },
            "tz_dict": {
                "pass": [
                    {"direction": "+", "hour": "01", "minute": "30", "offset": "90"},
                    {"direction": "+", "hour": "01", "minute": "30", "offset": "+90"},
                    {"direction": "-", "hour": "05", "minute": "00", "offset": "-300"},
                    {"direction": "+", "hour": "01", "minute": "30", "offset": "+90"},
                    {"direction": "+", "hour": "01", "minute": "30", "offset": "+90"},
                    {"direction": "-", "hour": "01", "minute": "30", "offset": "-90"},
                    {"direction": "+", "hour": "01", "minute": "30", "offset": "90"},
                ],
                "fail": [
                    {"direction": "&", "hour": "01", "minute": "30", "offset": "+90"},
                    {"direction": "+", "hour": "25", "minute": "30", "offset": "+90"},
                    {"direction": "-", "hour": "01", "minute": "32", "offset": "-92"},
                    {"direction": "+", "hour": "01", "minute": "32", "offset": "92"},
                ]
            }
        }
