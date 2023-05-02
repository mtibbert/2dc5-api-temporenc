from type_ext.precision_type import PrecisionType
from type_ext.temporenc_type import TemporencType
#
# Test Helpers
#


def get_response(suffix: str, prefix: str, app):
    url = f'{prefix}{suffix}'
    return app.get(url)


def iso_to_encode_get_response(iso: str, prefix: str, app):
    # TODO: #48 Migrate iso_to_encode_get_response fn to a more Generic Name
    url = f'{prefix}{iso}'
    return app.get(url)


def dp_item_encoded_to_actual_expected(item, prefix: str, app):
    type_ext = TemporencType.type_of(item["encoded"]).name
    precision = PrecisionType.encoded_to_precision_type(item["encoded"]).name
    expected = {"decoded": item["iso"], "encoded": item["encoded"],
                "precision": precision, "type_ext": type_ext}
    response = get_response(item["iso"], prefix, app)
    return {"actual": response.get_json(),
            "expected": expected}


def dp_item_to_actual_expected(item, prefix: str, app):
    # TODO: #47 Rename dp_item_to_actual_expected Helper
    type_ext = TemporencType.type_of(item["encoded"]).name
    precision = PrecisionType.encoded_to_precision_type(item["encoded"]).name
    expected = {"decoded": item["iso"], "encoded": item["encoded"],
                "precision": precision, "type_ext": type_ext}
    response = iso_to_encode_get_response(item["iso"], prefix, app)
    return {"actual": response.get_json(),
            "expected": expected}
