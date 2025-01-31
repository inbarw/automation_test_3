import base64
from unittest.mock import MagicMock
from utils.api_clients import TrelloClient

class TestGmailToTrello:
    def setup_method(self):
        self.gmail_service = MagicMock()
        self.gmail_service.users().messages().get.return_value.execute.return_value = {
                'subject': 'This is a great day',
                'body': 'UGxlYXNlIHByb3ZpZGUgYWxsIHRoZSByZWxldmFudCBpbmZvcm1hdGlvbiByZWdhcmRpbmcgdGhlIHVwY29taW5nIGV2ZW50LiBUaGlzIGlzIG9wcG9ydHVuaXR5IGZvciBhbGwgb2YgdXMgYXRvIHdhdGNoIGl0IGhhcHBlbnMsIGFmdGVyIGVuYW5jaW5nIGFsbCBvZiBvdXIgaW5lcmd5IHRvIG1heGltaXplIHRoZSByZXN1bHMuIERvIG5vdCBtaXNzIGl0LiBUaGlzIGlzIGEgbGlmZSB0aW1lIGNoYW5jZS4gRG9uJ3QgdGhpbmsgdG8gb21lIGp1c3Qgbm8gaXQuIFdlIGFyZSBzbyBoYXBweSB0aGF0IHdlIGJlY2FtZSB0aGF0IHdlIHJlYWNoZWQgdGhpcyBwb2ludCBhbmQgZmluYWxseSB3ZSBjYW4gYW5ub3VuY2UgdGhpcyBkZWNpc2lvbi4gSSdtIHN1cmUgdGhhdCBldmVyeXRob25lIHdpbGwgbm9dIHdoZW4gd2UgYXJlIHNvIGhhcHB5IHRoYXQgd2UgcmlzZSB3aXRoIHN1Y2ggcG9pbnQuCg=='

        }
        self.trello = TrelloClient()

    def test_sending_email(self):
        email = self.gmail_service.users().messages().get(userId='me', id='123').execute()
        subject = email["subject"]
        body = email['body']

        # Decode the base64url encoded email body
        decoded_body = base64.urlsafe_b64decode(body).decode('utf-8')

        card = self.trello.get_card_by_title(subject)
        assert card, f"Can't find card for {subject} email"
        assert card["desc"] == decoded_body, "Failed to verify that correct card description is displayed"


