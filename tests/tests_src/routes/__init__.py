from type_ext.precision_type import PrecisionType
from type_ext.temporenc_type import TemporencType
#
# Test Helpers
#


def iso_to_encode_get_response(iso: str, prefix: str, app):
    url = f'{prefix}{iso}'
    return app.get(url)


def dp_item_to_actual_expected(item, prefix: str, app):
    type_ext = TemporencType.type_of(item["encoded"]).name
    precision = PrecisionType.encoded_to_precision_type(item["encoded"]).name
    expected = {"decoded": item["iso"], "encoded": item["encoded"],
                "precision": precision, "type_ext": type_ext}
    response = iso_to_encode_get_response(item["iso"], prefix, app)
    return {"actual": response.get_json(),
            "expected": expected}
