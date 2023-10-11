import unittest

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


if __name__ == '__main__':
    unittest.main()
