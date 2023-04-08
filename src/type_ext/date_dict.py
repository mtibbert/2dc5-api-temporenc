from typing import TypedDict


class DateDict(TypedDict):
    """
    A TypedDict for date components
    """
    year: str | None
    month: str | None
    day: str | None

