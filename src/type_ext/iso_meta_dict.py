from typing import TypedDict


class IsoMetaDict(TypedDict):
    """
    A TypedDict for ISO datetime string metadat
    """
    has_date_time: bool
    is_precise: bool
    is_tz_aware: bool


