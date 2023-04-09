from app.type_ext.validators.validate_dict_base import ValidateDictBase
from type_ext import TimeDict
from type_ext.validators.validate_iso_component_dicts import ValidateDict


class TestValidateTimeDict(ValidateDictBase):

    def setUp(self) -> None:
        super().setUp()  # Init data_provider

    def test_invalid_time_dict_should_fail(self):
        dp = self.data_provider["time_dict"]["fail"]
        for item in dp:
            arg: TimeDict = item
            iso = self.join_dict_values(arg, glue=":")
            with self.subTest(iso):
                self.assertFalse(ValidateDict.validate_time_dict(arg))

    def test_valid_time_dict_should_pass(self):
        dp = self.data_provider["time_dict"]["pass"]
        for item in dp:
            arg: TimeDict = item
            iso = self.join_dict_values(arg)
            with self.subTest(iso):
                self.assertTrue(ValidateDict.validate_time_dict(arg))
