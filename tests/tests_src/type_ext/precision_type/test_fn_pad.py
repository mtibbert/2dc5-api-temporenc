import unittest
from src.type_ext.precision_type import PrecisionType


class TestFnPad(unittest.TestCase):

    dataprovider = {}

    def setUp(self) -> None:
        self.dataprovider = {
            PrecisionType.PRECISION_MILLISECOND: "0000",
            PrecisionType.PRECISION_MICROSECOND: "00",
            PrecisionType.PRECISION_NANOSECOND: "",
            PrecisionType.PRECISION_NONE: "000000"}

    def test_fn_pad(self):
        for arg, expected in self.dataprovider.items():
            with self.subTest(f'{arg.name} pad() == "{expected}"'):
                actual = PrecisionType.pad(arg)
                self.assertIsInstance(actual, str)
                self.assertEqual(expected, actual)

    def test_fn_pad_to_precision_type(self):
        for expected, arg in self.dataprovider.items():
            with self.subTest(f'"{arg}" returns PrecisionType "{expected}"'):
                actual = PrecisionType.pad_to_precision_type(arg)
                self.assertIsInstance(actual, PrecisionType)
                self.assertEqual(expected, actual)
