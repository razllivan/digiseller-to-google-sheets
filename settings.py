import os
import sys

from dotenv import load_dotenv
from loguru import logger

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'service_account.json')
REPEAT_INTERVALS = [60, 60, 60, 300, 300, 300, 1800, 1800, 1800]
UPDATE_INTERVAL = 60

# Environment variables
load_dotenv()
SPREADSHEET_URL = os.environ.get('SPREADSHEET_URL')
WORKSHEET_NAME = os.environ.get('WORKSHEET_NAME')
DIGISELLER_API_KEY = os.environ.get('DIGISELLER_API_KEY')
DIGISELLER_SELLER_ID = int(os.environ.get('DIGISELLER_SELLER_ID'))


# Logging settings
def level_filter(levels):
    def is_level(record):
        return record['level'].name not in levels

    return is_level


logger.remove(0)

logger.add(sys.stderr, level="SUCCESS", filter=level_filter("ERROR"))
logger.add("logs/app.log", rotation="7 days")
