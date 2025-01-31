import base64
from unittest.mock import MagicMock

import allure

from api_utils.trello_client import TrelloClient

class TestGmailToTrello:
    def setup_method(self):
        self.gmail_service = MagicMock()
        self.gmail_service.users().messages().get.return_value.execute.return_value = {
                'subject': 'This is a great day',
                'body': """Please  provide all the relevant information regarding the upcoming event. This is opportunity for all of us to watch it happens, after enhancing all of our energy to maximize the results. Do not miss it This is a life time chance. Don’t think too much just do it. We are so happy that we reached this point and finally we can announce about this decision. I’m sure that everyone will find it existing. Cant' wait to see you there!"""
        }
        self.trello = TrelloClient()

    @allure.title("Verify Email Processing and Trello Card Creation")
    def test_sending_email(self):
        with allure.step("Retrieve email content from mocked Gmail service"):
            email = self.gmail_service.users().messages().get(userId='me', id='123').execute()
            subject = email["subject"]
            body = email['body']

        with allure.step("Verify Trello card exists"):
            card = self.trello.get_card_by_title(subject)
            assert card, f"Can't find card for {subject} email"

        with allure.step("Verify Trello card description matches email body"):
            assert card["desc"] == body, f"Mismatch! Expected: {body}, Actual: {card['desc']}"


