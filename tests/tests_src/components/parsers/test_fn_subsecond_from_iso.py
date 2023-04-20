import unittest
from tests_src.components.parsers.tests_parse_iso_string_base \
    import TestsParseIsoStringBase
from components.parsers.parse_iso_strings import Parse
from type_ext import PrecisionType


class TestFnSubsecondFromIso(TestsParseIsoStringBase):

    def setUp(self) -> None:
        super().setUp()

    def test_component_precision_identified_precision_type(self):
        dp_keys = [k for k in self.data_provider.keys() if "TS" in k]
        for type_key in dp_keys:
            for item in self.data_provider[type_key]:
                with self.subTest(item['iso']):
                    d = Parse.iso_to_iso_dict(f'{item["iso"]}')
                    actual = d["components"]["precision"]
                    expected = item["expected"]["components"]["precision"]
                    if len(actual["subsecond"]) == 0:
                        self.assertEqual(None, actual["precision"])
                    elif len(actual["subsecond"]) < 4:
                        self.assertEqual(PrecisionType.PRECISION_MILLISECOND.name,
                                         actual["precision"])
                    elif len(actual["subsecond"]) < 7:
                        self.assertEqual(PrecisionType.PRECISION_MICROSECOND.name,
                                         actual["precision"])
                    elif len(actual["subsecond"]) < 10:
                        self.assertEqual(PrecisionType.PRECISION_NANOSECOND.name,
                                         actual["precision"])
                    self.assertEqual(expected["precision"], actual["precision"])
                    self.assertEqual(expected["subsecond"], actual["subsecond"])


if __name__ == '__main__':
    unittest.main()
