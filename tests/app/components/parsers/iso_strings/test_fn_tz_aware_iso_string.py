import unittest
from routes.encode.components.parsers.iso_strings.parse_iso_strings import Parse
from type_ext import IsoDict, PrecisionType


class TestParseTzAwareStr(unittest.TestCase):

    empty_iso_dict: IsoDict = {
        "iso": None,
        "meta": {
             "has_date_time": {},
             "is_precise": {},
             "is_tz_aware": {}
         },
        "components": {
             "date": {},
             "precision": {},
             "time": {},
             "tz": {
                 "direction": "",
                 "hour": "",
                 "minute": "",
                 "offset": ""
             }
         }
    }

    expected_properties = {
        "date": ["year", "month", "day"],
        "precision": ["precision", "subsecond"],
        "subsecond": ["precision", "subsecond"],
        "time": ["hour", "minute", "second"],
        "tz": ["direction", "hour", "minute", "offset"],
    }

    def setUp(self) -> None:
        pass

    def test_component_date(self):
        dataprovider = [
            {"iso": "1983-01-15T18:25:12",
             "expected": {"year": "1983", "month": "01", "day": "15"}},
            {"iso": "1983-01-15T18:25:12.12",
             "expected": {"year": "1983", "month": "01", "day": "15"}},
            {"iso": "1983-01-15T18:25:12.12-06:00",
             "expected": {"year": "1983", "month": "01", "day": "15"}},
            {"iso": "1983-01-15T18:25:12.12+06:00",
             "expected": {"year": "1983", "month": "01", "day": "15"}}
        ]
        for item in dataprovider:
            with self.subTest(item['iso']):
                d = Parse.tz_aware_iso_string(f'{item["iso"]}')
                actual = d["components"]["date"]
                expected = item["expected"]
                self.assertListEqual(list(expected.keys()), list(actual))
                self.assertEqual(expected["year"], actual["year"])
                self.assertEqual(expected["month"], actual["month"])
                self.assertEqual(expected["day"], actual["day"])

    def test_component_precision(self):
        dataprovider = [
            {"iso": "1983-01-15T18:25:12.1",
             "expected": {
                 "precision": PrecisionType.PRECISION_MICROSECOND.name,
                 "subsecond": "1"}
             },
            {"iso": "1983-01-15T18:25:12.12",
             "expected": {
                 "precision": PrecisionType.PRECISION_MICROSECOND.name,
                 "subsecond": "12"}
             },
            {"iso": "1983-01-15T18:25:12.12345",
             "expected": {
                 "precision": PrecisionType.PRECISION_MILLISECOND.name,
                 "subsecond": "12345"}
             },
            {"iso": "1983-01-15T18:25:12.1234567",
             "expected": {
                 "precision": PrecisionType.PRECISION_NANOSECOND.name,
                 "subsecond": "1234567"}
             }
        ]
        for item in dataprovider:
            with self.subTest(item['iso']):
                d = Parse.tz_aware_iso_string(f'{item["iso"]}')
                actual = d["components"]["precision"]
                expected = item["expected"]
                self.assertListEqual(list(expected.keys()), list(actual.keys()))
                self.assertEqual(expected["subsecond"], actual["subsecond"])
                self.assertEqual(expected["subsecond"], actual["subsecond"])

    def test_component_time(self):
        dataprovider = [
            {"iso": "1983-01-15T18:25:12",
             "expected": {"hour": "18", "minute": "25", "second": "12"}},
            {"iso": "1983-01-15T18:25:12.12",
             "expected": {"hour": "18", "minute": "25", "second": "12"}},
            {"iso": "1983-01-15T18:25:12.12-06:00",
             "expected": {"hour": "18", "minute": "25", "second": "12"}},
            {"iso": "1983-01-15T18:25:12.12+06:00",
             "expected": {"hour": "18", "minute": "25", "second": "12"}},
        ]
        for item in dataprovider:
            with self.subTest(item['iso']):
                d = Parse.tz_aware_iso_string(f'{item["iso"]}')
                actual = d["components"]["time"]
                expected = item["expected"]
                self.assertListEqual(list(expected.keys()), list(actual.keys()))
                self.assertEqual(expected["hour"], actual["hour"])
                self.assertEqual(expected["minute"], actual["minute"])
                self.assertEqual(expected["second"], actual["second"])

    def test_component_tz(self):
        data_provider = [
            {"iso": "1983-01-15T18:25:12.12345-06:00",
             "expected": {
                 "direction": "-",
                 "hour": "06",
                 "minute": "00",
                 "offset": "-360"}},
            {"iso": "1983-01-15T18:25:12+06:00",
             "expected": {
                 "direction": "+",
                 "hour": "06",
                 "minute": "00",
                 "offset": "360"}}
        ]
        for item in data_provider:
            with self.subTest(item['iso']):
                d = Parse.tz_aware_iso_string(item["iso"])
                actual = d["components"]["tz"]
                expected = item["expected"]
                self.assertListEqual(list(expected.keys()), list(actual.keys()))
                self.assertEqual(expected["direction"], actual["direction"])
                self.assertEqual(expected["hour"], actual["hour"])
                self.assertEqual(expected["minute"], actual["minute"])
                self.assertEqual(expected["offset"], actual["offset"])

    def test_raises_exception_time_no_colon(self):
        iso = "1983-01-15T18-25-12.123456"
        # TODO: #16 Check Raised Exception Message
        self.assertRaises(ValueError, Parse.tz_aware_iso_string, iso)

    def test_raises_exception_year_no_dash(self):
        iso = "1983:01:15T18:25:12.123456"
        self.assertRaisesRegex(
            ValueError,
            'ValueError: 1983:01:15 - Expected string in YYYY-MM-DD format',
            Parse.tz_aware_iso_string, iso)

    def test_raises_exception_year_format(self):
        iso = "1983-01-15-02T18:25:12.123456"
        self.assertRaisesRegex(
            ValueError,
            'ValueError: 1983-01-15-02 - Expected string in YYYY-MM-DD format',
            Parse.tz_aware_iso_string, iso)

    def test_returns_an_instance_of_dict(self):
        iso = "1983-01-15T18:25:12.123456"
        self.assertIsInstance(Parse.tz_aware_iso_string(iso), dict)

    def test_returned_dict_has_expected_date_properties(self):
        iso = "1983-01-15T18:25:12.123456"
        expected = self.expected_properties["date"]
        d = Parse.tz_aware_iso_string(iso)
        actual = list(d["components"]["date"].keys())
        self.assertListEqual(expected, actual)

    def test_returned_dict_has_expected_precision_properties(self):
        iso = "1983-01-15T18:25:12.12345"
        expected = self.expected_properties["precision"]
        d = Parse.tz_aware_iso_string(iso)
        actual = list(d["components"]["precision"].keys())
        self.assertListEqual(expected, actual)

    def test_returned_dict_has_expected_tz_properties(self):
        expected = list(self.empty_iso_dict["components"]["tz"].keys())
        iso = "1983-01-15T18:25:12.12345-06:00"
        d: IsoDict = Parse.tz_aware_iso_string(iso)
        actual = list(d["components"]["tz"].keys())
        self.assertListEqual(expected, actual)

    def test_returned_dict_has_expected_time_properties(self):
        iso = "1983-01-15T18:25:12.123456"
        expected = self.expected_properties["time"]
        d = Parse.tz_aware_iso_string(iso)
        actual = list(d["components"]["time"].keys())
        self.assertListEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
