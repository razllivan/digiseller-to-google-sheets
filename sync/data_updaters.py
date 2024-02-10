import time

from api.digiseller_api import DigisellerAPI
from api.google_sheets_api import GoogleSheetsAPI
from products.products import Product
from settings import CREDENTIALS_PATH, SPREADSHEET_URL, WORKSHEET_NAME, \
    DIGISELLER_API_KEY, DIGISELLER_SELLER_ID, UPDATE_INTERVAL


class DataUpdater:
    def __init__(self):
        self.google_sheets_api = GoogleSheetsAPI(
            CREDENTIALS_PATH, SPREADSHEET_URL, WORKSHEET_NAME
        )
        self.digiseller_api = DigisellerAPI(
            DIGISELLER_API_KEY, DIGISELLER_SELLER_ID
        )

    def run(self) -> None:
        while True:
            products = self.digiseller_api.get_products()
            data = Product.to_gs_format(products)
            self.google_sheets_api.cleanup_extra_data(data)
            self.google_sheets_api.write_data(data)
            time.sleep(UPDATE_INTERVAL)
