import typing
from enum import Flag
from typing import List


class TemporencType(Flag):
    """Enumeration related to Temporenc types."""
    TYPE_D = 1
    TYPE_T = 2
    TYPE_DT = 4
    TYPE_DTS = 8
    TYPE_DTZ = 16
    TYPE_DTSZ = 32

    @classmethod
    def precision_list(cls) -> List["TemporencType"]:
        """
        Return a list of TemporencType members containing a sub-second
        component.

        Note: The Temporenc specification defines microsecond (.123),
              millisecond (.123456), nanosecond (.123456789), and none as
              sub-second components.

        Returns: Iterable["TemporencType"]
        """
        return [cls.TYPE_DTS, cls.TYPE_DTSZ]

    @classmethod
    def tz_aware_list(cls) -> List["TemporencType"]:
        """
        Return a list of TemporencType members that are timezone aware.

        Returns: Iterable["TemporencType"]
        """
        return [cls.TYPE_DTZ, cls.TYPE_DTSZ]

    @classmethod
    def list_encoding_types(cls) -> List[str]:
        l: List[str] = [member.as_encoding_type()
                        for name, member in TemporencType.__members__.items()]
        return l

    def as_encoding_type(self) -> str:
        """
        Cast instance to corresponding Temporenc encoding string.

        :return: {str}

        >>> TemporencType.TYPE_DT.as_encoding_type() == "DT"
        True

        """
        return self.name.replace("TYPE_", "")

    def is_precise(self) -> bool:
        """
        Returns True if TemporencType member contains a sub-second
        component.

        :return: bool
        """
        return self in self.precision_list()

    def is_tz_aware(self) -> bool:
        """
        Returns True if TemporencType member is timezone aware.

        :return: bool
        """
        return self in self.tz_aware_list()


# TemporencEncodingType = typing.TypeVar('TemporencEncodingType', bound=TemporencType)

