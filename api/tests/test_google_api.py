import unittest
from random import randint, choice
from string import ascii_letters
from unittest.mock import MagicMock, patch

from api.google_sheets_api import GoogleSheetsAPI
from settings import PRODUCT_TABLE_ROWS_TO_EXCLUDE


class GoogleSheetsAPITest(unittest.TestCase):

    def setUp(self):
        credentials_path = "path/to/credentials.json"
        spreadsheet_url = "https://docs.google.com/spreadsheets/d/1234567890"
        worksheet_name = "Sheet1"

        mock_client = MagicMock()
        mock_spreadsheet = MagicMock()
        mock_worksheet = MagicMock()

        with patch('api.google_sheets_api.gspread.service_account',
                   return_value=mock_client), \
                patch.object(mock_client, 'open_by_url',
                             return_value=mock_spreadsheet):
            mock_worksheet.batch_clear = MagicMock()
            mock_spreadsheet.worksheet = MagicMock(return_value=mock_worksheet)

            self.api = GoogleSheetsAPI(credentials_path, spreadsheet_url,
                                       worksheet_name)

    @patch('api.google_sheets_api.GoogleSheetsAPI.read_data')
    def test_cleanup_extra_data(self, mocked_read_data):
        test_cases = [
            self.generate_test_cases(msg='more old products',
                                     new_product_count=3,
                                     old_product_count=5,
                                     expected_clear_range=['6:7'],
                                     should_call_bath_clear=True),
            self.generate_test_cases(msg='more old products 2',
                                     new_product_count=3,
                                     old_product_count=4,
                                     expected_clear_range=['6:6'],
                                     should_call_bath_clear=True),
            self.generate_test_cases(msg='fewer old products',
                                     new_product_count=6,
                                     old_product_count=5,
                                     should_call_bath_clear=False),
            self.generate_test_cases(msg='same number of products',
                                     new_product_count=6,
                                     old_product_count=6,
                                     should_call_bath_clear=False)
        ]
        for test_case in test_cases:
            with self.subTest(msg=test_case['msg'], test_case=test_case):
                mocked_read_data.return_value = test_case['rows_from_table']
                self.api.cleanup_extra_data(test_case['new_products'])
                if test_case['should_call_bath_clear']:
                    self.api.worksheet.batch_clear.assert_called_once_with(
                        test_case['expected_clear_range'])
                else:
                    self.api.worksheet.batch_clear.assert_not_called()
            self.api.worksheet.reset_mock()

    @staticmethod
    def generate_test_cases(msg, new_product_count, old_product_count,
                            should_call_bath_clear, expected_clear_range=None):
        return {'msg': msg,
                'new_products': [['Product'] for _ in
                                 range(new_product_count)],
                'rows_from_table': [
                                       ['row'] for _ in
                                       range(
                                           PRODUCT_TABLE_ROWS_TO_EXCLUDE)] + [
                                       ['Product'] for _ in
                                       range(old_product_count)
                                   ],
                'expected_clear_range': expected_clear_range,
                'should_call_bath_clear': should_call_bath_clear}


def generate_and_write_test_data(credentials_path: str, spreadsheet_url: str,
                                 worksheet_name: str, products_count: int):
    """
    Generates test data and writes it to a Google Sheet.

    Args:
        credentials_path (str): The path to the credentials file for accessing
         the Google Sheets API.
        spreadsheet_url (str): The URL of the Google Sheet where the data will
        be written.
        worksheet_name (str): The name of the worksheet in spreadsheet
        products_count (int): The number of test data products to generate.

    Returns:
        None
    """
    test_data = []
    for _ in range(products_count):
        product_id = randint(1, 100000)
        name = ''.join(choice(ascii_letters) for _ in range(10))
        price = randint(50, 5000)
        sales = randint(0, 5000)
        test_data.append([product_id, name, price, sales])
    api = GoogleSheetsAPI(credentials_path, spreadsheet_url, worksheet_name)
    api.cleanup_extra_data(test_data)
    api.write_data(test_data)


if __name__ == '__main__':
    unittest.main()
