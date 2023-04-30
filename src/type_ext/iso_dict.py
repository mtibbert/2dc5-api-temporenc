from typing import TypedDict
from src.type_ext.iso_components_dict import IsoComponentsDict
from src.type_ext.iso_meta_dict import IsoMetaDict


class IsoDict(TypedDict):
    """
    A TypedDict for ISO datetime strings
    """
    iso: str
    meta: IsoMetaDict
    components: IsoComponentsDict


