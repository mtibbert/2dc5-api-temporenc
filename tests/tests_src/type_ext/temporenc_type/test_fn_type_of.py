import unittest
from src.type_ext.temporenc_type import TemporencType


class TestFnTypeOf(unittest.TestCase):

    def test_type_of(self):
        encodings = {
            "800000": TemporencType.TYPE_D,       # 1/1/0000
            "8FCE79": TemporencType.TYPE_D,
            "A10B40": TemporencType.TYPE_T,
            "0000000000": TemporencType.TYPE_DT,  # 1/1/0000 @ 00:00:00
            "1EFC1D264C": TemporencType.TYPE_DT,
            "47C307499300C0": TemporencType.TYPE_DTS,
            "57E73CC2D0078900": TemporencType.TYPE_DTS,
            "67BF074993075BCD15": TemporencType.TYPE_DTS,
            "77BF07499300": TemporencType.TYPE_DTS,
            "CFCE7985A02C": TemporencType.TYPE_DTZ,
            "E3E183A2C9806440": TemporencType.TYPE_DTSZ,
            "EBF39E616803C480B0": TemporencType.TYPE_DTSZ,
            "F3DF83A2C983ADE68AC4": TemporencType.TYPE_DTSZ,
            "FBDF83A2C99100": TemporencType.TYPE_DTSZ
        }
        for encoded, expected in encodings.items():
            with self.subTest(f'"{encoded}" should be TemporencType.{expected.name}'):
                self.assertEqual(expected, TemporencType.type_of(encoded))
