import unittest
from src.types.temporenc_type import TemporencType


class TestTemporencType(unittest.TestCase):

    type_enum = ["TYPE_D", "TYPE_T", "TYPE_DT",
                 "TYPE_DTS", "TYPE_DTZ", "TYPE_DTSZ"]

    def test_class_method_precise_list_has_precision_members(self):
        expected = [TemporencType.TYPE_DTS, TemporencType.TYPE_DTSZ]
        actual = TemporencType.precision_list()
        self.assertEqual(expected, actual)
        pass

    def test_class_method_precise_list_has_two_items(self):
        expected = [TemporencType.TYPE_DTS, TemporencType.TYPE_DTSZ]
        actual = TemporencType.precision_list()
        self.assertEqual(len(expected), len(actual))

    def test_class_method_tz_aware_list_has_tz_aware_members(self):
        expected = [TemporencType.TYPE_DTZ, TemporencType.TYPE_DTSZ]
        actual = TemporencType.tz_aware_list()
        self.assertEqual(expected, actual)
        pass

    def test_class_method_tz_aware_list_has_two_items(self):
        expected = [TemporencType.TYPE_DTZ, TemporencType.TYPE_DTSZ]
        actual = TemporencType.tz_aware_list()
        self.assertEqual(len(expected), len(actual))

    def test_expected_members_exist(self):
        for e in self.type_enum:
            actual = TemporencType[e]
            self.assertIsNotNone(actual)

    def test_expected_number_of_members_eq_actual(self):
        self.assertEqual(len(self.type_enum),
                         len(TemporencType))

    def test_fn_is_precise_w_non_precise_members(self):
        for m in [TemporencType.TYPE_D, TemporencType.TYPE_T,
                  TemporencType.TYPE_DT, TemporencType.TYPE_DTZ]:
            self.assertFalse(m.is_precise())

    def test_fn_is_precise_w_type_dts_member(self):
        self.assertTrue(TemporencType.TYPE_DTS.is_precise())

    def test_fn_is_precise_w_type_dtsz_member(self):
        self.assertTrue(TemporencType.TYPE_DTSZ.is_precise())

    def test_fn_is_tz_aware_w_non_tz_aware_members(self):
        for m in [TemporencType.TYPE_D, TemporencType.TYPE_T,
                  TemporencType.TYPE_DT, TemporencType.TYPE_DTS]:
            self.assertFalse(m.is_tz_aware())

    def test_fn_is_tz_aware_w_type_dtz_member(self):
        self.assertTrue(TemporencType.TYPE_DTZ.is_tz_aware())

    def test_fn_is_tz_aware_w_type_dtsz_member(self):
        self.assertTrue(TemporencType.TYPE_DTSZ.is_tz_aware())
