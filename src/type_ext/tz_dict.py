from typing import TypedDict


class TzDict(TypedDict):
    """
    A TypedDict for timezone components
    """
    direction: str | None
    hour: str | None
    minute: str | None
    offset: str | None

