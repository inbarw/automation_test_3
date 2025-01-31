import requests
from typing import Dict, List
from config.config import Config


class TrelloClient:
    def __init__(self):
        self.api_key = Config.TRELLO_API_KEY
        self.token = Config.TRELLO_TOKEN
        self.board_id = Config.TRELLO_BOARD_ID

        self.base_url = "https://api.trello.com/1"

    def get_board_cards(self) -> List[Dict]:
        """Gets all cards from the board"""
        url = f"{self.base_url}/boards/{self.board_id}/cards"
        return self._make_request(url)

    def _make_request(self, url: str) -> Dict:
        """Makes an API request to Trello"""
        params = {
            'key': self.api_key,
            'token': self.token
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_card_by_title(self, title: str) -> Dict:
        """Finds a card by its title"""
        cards = self.get_board_cards()
        return next((card for card in cards if card['name'] == title), None)

    def get_card_labels(self, card_id: str) -> List[str]:
        """Gets all labels for a specific card"""
        card = self.get_card_details(card_id)
        return [label['name'] for label in card.get('labels', [])]

    def get_card_details(self, card_id: str) -> Dict:
        """Gets detailed card information"""
        url = f"{self.base_url}/cards/{card_id}"
        return self._make_request(url)