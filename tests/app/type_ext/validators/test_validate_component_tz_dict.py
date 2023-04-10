from .validate_dict_base import ValidateDictBase
from type_ext.validators import ValidateDict
import json


class TestValidateTzDict(ValidateDictBase):

    data_provider = None

    def setUp(self) -> None:
        super().setUp()
        self.data_provider = self.base_data_provider["tz_dict"]

    def test_invalid_tz_dict_should_fail(self):
        dp = self.data_provider["fail"]
        for item in dp:
            with self.subTest(json.dumps(item)):
                self.assertFalse(ValidateDict.validate_tz_dict(item))

    def test_valid_tz_dict_should_pass(self):
        dp = self.data_provider["pass"]
        for item in dp:
            with self.subTest(json.dumps(item)):
                self.assertTrue(ValidateDict.validate_tz_dict(item))
