import unittest
from src.type_ext.temporenc_type import TemporencType


class TestFnAsEncodingType(unittest.TestCase):

    data_provider = [
        (TemporencType.TYPE_D, "D"),
        (TemporencType.TYPE_T, "T"),
        (TemporencType.TYPE_DT, "DT"),
        (TemporencType.TYPE_DTS, "DTS"),
        (TemporencType.TYPE_DTZ, "DTZ"),
        (TemporencType.TYPE_DTSZ, "DTSZ")]

    def test_fn_returns_expected_str(self):
        for i in self.data_provider:
            actual = i[0].as_encoding_type()
            expected = i[1]
            with self.subTest(f'{i[0]}-as_encoding_type() == "{actual}"'):
                self.assertIsInstance(actual, str)
                self.assertEqual(expected, actual)
