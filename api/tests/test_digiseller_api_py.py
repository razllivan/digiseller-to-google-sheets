import unittest
from hashlib import sha256

from api.digiseller_api import DigisellerAPI


class DigisellerAPITest(unittest.TestCase):

    def setUp(self):
        self.api_key = "YOUR_API_KEY"
        self.seller_id = 12345
        self.digiseller_api = DigisellerAPI(self.api_key, self.seller_id)

    def test_init_with_valid_values(self):
        self.assertEqual(self.digiseller_api.api_key, self.api_key)
        self.assertEqual(self.digiseller_api.seller_id, self.seller_id)
        self.assertIsNone(self.digiseller_api.token)
        self.assertIsNone(self.digiseller_api.token_expiration)
        self.assertIsNotNone(self.digiseller_api.session)

    def test_init_with_missing_values(self):
        with self.assertRaises(ValueError):
            DigisellerAPI("", self.seller_id)

        with self.assertRaises(ValueError):
            DigisellerAPI(self.api_key, None)  # noqa

        with self.assertRaises(ValueError):
            DigisellerAPI("", None)  # noqa

    def test_generate_sign(self):
        timestamp = "2022-01-01T00:00:00Z"
        expected_sign = sha256(
            f"{self.api_key}{timestamp}".encode('utf-8')).hexdigest()
        generated_sign = self.digiseller_api.generate_sign(timestamp)
        self.assertEqual(generated_sign, expected_sign)

    def test_generate_sign_with_empty_timestamp(self):
        timestamp = ""
        with self.assertRaises(ValueError):
            self.digiseller_api.generate_sign(timestamp)


if __name__ == '__main__':
    unittest.main()
