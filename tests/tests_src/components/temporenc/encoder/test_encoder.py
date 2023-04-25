from unittest import TestCase
from components.parsers.parse_iso_strings import Parse
from components.temporenc import Encoder, Utilities
from type_ext import IsoDict
from type_ext.temporenc_arg_dict import TemporencArgDict
import datetime


class TestEncoder(TestCase):

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
                {"iso": "2023-03-28T17:27:00.123420",
                 "encoded": "57E72DC5B0078870"},
                {"iso": "1983-01-15T18:25:12.123456",
                 "encoded": "57BF074993078900"}],
            "TYPE_DTZ": [
                {"iso": "1983-01-15T18:25:12+01:00",
                 "encoded": "CF7E0E8B2644"}],
            "TYPE_DTSZ": [
                {"iso": "1983-01-15T18:25:12.123456+01:00",
                 "encoded": "EBDF83A2C983C48110"}],
        }
        self.dp_complex_types = \
            data["TYPE_DTSZ"] + data["TYPE_DTZ"] + data["TYPE_DTS"] + data["TYPE_DT"]
        self.dp_elemental_types = data["TYPE_D"] + data["TYPE_T"]
        self.data_provider = self.dp_complex_types + self.dp_elemental_types

    def test_encode_by_args_complex_types(self):
        for item in self.dp_complex_types:
            expected = item["encoded"]
            iso_str = item["iso"]
            iso_dict: IsoDict = Parse.iso_to_iso_dict(iso_str)
            arg_dict: TemporencArgDict = Utilities.iso_dict_to_arg_dict(iso_dict)
            precision = (arg_dict["nanosecond"] or
                         arg_dict["microsecond"] or
                         arg_dict["millisecond"])
            actual = Encoder.encode_by_args(
                year=arg_dict["year"], month=arg_dict["month"], day=arg_dict["day"],
                hour=arg_dict["hour"], minute=arg_dict["minute"],
                second=arg_dict["second"],
                precision=precision, tz_offset=arg_dict["tz_offset"])
            with self.subTest(f'{actual} == {expected} for {iso_str}'):
                self.assertEqual(expected, actual)

    def test_encode_by_args_returns_uppercase_str(self):
        for item in self.dp_complex_types:
            iso_str = item["iso"]
            iso_dict: IsoDict = Parse.iso_to_iso_dict(iso_str)
            arg_dict: TemporencArgDict = Utilities.iso_dict_to_arg_dict(iso_dict)
            precision = (arg_dict["nanosecond"] or
                         arg_dict["microsecond"] or
                         arg_dict["millisecond"])
            actual = Encoder.encode_by_args(
                year=arg_dict["year"], month=arg_dict["month"], day=arg_dict["day"],
                hour=arg_dict["hour"], minute=arg_dict["minute"],
                second=arg_dict["second"],
                precision=precision, tz_offset=arg_dict["tz_offset"])
            with self.subTest(f'{iso_str} encodes to {actual}'):
                self.assertIsInstance(actual, str)
                self.assertEqual(actual.upper(), actual)

    def test_encode_iso_date(self):
        for item in self.dp_elemental_types:
            if "-" in item["iso"] or len(item["iso"]) == 4:  # Cover year only
                expected = item["encoded"]
                actual = Encoder.encode_iso_date(
                    datetime.date.fromisoformat(item["iso"]))
                with self.subTest(f'{item["iso"]} encodes to {actual}'):
                    self.assertIsInstance(actual, str)
                    self.assertEqual(actual.upper(), actual)
                    self.assertEqual(expected, actual)

    def test_encode_iso_str_encodes_complex_types(self):
        for item in self.dp_complex_types:
            expected = item["encoded"]
            actual = Encoder.encode_iso_str(item["iso"])
            with self.subTest(f'{item["iso"]} encodes to {actual}'):
                self.assertIsInstance(actual, str)
                self.assertEqual(actual.upper(), actual)
                self.assertEqual(expected, actual)

    def test_encode_iso_str_encodes_type_d(self):
        for item in self.dp_elemental_types:
            if "-" in item["iso"] or len(item["iso"]) == 4:  # Cover year only
                expected = item["encoded"]
                actual = Encoder.encode_iso_str(item["iso"])
                with self.subTest(f'{item["iso"]} encodes to {actual}'):
                    self.assertIsInstance(actual, str)
                    self.assertEqual(actual.upper(), actual)
                    self.assertEqual(expected, actual)

    def test_encode_iso_str_encodes_type_t(self):
        for item in self.dp_elemental_types:
            if ":" in item["iso"] or len(item["iso"]) == 3:  # Cover THH use
                expected = item["encoded"]
                actual = Encoder.encode_iso_time(datetime.time.fromisoformat(item["iso"]))
                with self.subTest(f'{item["iso"]} encodes to {actual}'):
                    self.assertIsInstance(actual, str)
                    self.assertEqual(actual.upper(), actual)
                    self.assertEqual(expected, actual)

    def test_encode_iso_time(self):
        for item in self.dp_elemental_types:
            if ":" in item["iso"] or len(item["iso"]) <= 3:  # Cover T15 and 15
                expected = item["encoded"]
                actual = Encoder.encode_iso_time(
                    datetime.time.fromisoformat(item["iso"]))
                with self.subTest(f'{item["iso"]} encodes to {actual}'):
                    self.assertIsInstance(actual, str)
                    self.assertEqual(actual.upper(), actual)
                    self.assertEqual(expected, actual)
