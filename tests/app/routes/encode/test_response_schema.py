import unittest

from src import app


class TestResponseSchema(unittest.TestCase):

    prefix = "/api/v1/temporenc/encode/"
    iso = "1983-01-15T18:25:12.123456"
    url = f'{prefix}{iso}'

    response_props = ["decoded", "encoded", "precision", "type"]

    type_enum = ["TYPE_D", "TYPE_T", "TYPE_DT",
                 "TYPE_DTS", "TYPE_DTZ", "TYPE_DTSZ"]

    precision_enum = ["PRECISION_MICRO", "PRECISION_MILLI", "PRECISION_NANO",
                      "PRECISION_NONE", "PRECISION_NON_PRECISE"]

    def setUp(self):
        self.app = app.test_client()
        self.response = self.app.get(self.url)

    def test_response_contains_properties(self):
        actual = list(self.response.get_json().keys())
        self.assertListEqual(self.response_props, actual)

    def test_response_json_properties_are_strings(self):
        d = self.response.get_json()
        for key in d.keys():
            self.assertIsInstance(d[key], str)

    def test_response_precision_property_is_in_enum(self):
        # TODO: #6 Expand test once encode is implemented
        json = self.response.get_json()
        actual = json["precision"]
        self.assertIn(actual, self.precision_enum)

    def test_response_type_property_is_in_enum(self):
        # TODO: #6 Expand test once encode is implemented
        json = self.response.get_json()
        actual = json["type"]
        self.assertIn(actual, self.type_enum)

    def test_response_precision_property_when_not_enum_fails(self):
        self.assertNotIn("foo", self.precision_enum)

    def test_response_type_property_when_not_enum_fails(self):
        self.assertNotIn("foo", self.type_enum)


if __name__ == '__main__':
    unittest.main()
