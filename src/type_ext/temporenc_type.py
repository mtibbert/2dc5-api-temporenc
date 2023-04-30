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

    def as_encoding_type(self) -> str:
        """
        Cast instance to corresponding Temporenc encoding string.

        :return: {str}

        >>> TemporencType.TYPE_DT.as_encoding_type() == "DT"
        True

        """
        return self.name.replace("TYPE_", "")

    def expected_len(self, precision: str = "PRECISION_NANOSECOND") -> int:
        """
        Return the expected length of the TemporencType member. For types with a
        precision component, the longest encoding (nanosecond) is returned.

        :param precision: (str) specified precision length (default PRECISION_NANOSECOND)

        :return: {int}
        """
        ret_length = 0
        match self:
            case TemporencType.TYPE_D:
                ret_length = 6
            case TemporencType.TYPE_T:
                ret_length = 6
            case TemporencType.TYPE_DT:
                ret_length = 10
            case TemporencType.TYPE_DTZ:
                ret_length = 12
            case TemporencType.TYPE_DTS:
                match precision:
                    case "PRECISION_MILLISECOND":
                        ret_length = 14
                    case "PRECISION_MICROSECOND":
                        ret_length = 16
                    case "PRECISION_NANOSECOND":
                        ret_length = 18
                    case "PRECISION_NONE":
                        ret_length = 12
            case TemporencType.TYPE_DTSZ:
                match precision:
                    case "PRECISION_MILLISECOND":
                        ret_length = 16
                    case "PRECISION_MICROSECOND":
                        ret_length = 18
                    case "PRECISION_NANOSECOND":
                        ret_length = 20
                    case "PRECISION_NONE":
                        ret_length = 14
        return ret_length

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

    @classmethod
    def list_encoding_types(cls) -> List[str]:
        l: List[str] = [member.as_encoding_type()
                        for name, member in TemporencType.__members__.items()]
        return l

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
    def type_of(cls, encoded: str) -> "TemporencType":
        """
        Return TemporencType of the encoded string.

        NOTE: The candidate string is not validated.

        Returns: {TemporencType | None:} returns the TemporencType found
        """

        # noinspection PyUnusedLocal
        return_member = None

        bin_str = bin(int(encoded, 16))[2:]
        # Add leading zeros for types DT and DTS
        pad = "0000"[0:(4-(len(bin_str) % 4))] if (len(bin_str) % 4) > 0 else ""
        candidate = f'{pad}{bin_str}'

        match candidate[:3]:
            case "100":
                return_member = TemporencType.TYPE_D
            case "101":
                return_member = TemporencType.TYPE_T
            case "110":
                return_member = TemporencType.TYPE_DTZ
            case "111":
                return_member = TemporencType.TYPE_DTSZ
            case _:
                return_member = TemporencType.TYPE_DT \
                    if candidate[:2] == "00" else TemporencType.TYPE_DTS

        return return_member

    @classmethod
    def tz_aware_list(cls) -> List["TemporencType"]:
        """
        Return a list of TemporencType members that are timezone aware.

        Returns: Iterable["TemporencType"]
        """
        return [cls.TYPE_DTZ, cls.TYPE_DTSZ]
