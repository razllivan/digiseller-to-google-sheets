from api.digiseller_api import DigisellerAPI
from api.google_sheets_api import GoogleSheetsAPI
from data_sync.data_sync import DataSync



class Main:
    def __init__(self):
        # TODO: Implement __init__ method
        self.google_sheets_api = GoogleSheetsAPI()
        self.online_store_api = DigisellerAPI()
        self.data_sync = DataSync(self.google_sheets_api,
                                  self.online_store_api)

    def run(self):
        # TODO: Implement run method
        while True:
            self.data_sync.sync_data()


if __name__ == '__main__':
    pass