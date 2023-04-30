import datetime
from typing import TypedDict, Literal


class TemporencArgDict(TypedDict):
    value: datetime.datetime | datetime.date | datetime.time | None
    type:  Literal["D", "T", "DT", "DTS", "DTZ", "DTSZ"] | None
    year: int | None
    month: int | None
    day: int | None
    hour: int | None
    minute: int | None
    second: int | None
    millisecond: int | None
    microsecond: int | None
    nanosecond: int | None
    tz_offset: int | None


def factory() -> "TemporencArgDict":
    return TemporencArgDict(value=None, type=None, year=None,
                            month=None, day=None, hour=None,
                            minute=None, second=None,
                            millisecond=None, microsecond=None,
                            nanosecond=None, tz_offset=None)
