from tests_src.type_ext.validators.validate_dict_base import ValidateDictBase
from type_ext import DateDict
from type_ext.validators.validate_iso_component_dicts import ValidateDict


class TestValidateDateDict(ValidateDictBase):

    data_provider = None

    def setUp(self) -> None:
        super().setUp()
        self.data_provider = self.base_data_provider["date_dict"]

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
