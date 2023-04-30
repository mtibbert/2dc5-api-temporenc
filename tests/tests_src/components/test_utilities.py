from datetime import time
from typing import TypedDict, NotRequired
from components.utilities import Utilities
from tests_src.components.parsers.tests_parse_iso_string_base \
    import TestsParseIsoStringBase


class ArgDict(TypedDict):
    """
    A TypedDict
    """
    count: int
    generate_hours: int
    hour_start: NotRequired[int]
    generate_minutes: int
    minute_start: NotRequired[int]
    # seconds: int
    seconds_start: NotRequired[int]
    generate_couplet: int


class TestUtilities(TestsParseIsoStringBase):

    def setUp(self) -> None:
        super().setUp()

    @staticmethod
    def generate_time_strings(arg_dict: ArgDict):
        """

        :param arg_dict:
        :return:

        # >>> arg = {
        # ... "count": 0,
        # ... "hour_start": 23,"generate_hours": 2,
        # ... "minute_start": 58,"generate_minutes": 4,
        # ... "seconds_start": 5, "generate_couplet": 2 }
        # >>> expected =\
        # arg["generate_hours"]*arg["generate_minutes"]*arg["generate_couplet"]
        # >>> len(TestFnIsoDictAsIsoStr.generate_time_strings(arg)) == expected
        # True

        """
        ret_list = []
        arg_dict = {k: abs(v) for k, v in arg_dict.items()}
        # settings = {
        #     "count": 5, "generate_hours": 0, "hour_start": 0, "generate_minutes": 0,
        #     "minute_start": 0, "generate_couplet": 0, "seconds_start": 0}
        if arg_dict["generate_hours"] > 24 or arg_dict["generate_hours"] == 0:
            arg_dict["generate_hours"] = 1
        if arg_dict["hour_start"] > 23 or arg_dict["hour_start"] == 0:
            arg_dict["hour_start"] = 0
        if arg_dict["generate_minutes"] > 60 or arg_dict["generate_minutes"] == 0:
            arg_dict["generate_minutes"] = 1
        if arg_dict["minute_start"] > 60:
            arg_dict["minute_start"] = 0
        if arg_dict["generate_couplet"] > 60:
            arg_dict["generate_couplet"] = 60
        if arg_dict["seconds_start"] > 60:
            arg_dict["seconds_start"] = 0

        # 8600 Tests/day (3+ generate_minutes test time)
        rng_hours = range(arg_dict["hour_start"],
                          arg_dict["hour_start"] + arg_dict["generate_hours"])
        # 3600 test per hour (2.5 generate_couplet test time)
        rng_minutes = range(arg_dict["minute_start"],
                            arg_dict["minute_start"] + arg_dict["generate_minutes"])
        # 60 tests per minute (.05 generate_couplet test time)
        rng_seconds = range(arg_dict["seconds_start"],
                            arg_dict["seconds_start"] + arg_dict["generate_couplet"])
        for h in rng_hours:
            for m in rng_minutes:
                for s in rng_seconds:
                    ret_list.append(f'{str(h%24).zfill(2)}:{str(m%60).zfill(2)}:'
                                    f'{str(s%60).zfill(2)}')
        return ret_list

    def test_is_iso_datetime_str_returns_true_for_datetime_str(self):
        data_provider = ["1983-01-15T18:25:12",
                         "1983-01-15T18:25:12.123",
                         "1983-01-15T18:25:12+01:00",
                         "1983-01-15T18:25:12.123-01:00"]
        for iso_str in data_provider:
            with self.subTest(f'is_iso_datetime_str({iso_str}) is True'):
                self.assertTrue(Utilities.is_iso_datetime_str(iso_str))

    def test_is_iso_time_str_true_for_valid_strings(self):
        args: ArgDict = {
            "count": 0,
            "hour_start": 23,
            "minute_start": 58,
            "seconds_start": 5,
            "generate_hours": 2,
            "generate_minutes": 4,
            "generate_couplet": 2}
        iso_list = TestUtilities.generate_time_strings(args)
        for iso in iso_list:
            with self.subTest(f'{iso[:-6]} | {iso[:-3]} | {iso}'):
                # Test HH format
                self.assertTrue(Utilities.is_iso_time_str(iso[:-6]))
                # Test HH:MM format
                self.assertTrue(Utilities.is_iso_time_str(iso[:-3]))
                # Test HH:MM:SS format
                self.assertTrue(Utilities.is_iso_time_str(iso))

    def test_is_iso_time_str_true_for_valid_strings_t_leading(self):
        rng_hours = range(0, 2)  # Test Hours in the range 0 and 1
        rng_minutes = range(7, 10)  # Test Minutes in the range 7, 8 and 9
        rng_seconds = range(0, 60)  # Test 0-59 generate_couplet
        for h in rng_hours:
            for m in rng_minutes:
                for s in rng_seconds:
                    iso = f'T{str(h).zfill(2)}:{str(m).zfill(2)}:{str(s).zfill(2)}'
                    with self.subTest(f'{iso[:-6]} | {iso[:-3]} | {iso}'):
                        # Test HH:MM:SS format
                        self.assertTrue(Utilities.is_iso_time_str(iso))
                        # Test HH:MM format
                        self.assertTrue(Utilities.is_iso_time_str(iso[:-3]))
                        # Test HH format
                        self.assertTrue(Utilities.is_iso_time_str(iso[:-6]))

    def test_normalize_iso_str_returns_str(self):
        self.assertIsInstance(Utilities.normalize_iso_str("1983-01-15T18:25:12.10"), str)

    def test_normalize_iso_str(self):
        data_provider = [
            {"actual": "1983-01-15T18:25:12.0",
             "expected": "1983-01-15T18:25:12"},
            {"actual": "1983-01-15T18:25:12.10",
             "expected": "1983-01-15T18:25:12.1"},
            {"actual": "1983-01-15T18:25:12.120",
             "expected": "1983-01-15T18:25:12.12"},
            {"actual": "1983-01-15T18:25:12.123",
             "expected": "1983-01-15T18:25:12.123"},
            {"actual": "1983-01-15T18:25:12.1230",
             "expected": "1983-01-15T18:25:12.123"},
            {"actual": "1983-01-15T18:25:12.123400",
             "expected": "1983-01-15T18:25:12.1234"},
            {"actual": "1983-01-15T18:25:12.123450",
             "expected": "1983-01-15T18:25:12.12345"},
            {"actual": "1983-01-15T18:25:12.123456",
             "expected": "1983-01-15T18:25:12.123456"},
            {"actual": "1983-01-15T18:25:12.123456700",
             "expected": "1983-01-15T18:25:12.1234567"},
            {"actual": "1983-01-15T18:25:12.123456780",
             "expected": "1983-01-15T18:25:12.12345678"},
            {"actual": "1983-01-15T18:25:12.123456789",
             "expected": "1983-01-15T18:25:12.123456789"},
            {"actual": "1983-01-15T18:25:12.01",
             "expected": "1983-01-15T18:25:12.01"}]
        for item in data_provider:
            with self.subTest(f'{item["actual"]} is {item["expected"]}'):
                self.assertEqual(item["expected"],
                                 Utilities.normalize_iso_str(item["actual"]))

        actual = Utilities.packb_args_to_iso(year=1983, month=1, day=15,
                                             hour=18, minute=25, second=12,
                                             precision=None, tz_offset=60)
        self.assertIsInstance(actual, str)

    def test_packb_args_to_iso_returns_str(self):
        self.assertIsInstance(Utilities.packb_args_to_iso(
            year=1983, month=1, day=15,
            hour=18, minute=25, second=12, precision=None, tz_offset=60), str)

    def test_packb_args_to_iso(self):
        data_provider = [
            {"actual": {"year": 1983, "month": 1, "day": 15,
                        "hour": None, "minute": None, "second": None,
                        "precision": None, "tz_offset": None},
             "expected": "1983-01-15"},
            {"actual": {"year": None, "month": None, "day": None,
                        "hour": 18, "minute": 25, "second": 12,
                        "precision": None, "tz_offset": None},
             "expected": "18:25:12"},
            {"actual": {"year": 1983, "month": 1, "day": 15,
                        "hour": 18, "minute": 25, "second": 12,
                        "precision": None, "tz_offset": None},
             "expected": "1983-01-15T18:25:12"},
            {"actual": {"year": 1983, "month": 1, "day": 15,
                        "hour": 18, "minute": 25, "second": 12,
                        "precision": 123, "tz_offset": None},
             "expected": "1983-01-15T18:25:12.123"},
            {"actual": {"year": 1983, "month": 1, "day": 15,
                        "hour": 18, "minute": 25, "second": 12,
                        "precision": None, "tz_offset": 60},
             "expected": "1983-01-15T18:25:12+01:00"},
            {"actual": {"year": 1983, "month": 1, "day": 15,
                        "hour": 18, "minute": 25, "second": 12,
                        "precision": 123, "tz_offset": 60},
             "expected": "1983-01-15T18:25:12.123+01:00"},
            {"actual": {"year": 1983, "month": 1, "day": 15,
                        "hour": 18, "minute": 25, "second": None,
                        "precision": None, "tz_offset": None},
             "expected": "1983-01-15T18:25"},
            {"actual": {"year": 1983, "month": 1, "day": 15,
                        "hour": 18, "minute": None, "second": None,
                        "precision": None, "tz_offset": None},
             "expected": "1983-01-15T18"},
            {"actual": {"year": 1983, "month": 1, "day": 15,
                        "hour": None, "minute": None, "second": None,
                        "precision": None, "tz_offset": None},
             "expected": "1983-01-15"},
            {"actual": {"year": 1983, "month": 1, "day": None,
                        "hour": None, "minute": None, "second": None,
                        "precision": None, "tz_offset": None},
             "expected": "1983-01"},
            {"actual": {"year": 1983, "month": None, "day": None,
                        "hour": None, "minute": None, "second": None,
                        "precision": None, "tz_offset": None},
             "expected": "1983"},
        ]
        for item in data_provider:
            with self.subTest(f'expecting {item["expected"]}'):
                actual = Utilities.packb_args_to_iso(
                    year=item["actual"]["year"], month=item["actual"]["month"],
                    day=item["actual"]["day"],
                    hour=item["actual"]["hour"], minute=item["actual"]["minute"],
                    second=item["actual"]["second"],
                    precision=item["actual"]["precision"],
                    tz_offset=item["actual"]["tz_offset"])
                self.assertEqual(item["expected"], actual)

    def test_time_str_to_time_obj_returns_time_obj(self):
        dp = [
            {"iso": "18",
             "time_obj": time(18, 0, 0)},
            {"iso": "18:25",
             "time_obj": time(18, 25, 0)},
            {"iso": "18:25:12",
             "time_obj": time(18, 25, 12)},
            {"iso": "T18:25:12",
             "time_obj": time(18, 25, 12)}]
        for item in dp:
            expected = item["time_obj"]
            actual = Utilities.time_str_to_time_obj(item["iso"])
            with self.subTest(f'"{item["iso"]}" returns the time instance ' +
                              f'{actual.isoformat()}'):
                self.assertIsInstance(actual, time)
                self.assertEqual(expected, actual)
