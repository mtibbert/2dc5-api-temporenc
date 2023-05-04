from flask import Blueprint
from components.temporenc import Decoder
from type_ext.precision_type import PrecisionType
from type_ext.temporenc_type import TemporencType

decode_bp = Blueprint('decode', __name__)


@decode_bp.route("/decode/<encoded_str>", methods=["GET"])
def do_decode_encoded_str(encoded_str: str) -> object:
    """
    Decode Temporenc encoded string

    Returns dict object in the form
        {'decoded': str, 'encoded': str,
         'precision': str, 'type_ext': str}

    :param encoded_str: {str} Temporenc encoded hex string to decode

    :rtype: Codec
    """
    # #49 Malformed URL Arg Should Return 404 Status Code
    precision = PrecisionType.encoded_to_precision_type(encoded_str=encoded_str).name
    type_ext = TemporencType.type_of(encoded=encoded_str).name
    match type_ext:
        case TemporencType.TYPE_D.name:
            fn = Decoder.as_date
        case TemporencType.TYPE_T.name:
            fn = Decoder.as_time
        case _:
            fn = Decoder.as_date_time
    decoded = fn(hex_str=encoded_str).isoformat()
    return {
        'decoded': decoded,
        'encoded': encoded_str,
        'precision': precision,
        'type_ext': type_ext}
