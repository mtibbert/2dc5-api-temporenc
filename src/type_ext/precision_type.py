import re
from enum import Flag
from components.utilities import Utilities


class PrecisionType(Flag):
    """Enumeration related to Temporenc sub-second precision component."""
    PRECISION_NON_PRECISE = 1
    PRECISION_NONE = 2
    PRECISION_MICROSECOND = 4
    PRECISION_MILLISECOND = 8
    PRECISION_NANOSECOND = 16

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
