from hashlib import sha256

import requests

BASE_URL = "https://api.digiseller.ru/api/"


class DigisellerAPI:

    def __init__(self, api_key: str, seller_id: int):
        if not api_key or not seller_id:
            raise ValueError("API key and seller id are required")

        self.api_key = api_key
        self.seller_id = seller_id
        self.token = None
        self.token_expiration = None
        self.session = requests.Session()

    def generate_sign(self, timestamp: str) -> str:
        """
          Generate a digiseller sign using the API key and timestamp.

          Args:
              timestamp: The timestamp.
          Returns:
              str: The generated sign.
          """
        concatenated_string = f"{self.api_key}{timestamp}"
        byte_array = concatenated_string.encode('utf-8')
        return sha256(byte_array).hexdigest()
