from hashlib import sha256
from typing import Any

import requests
from loguru import logger
from settings import REPEAT_INTERVALS
from utils.decorators import retry_intervals

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

    @retry_intervals(*REPEAT_INTERVALS)
    def _send_request(self, url: str,
                      request_data: dict) -> dict[str, Any]:
        """
        Sends a request and returns the response data.

        Args:
            url: The URL to send the request to.
            request_data: The request data.

        Returns:
            dict: The response data.
        """
        try:
            response = self.session.post(url, json=request_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.exception(
                f'Error occurred while requesting API, '
                f'request data: {request_data}')
            raise e
