from flask import Blueprint

from components.temporenc import Encoder
from type_ext.precision_type import PrecisionType
from type_ext.temporenc_type import TemporencType

encode_bp = Blueprint('encode', __name__)


@encode_bp.route("/encode/<iso_string>", methods=["GET"])
def do_encode_iso(iso_string: str) -> object:
    """
    Encode ISO string

    Returns uppercase hexadecimal Temporenc encoded string # noqa: E501

    :param iso_string: ISO string to encode
    :type_ext iso_to_iso_dict: str

    :rtype: Codec
    """
    encoded = Encoder.encode_iso_str(iso_str=iso_string)
    precision = PrecisionType.encoded_to_precision_type(encoded_str=encoded).name
    type_ext = TemporencType.type_of(encoded=encoded).name
    return {
        'decoded': iso_string,
        'encoded': encoded,
        'precision': precision,
        'type_ext': type_ext}
