import unittest
from src import app


class TestEncodeGet(unittest.TestCase):

    prefix = "/api/v1/temporenc/encode/"

    def setUp(self):
        self.app = app.test_client()

    def test_encodes_correctly(self):
        iso = "1923"
        url = f'{self.prefix}{iso}'
        expected = {"decoded": "3291", "encoded": "1923",
                    "precision": "PRECISION_MILLI", "type_ext": "TYPE_DTS"}
        response = self.app.get(url)
        self.assertDictEqual(expected, response.get_json())

    def test_response_is_json(self):
        iso = "1923"
        url = f'{self.prefix}{iso}'
        response = self.app.get(url)
        self.assertTrue(response.is_json)

    def test_response_status_code_is_200(self):
        iso = "1923"
        url = f'{self.prefix}{iso}'
        expected = 200
        response = self.app.get(url)
        self.assertEqual(expected, response.status_code)


if __name__ == '__main__':
    unittest.main()
