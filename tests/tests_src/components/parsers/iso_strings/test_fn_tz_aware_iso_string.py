import unittest
from tests_src.components.parsers.iso_strings.tests_parse_iso_string_base \
    import TestsParseIsoStringBase
from components.parsers.iso_strings.parse_iso_strings import Parse
from type_ext.validators import ValidateDict
from type_ext import DateDict


class TestTestsParseTzAwareStr(TestsParseIsoStringBase):

    def setUp(self) -> None:
        super().setUp()

    def test_component_date(self):
        data_provider = {k: v for k,
                         v in self.data_provider.items() if k != "TYPE_T"}
        dp_keys = data_provider.keys()
        for type_key in dp_keys:
            assert type_key not in ["TYPE_T"]  # Test requires date component
            for item in data_provider[type_key]:
                with self.subTest(item['iso']):
                    d = Parse.iso_string(f'{item["iso"]}')
                    actual: DateDict = d["components"]["date"]
                    expected = item["expected"]["components"]["date"]
                    # Assert valid date, validate_date_dict() always false for TYPE_T
                    if type_key != "TYPE_T":
                        self.assertTrue(ValidateDict.validate_date_dict(actual))
                    self.assertEqual(len(expected.keys()), len(actual.keys()))
                    self.assertListEqual(list(expected.values()), list(actual.values()))
                    self.assertListEqual(list(expected), list(actual))

    def test_component_precision(self):
        dp_keys = self.data_provider.keys()
        for type_key in dp_keys:
            for item in self.data_provider[type_key]:
                with self.subTest(item['iso']):
                    d = Parse.iso_string(f'{item["iso"]}')
                    actual = d["components"]["precision"]
                    expected = item["expected"]["components"]["precision"]
                    self.assertTrue(ValidateDict.validate_precision_dict(actual))
                    self.assertListEqual(list(expected.keys()), list(actual.keys()))
                    self.assertEqual(expected["subsecond"], actual["subsecond"])
                    self.assertEqual(expected["subsecond"], actual["subsecond"])

    def test_component_time(self):
        dp_keys = self.data_provider.keys()
        for type_key in dp_keys:
            for item in self.data_provider[type_key]:
                with self.subTest(item['iso']):
                    d = Parse.iso_string(f'{item["iso"]}')
                    actual = d["components"]["time"]
                    expected = item["expected"]["components"]["time"]
                    self.assertTrue(ValidateDict.validate_time_dict(actual))
                    self.assertListEqual(list(expected.keys()), list(actual.keys()))
                    self.assertEqual(expected["hour"], actual["hour"])
                    self.assertEqual(expected["minute"], actual["minute"])
                    self.assertEqual(expected["second"], actual["second"])

    def test_component_tz(self):
        data_provider = {k: v for k, v in self.data_provider.items() if "Z" in k}
        dp_keys = data_provider.keys()
        for type_key in dp_keys:
            assert type_key in ["TYPE_DTZ", "TYPE_DTSZ"]  # Test requires tz component
            for item in data_provider[type_key]:
                with self.subTest(item['iso']):
                    d = Parse.iso_string(item["iso"])
                    actual = d["components"]["tz"]
                    expected = item["expected"]["components"]["tz"]
                    self.assertTrue(ValidateDict.validate_tz_dict(actual))
                    self.assertListEqual(list(expected.keys()), list(actual.keys()))
                    self.assertEqual(expected["direction"], actual["direction"])
                    self.assertEqual(expected["hour"], actual["hour"])
                    self.assertEqual(expected["minute"], actual["minute"])
                    self.assertEqual(expected["offset"], actual["offset"])

    # TODO: #16 Check Raised Exception Message
    def test_extract_time_str_no_colon(self):
        iso = "1983-01-15T18-25-12.123456"
        self.assertEqual("", Parse.extract_time_str(iso))

    def test_extract_date_str_no_dash(self):
        iso = "1983:01:15T18:25:12.123456"
        self.assertEqual("", Parse.extract_date_str(iso))

    def test_extract_date_str_bad_format(self):
        iso = "1983-01-15-02T18:25:12.123456"
        self.assertEqual("", Parse.extract_date_str(iso))


if __name__ == '__main__':
    unittest.main()
