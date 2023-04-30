from datetime import datetime, timedelta, timezone, date, time
from temporenc import temporenc
from type_ext import TemporencType


class Decoder:

    @classmethod
    def decode(cls, hex_str: str) -> datetime | date | time:
        """
        Decode hex string to datetime, date, or time object

        :param hex_str: {str} hex string to decode

        :return: datetime | date | time
        """
        match TemporencType.type_of(hex_str):
            case TemporencType.TYPE_D:
                ret_obj = cls.as_date(hex_str)
            case TemporencType.TYPE_T:
                ret_obj = cls.as_time(hex_str)
            case _:
                ret_obj = cls.as_date_time(hex_str)
        return ret_obj

    @classmethod
    def as_date(cls, hex_str: str) -> date:
        """
        Decode hex string as date object

        :param hex_str: {str} hex string to decode
        :raise: {ValueError} if hex_str invalid or does not have a date component

        :return: date
        """
        if cls.encoded_is_valid(hex_str) \
                and TemporencType.type_of(hex_str) != TemporencType.TYPE_T:
            m = cls.unpackb(hex_str)    # Decode
            d_obj = m.date()            # Extract date
        else:
            raise ValueError(f'"{hex_str}" not recognized ' +
                             f'as {TemporencType.TYPE_D.name}')
        return d_obj

    @classmethod
    def as_date_time(cls, hex_str: str) -> datetime:
        """
        Decode hex string as datetime object

        :param hex_str: {str} hex string to decode
        :raise: {ValueError} if hex_str invalid or does not have a date or time component

        :return: datetime
        """
        if cls.encoded_is_valid(hex_str) \
                and TemporencType.type_of(hex_str) != TemporencType.TYPE_D \
                and TemporencType.type_of(hex_str) != TemporencType.TYPE_T:
            m = cls.unpackb(hex_str)    # Decode
            if m.tz_offset is None:     # Naive
                dto = m.datetime()
            else:                       # TZ Aware
                time_delta = timedelta(minutes=m.tz_offset)
                tzo = timezone(time_delta, name="Origin")
                dto = m.datetime().astimezone(tzo)
        else:
            raise ValueError(f'"{hex_str}" not recognized ' +
                             f'as a datetime type')
        return dto

    @classmethod
    def as_time(cls, hex_str: str) -> time:
        """
        Decode hex string as time object

        :param hex_str: {str} hex string to decode
        :raise: {ValueError} if hex_str invalid or does not have a time component

        :return: time
        """
        if cls.encoded_is_valid(hex_str) \
                and TemporencType.type_of(hex_str) != TemporencType.TYPE_D:
            if TemporencType.type_of(hex_str) == TemporencType.TYPE_T:
                m = cls.unpackb(hex_str)       # Decode as Time
            else:
                m = cls.as_date_time(hex_str)  # Decode as Datetime
        else:
            raise ValueError(f'"{hex_str}" not recognized ' +
                             f'as {TemporencType.TYPE_T.name}')
        return m.time()                        # Return Time portion

    @classmethod
    def compare_as_local(cls, left: str, right: str) -> bool:
        """
        Compare two datetime encoded values and determine if they are the same in
        local time.

        :param left:    {str}  a Type DT, DTS, or DTSZ encoded value
        :param right:   {str}  a Type DT, DTS, or DTSZ encoded value

        :return:        {bool} True if left and right are the same datetime when
                               converted to local time.

        >>> enc_cet = "EBDF83A2C983C48110"  # 1983-01-15T18:25:12.123456+01:00
        >>> enc_cst = "EBDF83A2C983C480A0"  # 1983-01-15T11:25:12.123456-06:00
        >>> Decoder.compare_as_local(enc_cet, enc_cst) == True
        True
        """
        compares_eq = False
        if ("S" in TemporencType.type_of(left).name and
                TemporencType.type_of(left) == TemporencType.type_of(right)):
            moment_left = temporenc.unpackb(bytes.fromhex(left))
            moment_right = temporenc.unpackb(bytes.fromhex(right))
            compares_eq = (moment_left.datetime().astimezone() ==
                           moment_right.datetime().astimezone())
        return compares_eq

    @classmethod
    def encoded_is_valid(cls, hex_str: str):
        unpacks = True
        try:
            cls.unpackb(hex_str)
        except ValueError:
            unpacks = False
        return unpacks

    @classmethod
    def unpackb(cls, hex_str: str):
        """
        Unpack a temporenc value from a hex string.

        If no valid value could be read, this raises ValueError.

        :raise: {ValueError} If valid value can not be read.

        :return: {Moment}
        """
        b = bytes.fromhex(hex_str)     # Convert hex str to bytes
        return temporenc.unpackb(b)    # Decode
