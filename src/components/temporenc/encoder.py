import re
from datetime import datetime
from temporenc import temporenc
from components.utilities import Utilities


class Encoder:

    # TODO: Encode ISO String #26

    @classmethod
    def encode_by_args(cls, year: int = None, month: int = None, day: int = None,
                       hour: int = None, minute: int = None, second: int = None,
                       precision: int = None, tz_offset: int = None):
        """
        Encode arguments as an uppercase hexadecimal string.

        :param year:      {int} (default None)
        :param month:     {int} (default None
        :param day:       {int} (default None
        :param hour:      {int} (default None
        :param minute:    {int} (default None
        :param second:    {int} (default None
        :param precision: {int} (default None
        :param tz_offset: {int} (default None

        :return:          {str} an uppercase hexadecimal string.
        """
        iso = Utilities.packb_args_to_iso(year=year, month=month, day=day,
                                          hour=hour, minute=minute, second=second,
                                          precision=precision, tz_offset=tz_offset)
        return cls.encode_iso_dto(dto=datetime.fromisoformat(iso))

    @classmethod
    def encode_iso_date(cls, date_obj: datetime.date):
        """
        Encode date object as an uppercase hexadecimal string.

        :param date_obj: {datetime.date}

        :return: {str} a six (6) character uppercase hexadecimal string.
        """
        return temporenc.packb(value=date_obj, type="D").hex().upper()

    @classmethod
    def encode_iso_time(cls, time_obj: datetime.time):
        """
        Encode time object as an uppercase hexadecimal string.

        :param time_obj: {datetime.time}

        :return: {str} a six (6) character uppercase hexadecimal string.
        """
        return temporenc.packb(value=time_obj, type="T").hex().upper()

    @classmethod
    def encode_iso_dto(cls, dto: datetime, encode_to_type: str = None):
        """
        Encode datetime object as an uppercase hexadecimal string.

        :param dto: {datetime}
        :param encode_to_type: str (default None)

        :return: {str} an uppercase hexadecimal string.
        """
        encode_to_precision = "microsecond"
        encoded = None
        precision_extract = ""
        if encode_to_type is None and "." not in dto.isoformat():
            # DT or DTZ
            encode_to_type = "DT" if dto.tzinfo is None else "DTZ"
        elif encode_to_type is None and "." in dto.isoformat():
            new_iso_str = Utilities.normalize_iso_str(dto.isoformat())
            if len(re.split(r"\W+", new_iso_str.split(".")[1], 1)) > 1:
                precision_len = [x.isdigit()
                                 for x in new_iso_str.split(".")[1]].index(False)
            else:
                precision_len = len(new_iso_str.split(".")[1])
            if 0 < precision_len <= 3:
                encode_to_precision = "millisecond"
                precision_extract = new_iso_str.split(".")[1][:precision_len]
            elif 7 <= precision_len <= 9:
                # Python microsecond resolution ... Should not reach here.
                encode_to_precision = "nanosecond"
                precision_extract = new_iso_str.split(".")[1][:precision_len]
            dto = datetime.fromisoformat(new_iso_str)
        if encode_to_precision == "millisecond":
            encoded = temporenc.packb(value=dto, type=encode_to_type,
                                      millisecond=int(precision_extract)).hex().upper()
        elif encode_to_precision == "nanosecond":
            encoded = temporenc.packb(value=dto, type=encode_to_type,
                                      nanosecond=int(precision_extract)).hex().upper()
        else:
            encoded = temporenc.packb(value=dto, type=encode_to_type).hex().upper()
        return encoded
