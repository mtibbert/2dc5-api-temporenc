from unittest import TestCase
from components.parsers.parse_iso_strings import Parse
from components.temporenc import Encoder, Utilities
from type_ext import IsoDict
from type_ext.temporenc_arg_dict import TemporencArgDict


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
                {"iso": "1983-01-15T18:25:12.123456789",
                 "encoded": "67BF074993075BCD15"},
                {"iso": "2023-03-28T17:27:00.123420",
                 "encoded": "57E72DC5B0078870"}, ],
            "TYPE_DTZ": [
                {"iso": "1983-01-15T18:25:12+01:00",
                 "encoded": "CF7E0E8B2644"}],  # Doc has CF7E0E8B2644
            "TYPE_DTSZ": [
                {"iso": "1983-01-15T18:25:12.123456789+01:00",
                 "encoded": "F3DF83A2C983ADE68AC4"}, ],
        }
        self.data_provider = (data["TYPE_D"] + data["TYPE_T"] +
                              data["TYPE_DT"] + data["TYPE_DTS"]
                              # data["TYPE_DTZ"] + data["TYPE_DTSZ"]
                              )

    def test_encode_arg_dict_returns_expected_value(self):
        for item in self.data_provider:
            expected = item["encoded"]
            iso_str = item["iso"]
            iso_dict: IsoDict = Parse.iso_to_iso_dict(iso_str)
            arg_dict: TemporencArgDict = Utilities.iso_dict_to_arg_dict(iso_dict)
            actual = Encoder.encode_arg_dict(arg_dict)
            with self.subTest(f'{actual} == {expected} for {iso_str}'):
                self.assertEqual(expected, actual)

    def test_encode_arg_dict_returns_uppercase_str(self):
        for item in self.data_provider:
            iso_str = item["iso"]
            iso_dict: IsoDict = Parse.iso_to_iso_dict(iso_str)
            arg_dict: TemporencArgDict = Utilities.iso_dict_to_arg_dict(iso_dict)
            actual = Encoder.encode_arg_dict(arg_dict)
            with self.subTest(f'{iso_str} encodes to {actual}'):
                self.assertIsInstance(actual, str)
                self.assertEqual(actual.upper(), actual)

    # noinspection PyTypedDict
    # @classmethod
    # def iso_dict_to_arg_dict(cls, iso_dict: IsoDict):
    #     arg_dict: TemporencArgDict = temporenc_arg_dict.factory()
    #     if (iso_dict["components"]["date"] is not None or
    #             iso_dict["components"]["date"] is not None):
    #         if iso_dict["components"]["date"] is not None:
    #             arg_dict["year"] = iso_dict["components"]["date"]["year"]
    #             arg_dict["month"] = iso_dict["components"]["date"]["month"]
    #             arg_dict["day"] = iso_dict["components"]["date"]["day"]
    #         if iso_dict["components"]["time"] is not None:
    #             arg_dict["hour"] = iso_dict["components"]["time"]["hour"]
    #             arg_dict["minute"] = iso_dict["components"]["time"]["minute"]
    #             arg_dict["second"] = iso_dict["components"]["time"]["second"]
    #         if iso_dict["components"]["precision"] is not None:
    #             precision = iso_dict["components"]["precision"]["precision"]
    #             if precision == PrecisionType.PRECISION_MICROSECOND.name:
    #                 arg_dict["microsecond"] = \
    #                     int(iso_dict["components"]["precision"]["subsecond"])
    #                 arg_dict["millisecond"] = None
    #                 arg_dict["nanosecond"] = None
    #             if precision == PrecisionType.PRECISION_MILLISECOND.name:
    #                 arg_dict["millisecond"] = \
    #                     int(iso_dict["components"]["precision"]["subsecond"])
    #                 arg_dict["microsecond"] = None
    #                 arg_dict["nanosecond"] = None
    #             if precision == PrecisionType.PRECISION_NANOSECOND.name:
    #                 arg_dict["nanosecond"] = \
    #                     int(iso_dict["components"]["precision"]["subsecond"])
    #                 arg_dict["microsecond"] = None
    #                 arg_dict["millisecond"] = None
    #         if iso_dict["components"]["tz"]["offset"] is not None:
    #             arg_dict["tz_offset"] = int(iso_dict["components"]["tz"]["offset"])
    #     arg_dict = ({k: v for k, v in arg_dict.items() if v is None} |
    #                 {k: int(v) for k, v in arg_dict.items() if v is not None})
    #     return arg_dict

    # def test_encode_arg_dict_returns_uppercase_str(self):
    #     iso_str = "1983-01-15T18:25:12.123456"
    #     iso_dict: IsoDict = Parse.iso_to_iso_dict(iso_str)
    #     arg_dict: TemporencArgDict = temporenc_arg_dict.factory()
    #     actual = Encoder.encode_arg_dict(arg_dict)
    #     expected = "57BF074993078900"
    #     self.assertEqual(expected, actual)
