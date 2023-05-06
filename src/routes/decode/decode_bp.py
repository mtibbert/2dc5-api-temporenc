from flask import Blueprint
from components.temporenc import Decoder
from type_ext.precision_type import PrecisionType
from type_ext.temporenc_type import TemporencType

decode_bp = Blueprint('decode', __name__)


@decode_bp.route("/decode/<encoded_str>", methods=["GET"])
def do_decode_encoded_str(encoded_str: str) -> object:
    """
    Decode Temporenc encoded string.

    If the encoded string is not a Temporenc enoded value, or is not a valid hex string,
    status code 404 is returned along with json in the form {"message": str}.

    Returns dict object in the form
        {'decoded': str, 'encoded': str,
         'precision': str, 'type_ext': str}

    :param encoded_str: {str} Temporenc encoded hex string to decode

    :rtype: {json} Codec schema
    """
    try:
        # Possible ValueError("invalid literal for int() with base 16: '...'")
        precision = PrecisionType.encoded_to_precision_type(encoded_str=encoded_str).name
        type_ext = TemporencType.type_of(encoded=encoded_str).name
        # Possible ValueError("'{encoded_str}' not recognized as '...'")
        decoded = Decoder.decode(encoded_str)
    except ValueError as ve:
        err_msg = str(ve).replace('"', "'")
        return {"message": f'Resource not found: {err_msg}'}, 404
    return {
        'decoded': decoded.isoformat(),
        'encoded': encoded_str,
        'precision': precision,
        'type_ext': type_ext}
