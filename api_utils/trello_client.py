import requests
from typing import Dict, List
from config.config import Config


class TrelloClient:
    def __init__(self):
        self.api_key = Config.TRELLO_API_KEY
        self.token = Config.TRELLO_TOKEN
        self.board_id = Config.TRELLO_BOARD_ID
        self.base_url = "https://api.trello.com/1"

    def _make_request(self, url: str) -> Dict:
        """Makes an API request to Trello with error handling."""
        params = {'key': self.api_key, 'token': self.token}
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()  # Raise an error for non-200 responses
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to make request to Trello API: {str(e)}") from e

    def get_board_cards(self) -> List[Dict]:
        """Gets all cards from the board, handling potential API failures."""
        url = f"{self.base_url}/boards/{self.board_id}/cards"
        try:
            return self._make_request(url)
        except RuntimeError as e:
            return []  # Return empty list if API fails

    def get_card_by_title(self, title: str) -> Dict:
        """Finds a card by its title, returning None if not found."""
        try:
            cards = self.get_board_cards()
            return next((card for card in cards if card['name'] == title), None)
        except RuntimeError:
            return None

    def get_card_labels(self, card_id: str) -> List[str]:
        """Gets all labels for a specific card."""
        try:
            card = self.get_card_details(card_id)
            return [label['name'] for label in card.get('labels', [])]
        except RuntimeError:
            return []

    def get_card_details(self, card_id: str) -> Dict:
        """Gets detailed card information."""
        url = f"{self.base_url}/cards/{card_id}"
        return self._make_request(url)
