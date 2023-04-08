from type_ext import DateDict
from datetime import datetime


class ValidateDict:

    @staticmethod
    def validate_date_dict(date_dict: DateDict, allow_year_zero: bool = True):
        """
        Validate DateDict members parse to a valid date.

        Notes: * ISO strings in the form YYYY, are validated against YY-01-01
               * ISO strings in the form YYYY-MM, are validated against YY-MM-01

        :param date_dict:        {DateDict} DateDict to evaluate
        :param allow_year_zero:  {bool} Allow/disallow validation where ISO string
                                            YYYY is "0000"
        :return:                 {bool} True if DateDict members parse to a valid date.
        """
        date = None
        if allow_year_zero and date_dict["year"] == "0000":
            date_dict["year"] = "0004"
        iso = (f'{date_dict["year"]}-' +
               f'{date_dict["month"]}-' +
               f'{date_dict["day"]}') \
            .replace("None", "01")
        try:
            date = datetime.fromisoformat(iso)
        finally:
            return date is not None
