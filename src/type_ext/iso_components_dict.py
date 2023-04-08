from typing import TypedDict
from src.type_ext.date_dict import DateDict
from src.type_ext.precision_dict import PrecisionDict
from src.type_ext.time_dict import TimeDict
from src.type_ext.tz_dict import TzDict


class IsoComponentsDict(TypedDict):
    """
    A TypedDict for ISO string date, time, precision and timezone metadata
    """
    date: DateDict
    precision: PrecisionDict
    time: TimeDict
    tz: TzDict


