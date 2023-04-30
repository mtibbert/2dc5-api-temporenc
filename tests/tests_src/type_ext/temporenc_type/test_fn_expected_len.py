import unittest
from src.type_ext.temporenc_type import TemporencType
from type_ext import PrecisionType


class TestFnLen(unittest.TestCase):

    data_provider = {
        "non-precise": {
            TemporencType.TYPE_D: 6,
            TemporencType.TYPE_T: 6,
            TemporencType.TYPE_DT: 10,
            TemporencType.TYPE_DTZ: 12},
        "precise": {
            TemporencType.TYPE_DTS: {
                PrecisionType.PRECISION_MILLISECOND: 14,
                PrecisionType.PRECISION_MICROSECOND: 16,
                PrecisionType.PRECISION_NANOSECOND: 18,
                PrecisionType.PRECISION_NONE: 12},
            TemporencType.TYPE_DTSZ: {
                PrecisionType.PRECISION_MILLISECOND: 16,
                PrecisionType.PRECISION_MICROSECOND: 18,
                PrecisionType.PRECISION_NANOSECOND: 20,
                PrecisionType.PRECISION_NONE: 14},
        }
    }

    def test_fn_len_for_non_precise_types(self):
        for k, v in self.data_provider["non-precise"].items():
            actual = k.expected_len()
            expected = v
            with self.subTest(f'{k.name} expected_len() is "{expected}"'):
                self.assertIsInstance(actual, int)
                self.assertEqual(expected, actual)

    def test_fn_len_for_precise_types(self):
        for k, v in self.data_provider["precise"].items():
            for p, length in self.data_provider["precise"][k].items():
                actual = k.expected_len(precision=str(p.name))
                expected = length
                with self.subTest(f'{k.name} ({p.name}) expected_len() is "{expected}"'):
                    self.assertIsInstance(actual, int)
                    self.assertEqual(expected, actual)

    def test_fn_len_for_precise_types_default_arg(self):
        default_precision = "PRECISION_NANOSECOND"
        for k, v in self.data_provider["precise"].items():
            expected = k.expected_len(precision=default_precision)
            for p, length in self.data_provider["precise"][k].items():
                actual = k.expected_len()
                with self.subTest(f'{k.name} ({p.name}) at default precision length is '
                                  f'"{expected}"'):
                    self.assertEqual(expected, actual)
