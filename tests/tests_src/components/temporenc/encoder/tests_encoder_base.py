from unittest import TestCase


class TestsEncoderBase(TestCase):

    data_provider = {}

    def setUp(self) -> None:
        data = {
            "TYPE_D": [
                {"iso": "1983-01-15",
                 "encoded": "8F7E0E"}],
            "TYPE_T": [
                {"iso": "18:25:12",
                 "encoded": "A1264C"}],
            "TYPE_DT": [
                {"iso": "1983-01-15T18:25:12",
                 "encoded": "1EFC1D264C"}],
            "TYPE_DTS": [
                {"iso": "2023-03-28T17:27:00.123420",
                 "encoded": "57E72DC5B0078870"},
                {"iso": "1983-01-15T18:25:12.123456",
                 "encoded": "57BF074993078900"}],
            "TYPE_DTZ": [
                {"iso": "1983-01-15T18:25:12+01:00",
                 "encoded": "CF7E0E8B2644"}],
            "TYPE_DTSZ": [
                {"iso": "1983-01-15T18:25:12.123456+01:00",
                 "encoded": "EBDF83A2C983C48110"}],
        }
        self.dp_complex_types = \
            data["TYPE_DTSZ"] + data["TYPE_DTZ"] + data["TYPE_DTS"] + data["TYPE_DT"]
        self.dp_elemental_types = data["TYPE_D"] + data["TYPE_T"]
        self.data_provider = self.dp_complex_types + self.dp_elemental_types
