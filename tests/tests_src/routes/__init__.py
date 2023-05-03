from flask.testing import FlaskClient
from type_ext.precision_type import PrecisionType
from type_ext.temporenc_type import TemporencType

#
# Test Helpers
#


def get_response(test_client: FlaskClient, prefix: str, route_arg: str):
    """
    Helper for the FlaskClient get() function

    Example: get_response(route_arg="1983-01-15,
                     prefix="/api/v1/temporenc/encode/",
                     test_client=test_client.test_client()):

    :param test_client:  {FlaskClient} the test application
    :param prefix:       {str}         the API prefix,
                                       including the trailing backslash
    :param route_arg:    {str}         arguments used by the route

    :return:             {response}    the test response object
    """
    url = f'{prefix}{route_arg}'
    return test_client.get(url)


def dp_item_actual_expected_dict(test_client: FlaskClient,
                                 prefix: str, route_arg: str, item):
    """
    Test helper to create dict object with expected and actual response json.

    :param test_client:  {FlaskClient} the test application
    :param prefix:       {str}         the API prefix,
                                       including the trailing backslash
    :param route_arg:    {str}         arguments used by the route
    :param item:         {dict}        in form of {"iso": str, "encoded": str}

    :return:             {dict}        in form of {"actual": json,
                                                   "expected": json}
    """
    type_ext = TemporencType.type_of(item["encoded"]).name
    precision = PrecisionType.encoded_to_precision_type(item["encoded"]).name
    expected = {"decoded": item["iso"], "encoded": item["encoded"],
                "precision": precision, "type_ext": type_ext}
    response = get_response(test_client=test_client,
                            prefix=prefix, route_arg=route_arg)
    return {"actual": response.get_json(),
            "expected": expected}
