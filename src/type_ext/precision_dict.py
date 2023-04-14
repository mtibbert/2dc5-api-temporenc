from typing import TypedDict


class PrecisionDict(TypedDict):
    """
    A TypedDict for precision components
    """
    precision: str | None
    subsecond: str | None

