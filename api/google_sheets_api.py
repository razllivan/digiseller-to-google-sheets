import gspread


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

    def write_data(self, data: list[list[str]]):
        """
        Write the given data to the worksheet.

        Parameters:
            data: The data to be written to the worksheet.

        Returns:
            None
        """
        self.worksheet.update(data)

    def check_changes(self):
        # TODO: Implement check_changes method
        pass
