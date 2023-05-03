from tests_src.test_support.tests_base import TestsBase
from tests_src.routes import get_response, dp_item_actual_expected_dict
from src import app


class TestEncodeGet(TestsBase):

    prefix = "/api/v1/temporenc/encode/"

    def setUp(self):
        super().setUp()
        self.test_client = app.test_client()

    def test_response_is_json(self):
        for item in self.data_provider:
            response = get_response(test_client=self.test_client,
                                    prefix=self.prefix,
                                    route_arg=item["iso"])
            with self.subTest(f'{self.prefix}{item["iso"]} returns JSON content'):
                self.assertTrue(response.is_json)

    def test_response_status_code_is_200(self):
        expected = 200
        for item in self.data_provider:
            results = get_response(test_client=self.test_client,
                                   prefix=self.prefix,
                                   route_arg=item["iso"])
            with self.subTest(f'{self.prefix}{item["iso"]} returns '
                              f'status code {expected}'):
                self.assertEqual(expected, results.status_code)

    def test_encodes_iso_correctly(self):
        for item in self.data_provider:
            results = dp_item_actual_expected_dict(test_client=self.test_client,
                                                   prefix=self.prefix,
                                                   route_arg=item["iso"],
                                                   item=item)
            with self.subTest(f'{self.prefix}{item["iso"]} ' +
                              f'returns expected JSON data'):
                self.assertDictEqual(results["expected"], results["actual"])
