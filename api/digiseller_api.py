import time
from hashlib import sha256
from typing import Any

import requests
from loguru import logger

from products.products import Product
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
        if not timestamp:
            raise ValueError("Timestamp is required")

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

    @staticmethod
    def _parse_goods(response_data: dict[str, Any]) -> list[Product]:
        """
        Parses the response data and returns a list of Goods objects.

        Args:
            response_data: The response data.

        Returns:
            list[Product]: The list of Products objects.
        """
        digi_status_code = response_data["retval"]
        if digi_status_code == 0:
            goods_list = []
            for item in response_data.get("rows", []):
                goods = Product(
                    product_id=item["id_goods"],
                    name=item["name_goods"],
                    price=item["price"],
                    cnt_sell=item["cnt_sell"]
                )
                goods_list.append(goods)
            return goods_list
        else:
            desc = response_data.get("retdesc")
            logger.warning(desc)
            return []

    def get_products(self, order_col: str = "cntsell", order_dir: str = "desc",
                     rows: int = 10, page: int = 1, lang: str = "ru-RU",
                     show_hidden: int = 1,
                     currency: str = "RUR", ) -> list[Product]:
        """
           Retrieves goods from the Digiseller API.

           Args:
               order_col: The column to order the goods by. Defaults
                to "cntsell".
               order_dir: The direction of the ordering. Defaults to "desc".
               rows: The number of goods to retrieve. Defaults to 10.
               page: The page number of the goods. Defaults to 1.
               lang: The language of the goods. Defaults to "ru-RU".
               show_hidden: The parameter to show hidden goods. Defaults to 1.
               currency: The currency of the goods. Defaults to "RUR".


           Returns:
               list[Product]: The list of Products objects.
           """
        endpoint = "seller-goods"
        request_data = {
            "id_seller": self.seller_id,
            "order_col": order_col,
            "order_dir": order_dir,
            "rows": rows,
            "page": page,
            "currency": currency,
            "lang": lang,
            "show_hidden": show_hidden
        }
        if self.ensure_token_validity() is False:
            return []
        url = f"{BASE_URL}{endpoint}?token={self.token}"

        response_data = self._send_request(url, request_data)
        if response_data is not None:
            goods_list = self._parse_goods(response_data)
            logger.info('Digiseller products retrieved')
            return goods_list
        else:
            logger.warning('Failed to retrieve Digiseller products')
            return []
