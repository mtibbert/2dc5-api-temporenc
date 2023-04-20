from unittest import TestCase

from components.parsers.parse_iso_strings import Parse
from components.temporenc.encoder import Encoder
from type_ext import temporenc_arg_dict, IsoDict, PrecisionType

from type_ext.temporenc_arg_dict import TemporencArgDict


class TestEncoder(TestCase):

    data_provider = {}

    def setUp(self) -> None:
        data = {
            "TYPE_DTS": [
                {"iso": "1983-01-15T18:25:12.123",
                 "encoded": "47BF07499307B0"},
                {"iso": "1983-01-15T18:25:12.123456",
                 "encoded": "57BF074993078900"},
                {"iso": "1983-01-15T18:25:12.123456789",
                 "encoded": "67BF074993075BCD15"}]
        }
        self.data_provider = data["TYPE_DTS"]

    def test_encode_arg_dict_returns_uppercase_str(self):
        for item in self.data_provider:
            iso_str = item["iso"]
            iso_dict: IsoDict = Parse.iso_to_iso_dict(iso_str)
            arg_dict: TemporencArgDict = self.iso_dict_to_arg_dict(iso_dict)
            actual = Encoder.encode_arg_dict(arg_dict)
            with self.subTest(f'{iso_str} encodes to {actual}'):
                self.assertIsInstance(actual, str)
                self.assertEqual(actual.upper(), actual)

    # noinspection PyTypedDict
    @classmethod
    def iso_dict_to_arg_dict(cls, iso_dict: IsoDict):
        arg_dict: TemporencArgDict = temporenc_arg_dict.factory()
        if (iso_dict["components"]["date"] is not None or
                iso_dict["components"]["date"] is not None):
            if iso_dict["components"]["date"] is not None:
                arg_dict["year"] = iso_dict["components"]["date"]["year"]
                arg_dict["month"] = iso_dict["components"]["date"]["month"]
                arg_dict["day"] = iso_dict["components"]["date"]["day"]
            if iso_dict["components"]["time"] is not None:
                arg_dict["hour"] = iso_dict["components"]["time"]["hour"]
                arg_dict["minute"] = iso_dict["components"]["time"]["minute"]
                arg_dict["second"] = iso_dict["components"]["time"]["second"]
            if iso_dict["components"]["precision"] is not None:
                precision = iso_dict["components"]["precision"]["precision"]
                if precision == PrecisionType.PRECISION_MICROSECOND.name:
                    arg_dict["microsecond"] = \
                        int(iso_dict["components"]["precision"]["subsecond"])
                    arg_dict["millisecond"] = None
                    arg_dict["nanosecond"] = None
                if precision == PrecisionType.PRECISION_MILLISECOND.name:
                    arg_dict["millisecond"] = \
                        int(iso_dict["components"]["precision"]["subsecond"])
                    arg_dict["microsecond"] = None
                    arg_dict["nanosecond"] = None
                if precision == PrecisionType.PRECISION_NANOSECOND.name:
                    arg_dict["nanosecond"] = \
                        int(iso_dict["components"]["precision"]["subsecond"])
                    arg_dict["microsecond"] = None
                    arg_dict["millisecond"] = None
            if iso_dict["components"]["tz"]["offset"] is not None:
                arg_dict["tz_offset"] = int(iso_dict["components"]["tz"]["offset"])
        arg_dict = ({k: v for k, v in arg_dict.items() if v is None} |
                    {k: int(v) for k, v in arg_dict.items() if v is not None})
        return arg_dict

    # def test_encode_arg_dict_returns_uppercase_str(self):
    #     iso_str = "1983-01-15T18:25:12.123456"
    #     iso_dict: IsoDict = Parse.iso_to_iso_dict(iso_str)
    #     arg_dict: TemporencArgDict = temporenc_arg_dict.factory()
    #     actual = Encoder.encode_arg_dict(arg_dict)
    #     expected = "57BF074993078900"
    #     self.assertEqual(expected, actual)
