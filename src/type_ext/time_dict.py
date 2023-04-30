from typing import TypedDict


class TimeDict(TypedDict):
    """
    A TypedDict for time components
    """
    hour: str | None
    minute: str | None
    second: str | None

