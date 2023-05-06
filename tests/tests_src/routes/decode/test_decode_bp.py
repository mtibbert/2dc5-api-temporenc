from tests_src.test_support.tests_base import TestsBase
from tests_src.routes import dp_item_actual_expected_dict, get_response
from src import app
from unittest.mock import patch


class TestDecodeBp(TestsBase):

    prefix_de = "/api/v1/temporenc/decode/"
    prefix_en = "/api/v1/temporenc/encode/"

    def setUp(self):
        super().setUp()
        self.app = app.test_client()

    def test_decodes_hex_str_correctly(self):
        for item in self.data_provider:
            results = dp_item_actual_expected_dict(test_client=self.app,
                                                   prefix=self.prefix_de,
                                                   route_arg=item["encoded"],
                                                   item=item)
            with self.subTest(f'{self.prefix_de}{item["encoded"]} returns expected JSON '
                              f'data'):
                self.assertDictEqual(results["expected"], results["actual"])

    def test_decodes_hex_str_equals_encoded_iso_str(self):
        for item in self.data_provider:
            encoded_response = get_response(test_client=self.app,
                                            prefix=self.prefix_en,
                                            route_arg=item["iso"])
            decoded_response = get_response(test_client=self.app,
                                            prefix=self.prefix_de,
                                            route_arg=item["encoded"])
            with self.subTest(f'/decode/{item["encoded"]} response == ' +
                              f'/encode/{item["iso"]}'):
                self.assertDictEqual(decoded_response.json, encoded_response.json)

    def test_response_200_response_type_is_json(self):
        for item in self.data_provider:
            response = get_response(test_client=self.app,
                                    prefix=self.prefix_de,
                                    route_arg=item["encoded"])
            with self.subTest(f'{self.prefix_de}{item["encoded"]} returns JSON content'):
                self.assertTrue(response.is_json)

    def test_response_200_status_code_for_valid_encoded_value(self):
        expected = 200
        for item in self.data_provider:
            response = get_response(test_client=self.app,
                                    prefix=self.prefix_de,
                                    route_arg=item["encoded"])
            with self.subTest(f'{self.prefix_de}{item["encoded"]} returns status code '
                              f'{expected}'):
                self.assertEqual(expected, response.status_code)

    def test_response_404_response_json_key_message_is_str(self):
        data_provider = ["x3F396E0D803DC40"]
        expected = ["message"]

        for route_arg in data_provider:
            response = get_response(test_client=self.app,
                                    prefix=self.prefix_de,
                                    route_arg=route_arg)
            with self.subTest(f'{self.prefix_de}{route_arg} response key(s) '
                              f'are {expected}'):
                self.assertListEqual(expected, list(response.json.keys()))
                self.assertIsInstance(response.json[expected[0]], str)

    def test_response_404_response_type_is_json(self):
        data_provider = ["x3F396E0D803DC40"]
        expected = "application/json"

        for route_arg in data_provider:
            response = get_response(test_client=self.app,
                                    prefix=self.prefix_de,
                                    route_arg=route_arg)
            with self.subTest(f'{self.prefix_de}{route_arg} content_type is '
                              f'"{expected}"'):
                self.assertEqual(expected, response.content_type)

    def test_response_404_status_code_for_invalid_encoded_value(self):
        expected = 404
        for item in self.data_provider:
            response = get_response(test_client=self.app,
                                    prefix=self.prefix_de,
                                    route_arg=f'b{item["encoded"][1:]}')
            with self.subTest(f'{self.prefix_de}{item["encoded"]} returns status code '
                              f'{expected}'):
                self.assertEqual(expected, response.status_code)

    def test_response_404_status_code_for_non_hex_arg(self):
        expected = 404
        for item in self.data_provider:
            arg_proxy = f'z{item["encoded"][1:]}'
            response = get_response(test_client=self.app,
                                    prefix=self.prefix_de,
                                    route_arg=arg_proxy)
            with self.subTest(f'{self.prefix_de}{arg_proxy} returns status code '
                              f'{expected}'):
                self.assertEqual(expected, response.status_code)

    def test_response_404_err_msg_ends_with_expected_type(self):
        expected = 404
        for item in self.data_provider:
            arg_proxy = f'b{item["encoded"][1:]}'
            expected_msg_end_rx = r'not recognized as TYPE_' \
                                  r'[D | T | DT| DTS | DTZ | DTSZ]$'
            response = get_response(test_client=self.app,
                                    prefix=self.prefix_de,
                                    route_arg=arg_proxy)
            with self.subTest(f'{self.prefix_de}{arg_proxy} ends with "TYPE_x"'):
                self.assertEqual(expected, response.status_code)  # Check for 404
                self.assertRegex(response.json["message"], expected_msg_end_rx)

    def test_response_404_err_msg_includes_encoded_hex(self):
        expected = 404
        for item in self.data_provider:
            arg_proxy = f'b{item["encoded"][1:]}'
            expected_msg_start = f'Resource not found: \'{arg_proxy}\' ' \
                                 f'not recognized as TYPE_'
            response = get_response(test_client=self.app,
                                    prefix=self.prefix_de,
                                    route_arg=arg_proxy)
            with self.subTest(f'{self.prefix_de}{arg_proxy} error message '
                              f'includes {arg_proxy}'):
                self.assertEqual(expected, response.status_code)  # Check for 404
                self.assertTrue(
                    str(response.json["message"]).startswith(expected_msg_start),
                    f'expected "{response.json["message"]}" '
                    f'to start with "{expected_msg_start}"')

    @patch('components.temporenc.decoder.Decoder.decode')
    def test_response_404_err_msg_invalid_encoded_hex(self, mock_decode):
        data_provider = [
            {"arg": "8fffff0E", "type": "TYPE_D"},
            {"arg": "bEFC1D264C", "type": "TYPE_T"},
            {"arg": "1fff1D264C", "type": "a datetime"},
        ]
        for item in data_provider:
            msg = f'\'{item["arg"]}\' not recognized as {item["type"]}'
            expected = {'message': f'Resource not found: {msg}'}
            mock_decode.side_effect = ValueError(msg)
            with self.subTest(f'{item["arg"]} returns error message {msg}'):
                response = self.app.get(f'{self.prefix_de}{item["arg"]}')
                mock_decode.assert_called_with(item["arg"])
                self.assertEqual(expected, response.json)

    def test_response_404_err_msg_non_hex_arg(self):
        for item in self.data_provider:
            arg_proxy = f'x{item["encoded"][1:]}'
            expected = f'Resource not found: '\
                       f'invalid literal for int() with base 16: '\
                       "'" + f'{arg_proxy}' + "'"
            response = get_response(test_client=self.app,
                                    prefix=self.prefix_de,
                                    route_arg=arg_proxy)
            msg = f'"{expected[:18]} ~ {expected[-10:]}"'
            with self.subTest(f'{self.prefix_de}{arg_proxy} message includes {msg}'):
                self.assertEqual(404, response.status_code)  # Check for 404
                self.assertEqual(response.json["message"], expected)
