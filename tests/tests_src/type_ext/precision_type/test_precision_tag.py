import unittest
from src.type_ext.precision_type import PrecisionType


class TestPrecisionTag(unittest.TestCase):

    dataprovider = {}

    def setUp(self) -> None:
        self.dataprovider = {
            PrecisionType.PRECISION_MILLISECOND.name: "00",
            PrecisionType.PRECISION_MICROSECOND.name: "01",
            PrecisionType.PRECISION_NANOSECOND.name: "10",
            PrecisionType.PRECISION_NONE.name: "11",
            PrecisionType.PRECISION_NON_PRECISE.name: ""}

    def test_encoded_to_precision_type(self):
        data_provider = {
            "PRECISION_MILLISECOND": [
                "47 bf 07 49 93 07 b0", "e3 df 83 a2 c9 83 dc 40"],
            "PRECISION_MICROSECOND": [
                "57 bf 07 49 93 07 89 00", "eb df 83 a2 c9 83 c4 81 10"],
            "PRECISION_NANOSECOND": [
                "67 bf 07 49 93 07 5b cd 15", "f3 df 83 a2 c9 83 ad e6 8a c4"],
            "PRECISION_NONE": [
                "77 bf 07 49 93 00", "fb df 83 a2 c9 91 00"],
            "PRECISION_NON_PRECISE": [
                "8f 7e 0e", "a1 26 4c", "1e fc 1d 26 4c", "cf 7e 0e 8b 26 44"]
        }
        for expected_name, values in data_provider.items():
            for v in values:
                encoded = v.replace(" ", "").upper()
                with self.subTest(f'Check {encoded} is PrecisionType {expected_name} '):
                    actual = PrecisionType.encoded_to_precision_type(encoded)
                    self.assertIsInstance(actual, PrecisionType)
                    self.assertEqual(PrecisionType[expected_name], actual)

    def test_fn_precision_tag(self):
        for arg, expected in self.dataprovider.items():
            with self.subTest(f'PrecisionType {arg} ' +
                              f'precision_tag() == "{arg}"'):
                # noinspection PyTypeChecker
                actual = PrecisionType[arg].precision_tag()
                self.assertIsInstance(actual, str)
                self.assertEqual(expected, actual)

    def test_fn_precision_tag_to_precision_type(self):
        for expected, arg in self.dataprovider.items():
            with self.subTest(f'Precision tag "{arg}" ' +
                              f'returns PrecisionType {expected}'):
                actual = PrecisionType.precision_tag_to_precision_type(arg)
                self.assertIsInstance(actual, PrecisionType)
                # noinspection PyTypeChecker
                self.assertEqual(PrecisionType[expected], actual)
