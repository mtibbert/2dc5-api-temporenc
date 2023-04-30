from tests_src.components.temporenc.tests_base import TestsBase
from components.temporenc import Encoder, Utilities
from components.parsers import Parse
import datetime


class TestEncoderEncodeFnsReturnCongruent(TestsBase):

    def setUp(self) -> None:
        super().setUp()

    def test_encode_dto_encodes_same_as_encode_by_args(self):
        # Check Types DT, DTS, DTZ, and DTSZ
        for item in [i for i in self.data_provider if "T" in i["iso"]]:
            precision_type = None
            iso_dict = Parse.iso_to_iso_dict(item["iso"])
            arg_dict = Utilities.iso_dict_to_arg_dict(iso_dict)
            if arg_dict["nanosecond"] is not None:
                precision_type = "nanosecond"
            elif arg_dict["microsecond"] is not None:
                precision_type = "microsecond"
            elif arg_dict["millisecond"] is not None:
                precision_type = "millisecond"
            # noinspection PyTypedDict
            precision = None if precision_type is None else int(arg_dict[precision_type])
            # noinspection PyTypedDict
            actual = Encoder.encode_by_args(
                year=arg_dict["year"],
                month=arg_dict["month"],
                day=arg_dict["day"],
                hour=arg_dict["hour"],
                minute=arg_dict["minute"],
                second=arg_dict["second"],
                precision=precision,
                tz_offset=arg_dict["tz_offset"]
            )
            expected = Encoder.encode_iso_dto(
                datetime.datetime.fromisoformat(item["iso"]))
            with self.subTest(f'{actual} == {expected} for {item["iso"]}'):
                # Make sure we're checking a good encoding
                assert expected == item["encoded"]
                self.assertEqual(expected, actual)

    def test_encode_dto_encodes_same_as_encode_iso(self):
        # Check Types DT, DTS, DTZ, and DTSZ
        for item in [i for i in self.data_provider if "T" in i["iso"]]:
            expected = Encoder.encode_iso_dto(
                datetime.datetime.fromisoformat(item["iso"]))
            actual = Encoder.encode_iso_str(item["iso"])
            with self.subTest(f'{actual} == {expected} for {item["iso"]}'):
                # Make sure we're checking a good encoding
                assert expected == item["encoded"]
                self.assertEqual(expected, actual)

    def test_encode_iso_encodes_same_as_encode_by_args(self):
        # Check Types DT, DTS, DTZ, and DTSZ
        for item in [i for i in self.data_provider if "T" in i["iso"]]:
            precision_type = None
            iso_dict = Parse.iso_to_iso_dict(item["iso"])
            # TODO: #28 Create Utilities.iso_str_to_arg_dict() fn
            arg_dict = Utilities.iso_dict_to_arg_dict(iso_dict)
            if arg_dict["nanosecond"] is not None:
                precision_type = "nanosecond"
            elif arg_dict["microsecond"] is not None:
                precision_type = "microsecond"
            elif arg_dict["millisecond"] is not None:
                precision_type = "millisecond"
            # noinspection PyTypedDict
            precision = None if precision_type is None else int(arg_dict[precision_type])
            # noinspection PyTypedDict
            actual = Encoder.encode_by_args(
                year=arg_dict["year"],
                month=arg_dict["month"],
                day=arg_dict["day"],
                hour=arg_dict["hour"],
                minute=arg_dict["minute"],
                second=arg_dict["second"],
                precision=precision,
                tz_offset=arg_dict["tz_offset"]
            )
            expected = Encoder.encode_iso_str(item["iso"])
            with self.subTest(f'{actual} == {expected} for {item["iso"]}'):
                # Make sure we're checking a good encoding
                assert expected == item["encoded"]
                self.assertEqual(expected, actual)
