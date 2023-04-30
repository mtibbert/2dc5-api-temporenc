from components.temporenc import Encoder
from components.temporenc.decoder import Decoder
from tests_src.components.temporenc.tests_base import TestsBase
from type_ext import TemporencType
import datetime


class TestDecoder(TestsBase):

    def setUp(self) -> None:
        super().setUp()

    def test_compare_as_local(self):
        data_provider = [
            [Encoder.encode_iso_str("1983-01-15T18:25:12.123456+01:00"),
             Encoder.encode_iso_str("1983-01-15T11:25:12.123456-06:00")]]
        local = f'UTC{datetime.datetime.now().astimezone().isoformat()[-6:]}'
        for li in data_provider:
            with self.subTest(f'{li[0]} and {li[1]} are the same at {local}'):
                self.assertTrue(Decoder.compare_as_local(li[0], li[1]))

    def test_decode_fn(self):
        data_provider = self.dp_complex_types + self.dp_elemental_types
        for item in data_provider:
            encoded = item["encoded"]
            match TemporencType.type_of(encoded):
                case TemporencType.TYPE_D:
                    expected = datetime.date.fromisoformat(item["iso"])
                case TemporencType.TYPE_T:
                    expected = datetime.time.fromisoformat(item["iso"])
                case _:
                    expected = datetime.datetime.fromisoformat(item["iso"])
            with self.subTest(f'{encoded} decodes to {expected}'):
                actual = Decoder.decode(encoded)
                self.assertEqual(expected, actual)

    def test_decode_complex_types_as_date(self):
        data_provider = self.dp_complex_types
        for item in data_provider:
            encoded = item["encoded"]
            expected = datetime.datetime.fromisoformat(item["iso"]).date()
            with self.subTest(f'{encoded} decodes to {expected}'):
                actual = Decoder.as_date(encoded)
                self.assertEqual(expected, actual)

    def test_decode_complex_types_as_time(self):
        data_provider = self.dp_complex_types
        for item in data_provider:
            encoded = item["encoded"]
            expected = datetime.datetime.fromisoformat(item["iso"]).time()
            with self.subTest(f'{encoded} decodes to {expected}'):
                actual = Decoder.as_time(encoded)
                self.assertEqual(expected, actual)

    def test_invalid_hex_date_raises_err(self):
        invalid_hex = [
            "a1264c",  # No date component
            "f7e0e"]  # Invalid
        for arg in invalid_hex:
            expected = f'"{arg}" not recognized as TYPE_D'
            with self.subTest(f'{arg} raises ValueError({expected})'):
                self.assertRaisesRegex(ValueError, expected, Decoder.as_date, arg)

    def test_invalid_hex_date_time_raises_err(self):
        invalid_hex = [
            "8f7e0e",  # No time component
            "a1264c",  # No date component
            "f7e0e"]   # Invalid
        for arg in invalid_hex:
            expected = f'"{arg}" not recognized as a datetime type'
            with self.subTest(f'{arg} raises ValueError({expected})'):
                self.assertRaisesRegex(ValueError, expected, Decoder.as_date_time, arg)

    def test_invalid_hex_time_raises_err(self):
        invalid_hex = [
            "8f7e0e",  # No time component
            "f1264c"]  # Invalid
        for arg in invalid_hex:
            expected = f'"{arg}" not recognized as TYPE_T'
            with self.subTest(f'{arg} raises ValueError({expected})'):
                self.assertRaisesRegex(ValueError, expected, Decoder.as_time, arg)
