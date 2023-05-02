from tests_src.test_support.tests_base import TestsBase
from tests_src.routes import iso_to_encode_get_response, dp_item_to_actual_expected
from src import app


class TestEncodeGet(TestsBase):

    prefix = "/api/v1/temporenc/encode/"

    def setUp(self):
        super().setUp()
        self.app = app.test_client()

    def test_response_is_json(self):
        for item in self.data_provider:
            response = iso_to_encode_get_response(item["iso"], self.prefix, self.app)
            with self.subTest(f'{self.prefix}{item["iso"]} returns JSON content'):
                self.assertTrue(response.is_json)

    def test_response_status_code_is_200(self):
        expected = 200
        for item in self.data_provider:
            results = iso_to_encode_get_response(item["iso"], self.prefix, self.app)
            with self.subTest(f'{self.prefix}{item["iso"]} returns status code '
                              f'{expected}'):
                self.assertEqual(expected, results.status_code)

    def test_encodes_iso_correctly(self):
        for item in self.data_provider:
            results = dp_item_to_actual_expected(item, self.prefix, self.app)
            with self.subTest(f'{self.prefix}{item["iso"]} returns expected JSON data'):
                self.assertDictEqual(results["expected"], results["actual"])
