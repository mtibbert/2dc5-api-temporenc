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
