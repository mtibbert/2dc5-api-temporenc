import unittest
from typing import List
from type_ext import IsoDict


class TestsParseIsoStringBase(unittest.TestCase):

    def setUp(self) -> None:
        self.data_provider = {
            "TYPE_D": [
                {"iso": "1983-01-15",
                 "expected": {
                     "iso": "1983-01-15",
                     "meta": {
                         "has_date_time": False,
                         "is_precise": False,
                         "is_tz_aware": False
                     },
                     "components": {
                         "date": {
                             "year": "1983",
                             "month": "01",
                             "day": "15",
                         },
                         "precision": {
                             "precision": "PRECISION_NON_PRECISE",
                             "subsecond": None

                         },
                         "time": {
                             "hour": None,
                             "minute": None,
                             "second": None,
                         },
                         "tz": {
                             "direction": None,
                             "hour": None,
                             "minute": None,
                             "offset": None
                         }
                     }}}],
            "TYPE_T": [
                {"iso": "T18:25:12",
                 "expected": {
                     "iso": "T18:25:12",
                     "meta": {
                         "has_date_time": True,
                         "is_precise": False,
                         "is_tz_aware": False
                     },
                     "components": {
                         "date": {
                             "year": None,
                             "month": None,
                             "day": None,
                         },
                         "precision": {
                             "precision": "PRECISION_NON_PRECISE",
                             "subsecond": None

                         },
                         "time": {
                             "hour": "18",
                             "minute": "25",
                             "second": "12",
                         },
                         "tz": {
                             "direction": None,
                             "hour": None,
                             "minute": None,
                             "offset": None
                         }
                     }}}],
            "TYPE_DT": [
                {"iso": "1983-01-15T18:25:12",
                 "expected": {
                     "iso": "1983-01-15T18:25:12",
                     "meta": {
                         "has_date_time": True,
                         "is_precise": False,
                         "is_tz_aware": False
                     },
                     "components": {
                         "date": {
                             "year": "1983",
                             "month": "01",
                             "day": "15",
                         },
                         "precision": {
                             "precision": "PRECISION_NON_PRECISE",
                             "subsecond": None

                         },
                         "time": {
                             "hour": "18",
                             "minute": "25",
                             "second": "12",
                         },
                         "tz": {
                             "direction": None,
                             "hour": None,
                             "minute": None,
                             "offset": None
                         }
                     }}}],
            "TYPE_DTS": [
                {"iso": "1983-01-15T18:25:12.123",
                 "expected": {
                     "iso": "1983-01-15T18:25:12.123",
                     "meta": {
                         "has_date_time": True,
                         "is_precise": True,
                         "is_tz_aware": False
                     },
                     "components": {
                         "date": {
                             "year": "1983",
                             "month": "01",
                             "day": "15",
                         },
                         "precision": {
                             "precision": "PRECISION_MICROSECOND",
                             "subsecond": "123"

                         },
                         "time": {
                             "hour": "18",
                             "minute": "25",
                             "second": "12",
                         },
                         "tz": {
                             "direction": None,
                             "hour": None,
                             "minute": None,
                             "offset": None
                         }
                     }}},
                {"iso": "1983-01-15T18:25:12.123456",
                 "expected": {
                     "iso": "1983-01-15T18:25:12.123456",
                     "meta": {
                         "has_date_time": True,
                         "is_precise": True,
                         "is_tz_aware": False
                     },
                     "components": {
                         "date": {
                             "year": "1983",
                             "month": "01",
                             "day": "15",
                         },
                         "precision": {
                             "precision": "PRECISION_MILLISECOND",
                             "subsecond": "123456"

                         },
                         "time": {
                             "hour": "18",
                             "minute": "25",
                             "second": "12",
                         },
                         "tz": {
                             "direction": None,
                             "hour": None,
                             "minute": None,
                             "offset": None
                         }
                     }}},
                {"iso": "1983-01-15T18:25:12.123456789",
                 "expected": {
                     "iso": "1983-01-15T18:25:12.456789",
                     "meta": {
                         "has_date_time": True,
                         "is_precise": True,
                         "is_tz_aware": False
                     },
                     "components": {
                         "date": {
                             "year": "1983",
                             "month": "01",
                             "day": "15",
                         },
                         "precision": {
                             "precision": "PRECISION_NANOSECOND",
                             "subsecond": "123456789"

                         },
                         "time": {
                             "hour": "18",
                             "minute": "25",
                             "second": "12",
                         },
                         "tz": {
                             "direction": None,
                             "hour": None,
                             "minute": None,
                             "offset": None
                         }
                     }}},
                {"iso": "1983-01-15T18:25:12.1234567",
                 "expected": {
                     "iso": "1983-01-15T18:25:12.4567",
                     "meta": {
                         "has_date_time": True,
                         "is_precise": True,
                         "is_tz_aware": False
                     },
                     "components": {
                         "date": {
                             "year": "1983",
                             "month": "01",
                             "day": "15",
                         },
                         "precision": {
                             "precision": "PRECISION_NANOSECOND",
                             "subsecond": "1234567"

                         },
                         "time": {
                             "hour": "18",
                             "minute": "25",
                             "second": "12",
                         },
                         "tz": {
                             "direction": None,
                             "hour": None,
                             "minute": None,
                             "offset": None
                         }
                     }}},
            ],
            "TYPE_DTZ": [
                {"iso": "1983-01-15T18:25:12+01:30",
                 "expected": {
                     "iso": "1983-01-15T18:25:12+01:30",
                     "meta": {
                         "has_date_time": True,
                         "is_precise": False,
                         "is_tz_aware": True
                     },
                     "components": {
                         "date": {
                             "year": "1983",
                             "month": "01",
                             "day": "15",
                         },
                         "precision": {
                             "precision": "PRECISION_NON_PRECISE",
                             "subsecond": None

                         },
                         "time": {
                             "hour": "18",
                             "minute": "25",
                             "second": "12",
                         },
                         "tz": {
                             "direction": "+",
                             "hour": "01",
                             "minute": "30",
                             "offset": "90"
                         }
                     }}},
                {"iso": "1983-01-15T18:25:12+01:30",
                 "expected": {
                     "iso": "1983-01-15T18:25:12+01:30",
                     "meta": {
                         "has_date_time": True,
                         "is_precise": False,
                         "is_tz_aware": True
                     },
                     "components": {
                         "date": {
                             "year": "1983",
                             "month": "01",
                             "day": "15",
                         },
                         "precision": {
                             "precision": "PRECISION_NON_PRECISE",
                             "subsecond": None

                         },
                         "time": {
                             "hour": "18",
                             "minute": "25",
                             "second": "12",
                         },
                         "tz": {
                             "direction": "+",
                             "hour": "01",
                             "minute": "30",
                             "offset": "90"
                         }
                     }}},
                {"iso": "1983-01-15T18:25:12+01:30",
                 "expected": {
                     "iso": "1983-01-15T18:25:12+01:30",
                     "meta": {
                         "has_date_time": True,
                         "is_precise": False,
                         "is_tz_aware": True
                     },
                     "components": {
                         "date": {
                             "year": "1983",
                             "month": "01",
                             "day": "15",
                         },
                         "precision": {
                             "precision": "PRECISION_NON_PRECISE",
                             "subsecond": None

                         },
                         "time": {
                             "hour": "18",
                             "minute": "25",
                             "second": "12",
                         },
                         "tz": {
                             "direction": "+",
                             "hour": "01",
                             "minute": "30",
                             "offset": "90"
                         }
                     }}},
            ],
            "TYPE_DTSZ": [
                {"iso": "1983-01-15T18:25:12.123+01:30",
                 "expected": {
                     "iso": "1983-01-15T18:25:12.123+01:30",
                     "meta": {
                         "has_date_time": True,
                         "is_precise": True,
                         "is_tz_aware": True
                     },
                     "components": {
                         "date": {
                             "year": "1983",
                             "month": "01",
                             "day": "15",
                         },
                         "precision": {
                             "precision": "PRECISION_MICROSECOND",
                             "subsecond": "123"

                         },
                         "time": {
                             "hour": "18",
                             "minute": "25",
                             "second": "12",
                         },
                         "tz": {
                             "direction": "+",
                             "hour": "01",
                             "minute": "30",
                             "offset": "90"
                         }
                     }}},
                {"iso": "1983-01-15T18:25:12.123456+01:30",
                 "expected": {
                     "iso": "1983-01-15T18:25:12.123456+01:30",
                     "meta": {
                         "has_date_time": True,
                         "is_precise": True,
                         "is_tz_aware": True
                     },
                     "components": {
                         "date": {
                             "year": "1983",
                             "month": "01",
                             "day": "15",
                         },
                         "precision": {
                             "precision": "PRECISION_MILLISECOND",
                             "subsecond": "123456"

                         },
                         "time": {
                             "hour": "18",
                             "minute": "25",
                             "second": "12",
                         },
                         "tz": {
                             "direction": "+",
                             "hour": "01",
                             "minute": "30",
                             "offset": "90"
                         }
                     }}},
                {"iso": "1983-01-15T18:25:12.123456789+01:30",
                 "expected": {
                     "iso": "1983-01-15T18:25:12.456789+01:30",
                     "meta": {
                         "has_date_time": True,
                         "is_precise": True,
                         "is_tz_aware": True
                     },
                     "components": {
                         "date": {
                             "year": "1983",
                             "month": "01",
                             "day": "15",
                         },
                         "precision": {
                             "precision": "PRECISION_NANOSECOND",
                             "subsecond": "123456789"

                         },
                         "time": {
                             "hour": "18",
                             "minute": "25",
                             "second": "12",
                         },
                         "tz": {
                             "direction": "+",
                             "hour": "01",
                             "minute": "30",
                             "offset": "90"
                         }
                     }}},
                {"iso": "1983-01-15T18:25:12.1234567+01:30",
                 "expected": {
                     "iso": "1983-01-15T18:25:12.4567+01:30",
                     "meta": {
                         "has_date_time": True,
                         "is_precise": True,
                         "is_tz_aware": True
                     },
                     "components": {
                         "date": {
                             "year": "1983",
                             "month": "01",
                             "day": "15",
                         },
                         "precision": {
                             "precision": "PRECISION_NANOSECOND",
                             "subsecond": "1234567"

                         },
                         "time": {
                             "hour": "18",
                             "minute": "25",
                             "second": "12",
                         },
                         "tz": {
                             "direction": "+",
                             "hour": "01",
                             "minute": "30",
                             "offset": "90"
                         }
                     }}},
            ],
        }
        self.sample_iso_dict: IsoDict = {
            "iso": "1983-01-15T18:25:12.123456+01:00",
            "meta": {
                "has_date_time": True,
                "is_precise": True,
                "is_tz_aware": True
            },
            "components": {
                "date": {
                    "year": "1983", "month": "01", "day": "15"},
                "precision": {
                    "precision": "PRECISION_MILLISECOND",
                    "subsecond": "123456"},
                "time": {
                    "hour": "18", "minute": "25", "second": "12"},
                "tz": {
                    "direction": "+",
                    "hour": "01",
                    "minute": "00",
                    "offset": "60"
                }
            }
        }
        self.time_str_list = self.generate_hours()

    # @staticmethod
    # def generate_date_time_list(start_hour: int = 12,
    #                             generate_minutes: int = 2,
    #                             generate_hours: int = 0) -> List[str]:
    #     """
    #
    #     :param start_hour:
    #     :param generate_minutes:
    #     :param generate_hours:
    #     :return:
    #
    #     # >>> TestsParseIsoStringBase.generate_date_time_list(start_hour=23)
    #     # ['23', '2', '0']
    #     # >>> TestsParseIsoStringBase.generate_date_time_list(start_hour=24)
    #     # ['12', '2', '0']
    #     # >>> TestsParseIsoStringBase.generate_date_time_list(start_hour=0)
    #     # ['0', '2', '0']
    #     # >>> TestsParseIsoStringBase.generate_date_time_list(start_hour=-1)
    #     # ['12', '2', '0']
    #     >>> TestsParseIsoStringBase.generate_date_time_list(start_hour=23, generate_hours=2)
    #     ['23', '2', '1']
    #     """
    #     ret_list = []
    #     if start_hour > 23 or start_hour < 0:
    #         start_hour = 12
    #     if start_hour + generate_hours > 24:
    #         generate_hours = 24 - start_hour
    #     if generate_minutes > 60:
    #         generate_minutes = 60
    #     elif generate_minutes < 1:
    #         generate_minutes = 1
    #     ret_list = [str(start_hour), str(generate_minutes), str(generate_hours)]
    #     # generate_couplet: List[str] = []
    #     # for s in range(0, 60):
    #     #     generate_couplet.append(f'{str(s).zfill(2)}')
    #     # mm = range(0, 60)
    #     return ret_list

    @staticmethod
    def generate_couplet(start: int = 0, stop: int = 60, step: int = 1) -> List[str]:
        """
        Generate start two character strings.

        :param start: {int} an integer number specifying at which position to start.
                            Valid range is 0-59, default is 0.
        :param stop:  {int} an integer number specifying at which position to stop.
                            Valid range is 1-60, default is 60.
        :param step:  {int} an integer number greater than zero (0) specifying the
                            incrementation. Default is 1
        :return:

        >>> cls = TestsParseIsoStringBase

        # Valid call(s)
        >>> cls.generate_couplet(22, 25)
        ['22', '23', '24']

        # ValueErrors expected
        >>> cls.generate_couplet(start=60, stop=65, step=-1) #doctest:+ELLIPSIS
        Traceback (most recent call last):
        ...
        V...r: ... start (60) ..., step (-1) ...; ... zero (0) and stop (65) out of range.

        >>> cls.generate_couplet(stop=65, step=-1) # doctest:+ELLIPSIS
        Traceback (most recent call last):
        ...
        ValueError: ... step (-1) out of range; ... (0) and stop (65) out of range.

        >>> cls.generate_couplet(start=-1, stop=61) # doctest:+ELLIPSIS
        Traceback (most recent call last):
        ...
        ValueError: ... start (-1) out of range and stop (61) out of range.

        >>> cls.generate_couplet(start=-1, step=0) # doctest:+ELLIPSIS
        Traceback (most recent call last):
        ...
        ValueError: ... start (-1) out of range and step (0) ... (0).

        >>> cls.generate_couplet(step=0) # doctest:+ELLIPSIS
        Traceback (most recent call last):
        ...
        ValueError: ... step (0) ... expecting an integer number greater than zero (0).

        >>> cls.generate_couplet(start=1, stop=1)
        Traceback (most recent call last):
        ...
        ValueError: Invalid argument(s): stop (1) out of range.

        >>> cls.generate_couplet(1, 1)
        Traceback (most recent call last):
        ...
        ValueError: Invalid argument(s): stop (1) out of range.

        >>> cls.generate_couplet(start=-1)
        Traceback (most recent call last):
        ...
        ValueError: Invalid argument(s): start (-1) out of range.

        """
        ret_list = []
        is_start_arg_valid = (start >= 0) and (start <= 59)
        is_stop_arg_valid = (stop >= 0) and (stop <= 60) and (stop > start)
        is_step_arg_valid = (step > 0)
        is_args_valid = is_start_arg_valid and is_stop_arg_valid and is_step_arg_valid
        if is_args_valid:
            for i in range(start, stop, step):
                ret_list.append(f'{str(i).zfill(2)}')
        else:
            msg = "Invalid argument(s): "
            status = [{str(is_start_arg_valid is False): "start"},
                      {str(is_step_arg_valid is False): "step"},
                      {str(is_stop_arg_valid is False): "stop"}]
            errors = [d["True"] for d in status if "True" in d]
            for i in range(0, len(errors)):
                if i > 0 and (i < len(errors) - 1):
                    msg += ", "
                elif i > 0 and i == len(errors) - 1:
                    msg += " and "
                if errors[i] == "start":
                    msg += f'start ({start}) out of range'
                if errors[i] == "step":
                    msg += f'step ({step}) out of range; ' + \
                           f'expecting an integer number greater than zero (0)'
                if errors[i] == "stop":
                    msg += f'stop ({stop}) out of range'
            msg += "."
            raise ValueError(msg)
        return ret_list

    @staticmethod
    def generate_hours(hour_start: int = 0, hour_stop: int = 1, hour_step: int = 1,
                       min_start: int = 0, min_stop: int = 5, min_step: int = 2,
                       sec_start: int = 0, sec_stop: int = 10, sec_step: int = 3) \
            -> List[str]:
        """
        Generate list of HH:MM:SS strings.

        :param hour_start: {int} an integer number specifying at which position to start.
                                 Valid range is 0-59, default is 0.
        :param hour_stop:  {int} an integer number specifying at which position to stop.
                                 Valid range is 1-60, default is 1.
        :param hour_step:  {int} an integer number greater than zero (0) specifying the
                                 incrementation. Default is 1
        :param min_start: {int}  an integer number specifying at which position to start.
                                 Valid range is 0-59, default is 0.
        :param min_stop:  {int}  an integer number specifying at which position to stop.
                                 Valid range is 1-60, default is 1.
        :param min_step:  {int}  an integer number greater than zero (0) specifying the
                                 incrementation. Default is 1
        :param sec_start: {int}  an integer number specifying at which position to start.
                                 Valid range is 0-59, default is 0.
        :param sec_stop:  {int}  an integer number specifying at which position to stop.
                                 Valid range is 1-60, default is 60.
        :param sec_step:  {int}  an integer number greater than zero (0) specifying the
                                 incrementation. Default is 1
        :return:

        >>> cls = TestsParseIsoStringBase

        # Valid call(s)
        -- Check defaults
        >>> cls.generate_hours() == cls.generate_hours(0, 1, 1, 0, 5, 2, 0, 10, 3)
        True
        >>> l = cls.generate_hours(0, 2, 1, 0, 5, 2, 0, 10, 3)
        >>> len(l) == (int(1/1) + 1) * (int(5/2)+1) * (int(10/3)+1)
        True

        >>> cls.generate_hours(-1, 2, 1, 0, 5, 2, 0, 10, 3) # doctest:+ELLIPSIS
        Traceback (most recent call last):
        ...
        ValueError:...generating hour(s); arguments ... (start=-1, stop=2, step=1)...
        """
        ret_list = []
        try:
            hh = TestsParseIsoStringBase.generate_couplet(hour_start, hour_stop, hour_step)
        except ValueError as ve:
            args_str = f'start={hour_start}, stop={hour_stop}, step={hour_step}'
            msg = f'Error generating hour(s); '
            msg += f'arguments passed were ({args_str}). '
            msg += f'Review stack trace for additional information.'
            raise ValueError(msg) from ve
        try:
            iso = TestsParseIsoStringBase.generate_minutes(
                min_start, min_stop, min_step,
                sec_start, sec_stop, sec_step)
        except ValueError as ve:
            msg = f'Error raised in function generate_minutes(). '
            msg += f'Review stack trace for additional information.'
            raise ValueError(msg) from ve

        for h in hh:
            x = [f'{h}:{i}' for i in iso]
            ret_list += x
        return ret_list

    @staticmethod
    def generate_minutes(min_start: int = 0, min_stop: int = 5, min_step: int = 2,
                         sec_start: int = 0, sec_stop: int = 10, sec_step: int = 3) \
            -> List[str]:
        """
        Generate list of MM:SS strings.

        :param min_start: {int} an integer number specifying at which position to start.
                            Valid range is 0-59, default is 0.
        :param min_stop:  {int} an integer number specifying at which position to stop.
                            Valid range is 1-60, default is 1.
        :param min_step:  {int} an integer number greater than zero (0) specifying the
                            incrementation. Default is 1
        :param sec_start: {int} an integer number specifying at which position to start.
                            Valid range is 0-59, default is 0.
        :param sec_stop:  {int} an integer number specifying at which position to stop.
                            Valid range is 1-60, default is 60.
        :param sec_step:  {int} an integer number greater than zero (0) specifying the
                            incrementation. Default is 1
        :return:

        >>> cls = TestsParseIsoStringBase

        # Valid call(s)
        # -- Check defaults
        >>> cls.generate_minutes() == cls.generate_minutes(0, 5, 2, 0, 10, 3)
        True
        >>> len(cls.generate_minutes(0, 5, 2, 0, 10, 3)) == (int(5/2)+1) * (int(10/3)+1)
        True
        >>> len(cls.generate_minutes()) == (int(5/2)+1) * (int(10/3)+1)
        True
        >>> cls.generate_minutes(0, 5, 2, -1, 10, 3) # doctest:+ELLIPSIS
        Traceback (most recent call last):
        ...
        ValueError: Invalid...seconds; arg...(start=-1, stop=10, step=3). Rev...info...
        >>> cls.generate_minutes(-1, 5, 2, 1, 10, 3) # doctest:+ELLIPSIS
        Traceback (most recent call last):
        ...
        ValueError: Invalid...minutes; arg...(start=-1, stop=5, step=2). Rev...info...
        """
        ret_list = []

        try:
            ss = TestsParseIsoStringBase.generate_couplet(sec_start, sec_stop, sec_step)
        except ValueError as ve:
            args_str = f'start={sec_start}, stop={sec_stop}, step={sec_step}'
            msg = f'Invalid call to generate seconds; '
            msg += f'arguments passed were ({args_str}). '
            msg += f'Review stack trace for additional information.'
            raise ValueError(msg) from ve
        try:
            mm = TestsParseIsoStringBase.generate_couplet(min_start, min_stop, min_step)
        except ValueError as ve:
            args_str = f'start={min_start}, stop={min_stop}, step={min_step}'
            msg = f'Invalid call to generate minutes; '
            msg += f'arguments passed were ({args_str}). '
            msg += f'Review stack trace for additional information.'
            raise ValueError(msg) from ve

        for m in mm:
            x = [f'{str(m).zfill(2)}:{s}' for s in ss]
            ret_list += x
        return ret_list


if __name__ == '__main__':
    unittest.main()
