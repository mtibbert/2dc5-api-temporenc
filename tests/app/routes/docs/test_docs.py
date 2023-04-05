import unittest
from src import app


class TestDocs(unittest.TestCase):

    prefix = "/api/v1/temporenc/docs/"

    def setUp(self):
        self.app = app.test_client()

    def test_request_method_is_get(self):
        expected = "GET"
        response = self.app.get(self.prefix)
        self.assertEqual(expected, response.request.method)

    def test_request_path_is_docs(self):
        expected = "/api/v1/temporenc/docs/"
        response = self.app.get(self.prefix)
        self.assertEqual(expected, response.request.path)

    def test_response_content_type_is_html(self):
        expected = "text/html; charset=utf-8"
        response = self.app.get(self.prefix)
        self.assertEqual(expected, response.content_type)

    def test_response_is_html(self):
        expected = 200
        response = self.app.get(self.prefix)
        self.assertEqual(expected, response.status_code)

    def test_response_mime_type_is_text_html(self):
        expected = "text/html"
        response = self.app.get(self.prefix)
        self.assertEqual(expected, response.mimetype)

    def test_response_status_code_is_200(self):
        url = self.prefix
        expected = 200
        response = self.app.get(url)
        self.assertEqual(expected, response.status_code)


if __name__ == '__main__':
    unittest.main()
