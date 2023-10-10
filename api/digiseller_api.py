import time
from hashlib import sha256
from typing import Any

import requests
from loguru import logger
from settings import REPEAT_INTERVALS
from utils.decorators import retry_intervals

BASE_URL = "https://api.digiseller.ru/api/"
TOKEN_EXPIRATION_TIME = 7200


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

    def get_token(self) -> bool:
        """
           Retrieves a token from the API server for authentication.
           Returns:
               bool: True if the token is successfully retrieved
               , False otherwise.
           """
        endpoint = "apilogin"
        url = f"{BASE_URL}{endpoint}"
        timestamp = int(time.time())
        sign = self.generate_sign(str(timestamp))

        request_data = {
            "seller_id": self.seller_id,
            "timestamp": timestamp,
            "sign": sign
        }

        response_data = self._send_request(url, request_data)
        if response_data is None:
            logger.error('Failed to retrieve token: No response data')
            return False

        digi_status_code = response_data["retval"]
        if digi_status_code == 0:
            self.token = response_data["token"]
            self.token_expiration = time.time() + TOKEN_EXPIRATION_TIME
            logger.info('Digiseller token obtained')
            return True
        else:
            desc = response_data["desc"]
            logger.warning(desc)
            return False

    def ensure_token_validity(self) -> bool:
        """
           Ensure the validity of the token.
           Returns:
               bool: True if the token is valid or is successfully refreshed,
                False otherwise.
           """
        if not self.token or time.time() >= self.token_expiration:
            return self.get_token()
        return True
