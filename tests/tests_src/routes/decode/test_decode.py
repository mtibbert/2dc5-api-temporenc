from tests_src.test_support.tests_base import TestsBase
from tests_src.routes import dp_item_actual_expected_dict, get_response
from src import app


class TestDecodeGet(TestsBase):

    prefix_de = "/api/v1/temporenc/decode/"
    prefix_en = "/api/v1/temporenc/encode/"

    def setUp(self):
        super().setUp()
        self.app = app.test_client()

    def test_response_is_json(self):
        for item in self.data_provider:
            response = get_response(test_client=self.app,
                                    prefix=self.prefix_de,
                                    route_arg=item["encoded"])
            with self.subTest(f'{self.prefix_de}{item["encoded"]} returns JSON content'):
                self.assertTrue(response.is_json)

    def test_response_status_code_is_200(self):
        expected = 200
        for item in self.data_provider:
            response = get_response(test_client=self.app,
                                    prefix=self.prefix_de,
                                    route_arg=item["encoded"])
            with self.subTest(f'{self.prefix_de}{item["encoded"]} returns status code '
                              f'{expected}'):
                self.assertEqual(expected, response.status_code)

    def test_decodes_hex_str_correctly(self):
        for item in self.data_provider:
            results = dp_item_actual_expected_dict(test_client=self.app,
                                                   prefix=self.prefix_de,
                                                   route_arg=item["encoded"],
                                                   item=item)
            with self.subTest(f'{self.prefix_de}{item["encoded"]} returns expected JSON '
                              f'data'):
                self.assertDictEqual(results["expected"], results["actual"])

    def test_decodes_hex_str__equals_encoded_iso_str(self):
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
