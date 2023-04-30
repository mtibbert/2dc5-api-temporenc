from unittest import TestCase
from components.parsers.parse_iso_strings import Parse
from components.temporenc import Utilities
from type_ext import IsoDict


class TestFnIsoDictAsIsoStr(TestCase):

    data_provider = {}

    def setUp(self) -> None:
        data = {
            "TYPE_D": [
                {"iso": "1983-01-15",
                 "encoded": "8F7E0E"}],
            "TYPE_T": [
                {"iso": "18:25:12",
                 "encoded": "A1264C"}],
            "TYPE_DT": [
                {"iso": "1983-01-15T18:25:12",
                 "encoded": "1EFC1D264C"}],
            "TYPE_DTS": [
                {"iso": "1983-01-15T18:25:12.123456789",
                 "encoded": "67BF074993075BCD15"},
                {"iso": "2023-03-28T17:27:00.123420",
                 "encoded": "57E72DC5B0078870"}, ],
            "TYPE_DTZ": [
                {"iso": "1983-01-15T18:25:12+01:00",
                 "encoded": "CF7E0E8B2644"}],  # CF7E0E8B2644  - CF7E0E932644
            "TYPE_DTSZ": [
                {"iso": "1983-01-15T18:25:12.123456789+01:00",
                 "encoded": "F3DF83A2C983ADE68AC4"}, ],
        }
        self.data_provider = (data["TYPE_D"] + data["TYPE_T"] +
                              data["TYPE_DT"] + data["TYPE_DTS"] + data["TYPE_DTZ"] +
                              data["TYPE_DTS"])

    def test_fn_iso_dict_as_iso_str_returns_expected_value(self):
        for item in self.data_provider:
            expected = item["iso"]
            iso_dict: IsoDict = Parse.iso_to_iso_dict(expected)
            actual = Utilities.iso_dict_as_iso_str(iso_dict)
            with self.subTest(f'{actual} == {expected}'):
                self.assertEqual(expected, actual)
