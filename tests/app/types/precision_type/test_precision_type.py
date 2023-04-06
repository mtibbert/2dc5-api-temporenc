import unittest
from src.types.precision_type import PrecisionType


class TestPrecisionType(unittest.TestCase):

    precision_enum = ["PRECISION_NON_PRECISE", "PRECISION_NONE",
                      "PRECISION_MICROSECOND", "PRECISION_MILLISECOND",
                      "PRECISION_NANOSECOND"]

    def test_expected_members_exist(self):
        for e in self.precision_enum:
            self.assertIsNotNone(PrecisionType[e])

    def test_expected_number_of_members_eq_actual(self):
        self.assertEqual(len(self.precision_enum),
                         len(PrecisionType))

    def test_fn_is_precisely_encoded_w_precise_members(self):
        for m in [PrecisionType.PRECISION_NONE,
                  PrecisionType.PRECISION_MICROSECOND,
                  PrecisionType.PRECISION_MILLISECOND,
                  PrecisionType.PRECISION_NANOSECOND]:
            self.assertTrue(m.is_precisely_encoded())

    def test_fn_is_precisely_encoded_w_non_precise_member(self):
        self.assertFalse(PrecisionType.PRECISION_NON_PRECISE.is_precisely_encoded())
