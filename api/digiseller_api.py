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

    def get_products(self):
        # TODO: Implement get_products method
        pass

    def update_product(self, product):
        # TODO: Implement update_product method
        pass

    def check_changes(self):
        # TODO: Implement check_changes method
        pass
