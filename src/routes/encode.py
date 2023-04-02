from flask_restful import Resource
from flasgger import swag_from


class Encode(Resource):

    @swag_from('encode.yaml')
    def get(self, iso_string) -> object:
        """
        Encode ISO string

        Returns uppercase hexadecimal Temporenc encoded string # noqa: E501

        :param iso_string: ISO string to encode
        :type iso_string: str

        :rtype: Codec
        """
        return {
            'encoded': iso_string,
            'decoded': iso_string[::-1],
            'type': 'TYPE_DTS'}
