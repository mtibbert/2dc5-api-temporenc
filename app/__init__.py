from flask import Flask
from flasgger import Swagger, swag_from

api = Flask(__name__,
            template_folder="templates")

# TODO: #7 Extract Swagger Meta to an External File
template = {
    "version": "3.0.1",
    "info": {
        'title': 'Temporenc API',
        "summary": "api which encodes and decodes dates.",
        "description":
            "<h2>A Temporenc API</h2>" +
            "<ul>"
            "<li>Encodes date, time, and datetime ISO strings.<br/>" +
            "<li>Decodes Temporenc encoded values." +
            "</ul>",
        "contact": {
            "name": "Temporenc API Support",
            "email": "temporenc.api.support.v@qneni.com"},
        "version": "3.0.1",
    },
    "basePath": "/api/v1/temporenc/encode",
}

swagger = Swagger(api, template=template)


@api.route("/api/v1/temporenc/encode/<iso_string>")
@swag_from('encode.yaml')
def do_encode(iso_string):  # put application's code here
    """Encode ISO string

    Returns uppercase hexadecimal Temporenc encoded string # noqa: E501

    ---

    :param iso_string: ISO string to encode
    :type iso_string: str

    :rtype: Codec
    """
    return {
        'encoded': iso_string,
        'decoded': iso_string[::-1],
        'type': 'TYPE_DTS'}
