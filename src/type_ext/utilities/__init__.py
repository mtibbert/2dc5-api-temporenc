import re


def join_dict_values(d: dict, glue: str = "-", normalize: bool = True) -> str:
    """
    Join all dictionary values.

    :param d:         {dict} source dictionary
    :param glue:      {str}  character to join values, defaults to "-"
    :param normalize: {bool} normalize returned string by removing 'None' values,
                             defaults to True

    :return: {str}

    # >>> cls = TestValidateTimeDict
    # >>> date_dict = {"year": "1983", "month": "01", "day": "15"}
    # >>> none_dict = {"year": "1983", "month": "01", "day": None}
    # >>> time_dict = {"hour": "23", "minute": "59", "second": "59"}
    # >>> cls.join_dict_values(date_dict) == '1983-01-15'
    # True
    # >>> cls.join_dict_values(none_dict) == '1983-01'
    # True
    # >>> cls.join_dict_values(none_dict, "-", False) == '1983-01-None'
    # True
    # >>> cls.join_dict_values(time_dict, ":") == '23:59:59'
    # True
    """
    ret_str = glue.join([str(x) for x in d.values()])
    if normalize:
        ret_str = normalize_none(ret_str)
    return ret_str


def normalize_none(iso) -> str:
    """
    Removes "None" from ISO strings

    :param iso: {str} an ISO string
    :return: {str}

    # >>> TestValidateTimeDict.normalize_none("1983-01-None") == '1983-01'
    # True
    # >>> TestValidateTimeDict.normalize_none("1983-None-None") == '1983'
    # True
    # >>> TestValidateTimeDict.normalize_none("13:01:None") == '13:01'
    # True
    """
    rx = r"([-:]None){1,2}$"
    iso_str = re.sub(rx, "", iso)
    return iso_str
