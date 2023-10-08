import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'service_account.json')

# Environment variables
load_dotenv()
SPREADSHEET_URL = os.environ.get('SPREADSHEET_URL')
WORKSHEET_NAME = os.environ.get('WORKSHEET_NAME')
DIGISELLER_API_KEY = os.environ.get('DIGISELLER_API_KEY')
