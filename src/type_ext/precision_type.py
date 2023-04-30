import re
from enum import Flag
from components.utilities import Utilities
from type_ext.temporenc_type import TemporencType


class PrecisionType(Flag):
    """Enumeration related to Temporenc sub-second precision component."""
    PRECISION_NON_PRECISE = 1
    PRECISION_NONE = 2
    PRECISION_MICROSECOND = 4
    PRECISION_MILLISECOND = 8
    PRECISION_NANOSECOND = 16

    @classmethod
    def encoded_to_precision_type(cls, encoded_str: str) -> "PrecisionType":
        """
        Extracts PrecisionType member associated with encoded value.

        NOTE: No validation of encoded_str occurs.

        :param encoded_str: {str}

        :return: PrecisionType
        """

        member = PrecisionType.PRECISION_NON_PRECISE

        temporenc_type = TemporencType.type_of(encoded_str)
        precision_tag = ""

        if temporenc_type.is_precise():
            bin_str = bin(int(encoded_str, 16))[2:]
            if len(bin_str) % 4 != 0:  # Left pad to multiple of 4
                bin_str = bin_str.zfill(len(bin_str) + (4 - len(bin_str) % 4))
            match TemporencType.type_of(encoded_str):
                case TemporencType.TYPE_DTS:
                    # 01PPDDDD - DTS
                    precision_tag = bin_str[2:4]
                case TemporencType.TYPE_DTSZ:
                    # 111PPDDD - DTSZ
                    precision_tag = bin_str[3:5]
            member = PrecisionType.precision_tag_to_precision_type(precision_tag)
        return member

    def is_precisely_encoded(self) -> bool:
        """
        Returns True if PrecisionType member is not PRECISION_NON_PRECISE.

        :return: bool
        """
        return self != PrecisionType.PRECISION_NON_PRECISE

    @classmethod
    def iso_to_precision_type(cls, iso_str: str) -> "PrecisionType":
        """
        Parse an ISO String returning the most efficient precision type. When
        the precision component is in the for ".1230", the trailing zero(s)
        are removed and the resulting precision calculated (millisecond in the
        example).

        :param iso_str: {str} the ISO string to evaluate

        :return: {PrecisionType}
        """
        precision_type = PrecisionType.PRECISION_NON_PRECISE
        normalized_iso = Utilities.normalize_iso_str(iso_str)
        if "." in normalized_iso:
            # Find the length of the precision string
            match = re.search(r"\W", normalized_iso.split(".")[1])
            precision_len = match.start(0) if match \
                else len(normalized_iso.split(".")[1])
            # Use normalized length to find normalized precision type
            match precision_len:
                case 1 | 2 | 3:
                    precision_type = PrecisionType.PRECISION_MILLISECOND
                case 4 | 5 | 6:
                    precision_type = PrecisionType.PRECISION_MICROSECOND
                case 7 | 8 | 9:
                    precision_type = PrecisionType.PRECISION_NANOSECOND

        return precision_type

    def pad(self) -> str:
        """
        Retrieve the encoding precision padding string associated with member.
        Returned values are in the vocabulary ["", "00", "0000", "000000"].

        :return: {str}
        """
        pad_dict = {
            PrecisionType.PRECISION_MILLISECOND.name: "0000",
            PrecisionType.PRECISION_MICROSECOND.name: "00",
            PrecisionType.PRECISION_NANOSECOND.name: "",
            PrecisionType.PRECISION_NONE.name: "000000"}

        tag = pad_dict[PrecisionType.PRECISION_NANOSECOND.name]

        match self:
            case PrecisionType.PRECISION_MILLISECOND:
                tag = "0000"
            case PrecisionType.PRECISION_MICROSECOND:
                tag = "00"
            case PrecisionType.PRECISION_NANOSECOND:
                tag = ""
            case PrecisionType.PRECISION_NONE:
                tag = "000000"
        return tag

    @classmethod
    def pad_to_precision_type(cls, pad_str: str) -> "PrecisionType":
        """
        Retrieve the PrecisionType member associated with pad_str.

        Note: The padding associated with PRECISION_NANOSECOND and PRECISION_NON_PRECISE
                   are an empty string (""). Do not rely upon this function as the sole
                   means of identifying precision granularity.

        :param pad_str: {str}

        :return: {PrecisionType}
        """

        precision_type = PrecisionType.PRECISION_NANOSECOND

        precision_type_dict = {
            "0000": PrecisionType.PRECISION_MILLISECOND,
            "00": PrecisionType.PRECISION_MICROSECOND,
            "000000": PrecisionType.PRECISION_NONE}
        if pad_str in precision_type_dict:
            precision_type = precision_type_dict[pad_str]
        elif pad_str == "":
            precision_type = PrecisionType.PRECISION_NANOSECOND

        return precision_type

    def precision_tag(self) -> str:
        """
        Retrieve the encoding precision tag associated with member. Returned values
        are in the vocabulary ["", "00", "01", "10", "11"].

        :return: {str}
        """
        tag = ""
        match self:
            case PrecisionType.PRECISION_MILLISECOND:
                tag = "00"
            case PrecisionType.PRECISION_MICROSECOND:
                tag = "01"
            case PrecisionType.PRECISION_NANOSECOND:
                tag = "10"
            case PrecisionType.PRECISION_NONE:
                tag = "11"
        return tag

    @classmethod
    def precision_tag_to_precision_type(cls, precision_tag: str) -> "PrecisionType":
        """
        Retrieve the PrecisionType member associated with precision tag.

        :param precision_tag: {str}

        :return: {PrecisionType}
        """
        member = PrecisionType.PRECISION_NON_PRECISE
        match precision_tag:
            case "00":
                member = PrecisionType.PRECISION_MILLISECOND
            case "01":
                member = PrecisionType.PRECISION_MICROSECOND
            case "10":
                member = PrecisionType.PRECISION_NANOSECOND
            case "11":
                member = PrecisionType.PRECISION_NONE
        return member
