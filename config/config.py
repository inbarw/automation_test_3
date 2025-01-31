import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Gmail Configuration
    BASE_DIR = Path(__file__).resolve().parent.parent
    GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    GMAIL_TOKEN_FILE = BASE_DIR / 'qa_automation_assignment' / 'token.json'
    GMAIL_CREDENTIALS_FILE = BASE_DIR / 'qa_automation_assignment' /'credentials.json'
    GMAIL_USER = os.getenv('GMAIL_USER', 'droxiautomation@gmail.com')

    # Trello Configuration
    TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
    TRELLO_TOKEN = os.getenv('TRELLO_TOKEN')
    TRELLO_BOARD_ID = os.getenv('TRELLO_BOARD_ID', '2GzdgPlw')

    # Test Configuration
    SYNC_WAIT_TIME = 10  # seconds to wait for sync