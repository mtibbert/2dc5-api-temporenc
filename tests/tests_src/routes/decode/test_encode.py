from tests_src.test_support.tests_base import TestsBase
from tests_src.routes import dp_item_encoded_to_actual_expected
from src import app


class TestDecodeGet(TestsBase):

    prefix = "/api/v1/temporenc/decode/"

    def setUp(self):
        super().setUp()
        self.app = app.test_client()

    def test_response_is_json(self):
        for item in self.data_provider:
            response = dp_item_encoded_to_actual_expected(
                item, self.prefix, self.app)
            with self.subTest(f'{self.prefix}{item["iso"]} returns JSON content'):
                self.assertTrue(response.is_json)

    def test_response_status_code_is_200(self):
        expected = 200
        for item in self.data_provider:
            results = dp_item_encoded_to_actual_expected(item, self.prefix, self.app)
            with self.subTest(f'{self.prefix}{item["iso"]} returns status code '
                              f'{expected}'):
                self.assertEquals(expected, results.status_code)

    def test_decodes_hex_str_correctly(self):
        for item in self.data_provider:
            results = dp_item_encoded_to_actual_expected(item, self.prefix, self.app)
            with self.subTest(f'{self.prefix}{item["iso"]} returns expected JSON data'):
                self.assertDictEqual(results["expected"], results["actual"])
