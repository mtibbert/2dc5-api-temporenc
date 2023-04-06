from enum import Flag


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
