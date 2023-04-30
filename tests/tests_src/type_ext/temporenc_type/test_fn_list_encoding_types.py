import unittest
from src.type_ext.temporenc_type import TemporencType


class TestFnListEncodingTypes(unittest.TestCase):

    expected = ["D", "T", "DT", "DTS", "DTZ", "DTSZ"]

    def test_returns_expected_list_of_str(self):
        actual = TemporencType.list_encoding_types()
        self.assertEqual(self.expected, actual)

    def test_list_contains_only_uppercase_str(self):
        actual = TemporencType.list_encoding_types()
        for i in actual:
            with self.subTest(i):
                self.assertIsInstance(i, str)
                self.assertEqual(i.upper(), i)
