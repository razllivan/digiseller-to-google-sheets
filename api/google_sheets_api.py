import time

import gspread
from loguru import logger

from settings import REPEAT_INTERVALS, PRODUCT_TABLE_ROWS_TO_EXCLUDE
from utils.decorators import retry_intervals


class GoogleSheetsAPI:
    def __init__(self, credentials_path: str, spreadsheet_url: str,
                 worksheet_name: str):
        """
        Initializes the GoogleSheetsAPI object with the credentials

        Args:
            credentials_path: The path to the service account credentials
             file.
            spreadsheet_url: The URL of the spreadsheet.
            worksheet_name: The name of the worksheet.
        """
        self.client = gspread.service_account(filename=credentials_path)
        self.spreadsheet = self.client.open_by_url(spreadsheet_url)
        self.worksheet = self.spreadsheet.worksheet(worksheet_name)

    def read_data(self) -> list[list[str]]:
        """
        Reads data from the worksheet and returns all values.

        Returns:
            All values from the worksheet.
        """

        return self.worksheet.get_values()

    @retry_intervals(*REPEAT_INTERVALS)
    def write_data(self, data: list[list[str]]):
        """
        Write the given data to the worksheet.

        Parameters:
            data: The data to be written to the worksheet.

        Returns:
            None
        """
        try:
            self.worksheet.update('A1',
                                  time.strftime("%H:%M", time.localtime()))
            self.worksheet.update('A3', data)
            logger.success('Data updated successfully')
        except Exception as e:
            logger.exception(e)
            raise e

    def cleanup_extra_data(self, new_products: list[list[str]]):
        """
        Clears the extra data in the worksheet by removing rows of products
         that exceed the number of new products.

        Args:
            new_products (list[list[str]]): A list of lists of strings
             representing new products.

        Returns:
            None
            """
        old_products = self.read_data()[PRODUCT_TABLE_ROWS_TO_EXCLUDE:]

        start_row = len(new_products) + PRODUCT_TABLE_ROWS_TO_EXCLUDE + 1
        end_row = len(old_products) + PRODUCT_TABLE_ROWS_TO_EXCLUDE
        if start_row <= end_row:
            range_to_clear = f"{start_row}:{end_row}"
            self.worksheet.batch_clear([range_to_clear])
