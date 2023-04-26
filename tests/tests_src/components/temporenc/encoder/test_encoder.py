from tests_src.components.temporenc.encoder.tests_encoder_base import TestsEncoderBase
from components.parsers.parse_iso_strings import Parse
from components.temporenc import Encoder, Utilities
from type_ext import IsoDict
from type_ext.temporenc_arg_dict import TemporencArgDict
import datetime


class TestEncoder(TestsEncoderBase):

    def setUp(self) -> None:
        super().setUp()

    def test_encode_by_args_complex_types(self):
        for item in self.dp_complex_types:
            expected = item["encoded"]
            iso_str = item["iso"]
            # TODO: #28 Create Utilities.iso_str_to_arg_dict() fn
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
            # TODO: #28 Create Utilities.iso_str_to_arg_dict() fn
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
