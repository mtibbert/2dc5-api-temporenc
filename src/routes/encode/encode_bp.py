from flask import Blueprint

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
    return {
        'decoded': iso_string[::-1],
        'encoded': iso_string,
        'precision': "PRECISION_MILLI",
        'type_ext': 'TYPE_DTS'}
