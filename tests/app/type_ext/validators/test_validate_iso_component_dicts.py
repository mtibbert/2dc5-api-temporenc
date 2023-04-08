from unittest import TestCase
from type_ext import DateDict
from type_ext.validators.validate_iso_component_dicts import ValidateDict


class TestValidateDateDict(TestCase):

    data_provider = None

    def setUp(self) -> None:
        self.data_provider = {
            "pass": [
                {"year": "4094", "month": "12", "day": "31"},   # Max date for encoding
                {"year": "4095", "month": None, "day": None},   # Temporenc special year
                {"year": "2000", "month": "02", "day": "29"},   # Leap year (div by 400)
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
            ]}

    def test_invalid_date_dict_should_fail(self):
        dp = self.data_provider["fail"]
        for item in dp:
            arg: DateDict = item
            iso = f'{arg["year"]}-{arg["month"]}-{arg["day"]}' \
                .replace("-None", "")
            with self.subTest(iso):
                self.assertFalse(ValidateDict.validate_date_dict(arg))

    def test_valid_date_dict_should_pass(self):
        dp = self.data_provider["pass"]
        for item in dp:
            arg: DateDict = item
            iso = f'{arg["year"]}-{arg["month"]}-{arg["day"]}' \
                .replace("-None", "")
            with self.subTest(iso):
                self.assertTrue(ValidateDict.validate_date_dict(arg))

    def test_validate_year_0000_allow_arg_false(self):
        dp = [{"year": "0000", "month": None, "day": None},
              {"year": "0000", "month": "01", "day": None},
              {"year": "0000", "month": "01", "day": "01"}]
        for item in dp:
            arg: DateDict = item
            iso = f'{arg["year"]}-{arg["month"]}-{arg["day"]}' \
                .replace("-None", "")
            with self.subTest(iso):
                actual = \
                    ValidateDict.validate_date_dict(arg, allow_year_zero=False)
                self.assertFalse(actual)

    def test_validate_year_0000_allow_arg_true(self):
        dp = [{"year": "0000", "month": None, "day": None},
              {"year": "0000", "month": "01", "day": None},
              {"year": "0000", "month": "01", "day": "01"}]
        for item in dp:
            arg: DateDict = item
            iso = f'{arg["year"]}-{arg["month"]}-{arg["day"]}' \
                .replace("-None", "")
            with self.subTest(iso):
                self.assertTrue(ValidateDict.validate_date_dict(arg))
