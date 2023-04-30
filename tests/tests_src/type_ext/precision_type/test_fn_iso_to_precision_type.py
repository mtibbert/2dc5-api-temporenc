import unittest
from src.type_ext.precision_type import PrecisionType


class TestFnIsoToPrecisionType(unittest.TestCase):
    def test_fn_iso_to_precision_type_for_type_dts(self):
        iso_prefix = "1983-01-15T18:25:12"
        precision_components = {PrecisionType.PRECISION_MILLISECOND: ".010",
                                PrecisionType.PRECISION_MICROSECOND: ".12354",
                                PrecisionType.PRECISION_NANOSECOND: ".87654321"}
        for expected, arg in precision_components.items():
            iso = f'{iso_prefix}{arg}'
            with self.subTest(f'iso_to_precision_type("{iso}") is '
                              f'PrecisionType {expected.name}"'):
                actual = PrecisionType.iso_to_precision_type(iso)
                self.assertIsInstance(actual, PrecisionType)
                self.assertEqual(expected, actual)

    def test_fn_iso_to_precision_type_for_type_dtsz(self):
        iso_prefix = "1983-01-15T18:25:12"
        tz = "+01:00"
        precision_components = {PrecisionType.PRECISION_MILLISECOND: ".010",
                                PrecisionType.PRECISION_MICROSECOND: ".12354",
                                PrecisionType.PRECISION_NANOSECOND: ".87654321"}
        for expected, arg in precision_components.items():
            iso = f'{iso_prefix}{arg}{tz}'
            with self.subTest(f'iso_to_precision_type("{iso}") is '
                              f'PrecisionType {expected.name}"'):
                actual = PrecisionType.iso_to_precision_type(iso)
                self.assertIsInstance(actual, PrecisionType)
                self.assertEqual(expected, actual)

    def test_fn_iso_to_precision_type_removes_trailing_zeros(self):
        iso_prefix = "1983-01-15T18:25:12"
        tz = "+01:00"
        precision_components = {PrecisionType.PRECISION_MILLISECOND: ".010000",
                                PrecisionType.PRECISION_MICROSECOND: ".1235400",
                                PrecisionType.PRECISION_NON_PRECISE: ".0"}
        for expected, arg in precision_components.items():
            iso = f'{iso_prefix}{arg}{tz}'
            with self.subTest(f'iso_to_precision_type("{iso}") is '
                              f'PrecisionType {expected.name}"'):
                actual = PrecisionType.iso_to_precision_type(iso)
                self.assertIsInstance(actual, PrecisionType)
                self.assertEqual(expected, actual)
