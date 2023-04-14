from app.type_ext.validators.validate_dict_base import ValidateDictBase
from type_ext import TimeDict
from type_ext import utilities
from type_ext.validators.validate_iso_component_dicts import ValidateDict


class TestValidateTimeDict(ValidateDictBase):

    data_provider = None

    def setUp(self) -> None:
        super().setUp()
        self.data_provider = self.base_data_provider["time_dict"]

    def test_invalid_time_dict_should_fail(self):
        dp = self.data_provider["fail"]
        for item in dp:
            arg: TimeDict = item
            iso = utilities.join_dict_values(arg, glue=":")
            with self.subTest(iso):
                self.assertFalse(ValidateDict.validate_time_dict(arg))

    def test_valid_time_dict_should_pass(self):
        dp = self.data_provider["pass"]
        for item in dp:
            arg: TimeDict = item
            iso = utilities.join_dict_values(arg)
            with self.subTest(iso):
                self.assertTrue(ValidateDict.validate_time_dict(arg))
