from api_utils import gmail_client, trello_client
from api_utils.gmail_client import GmailClient
from utils.api_clients import TrelloClient


class TestGmailTrelloSync:
    def setup_method(self):
        self.gmail = GmailClient()
        self.trello = TrelloClient()

    def test_urgent_email_sync(self):
        emails = [email for email in self.gmail.get_inbox_emails() if email['subject'] != "התראת אבטחה"]

        for email in emails:
            subject = email['subject'].replace("Task: ", "").strip()
            body = email['body']

            card = self.trello.get_card_by_title(subject)
            if card:
                card_labels = self.trello.get_card_labels(card['id'])
            else:
                card_labels = []

            if "urgent" in body.lower():
                assert "Urgent" in card_labels, f"Email with subject '{subject}' should have 'Urgent' label."

    def test_merge(self):
        subject_bodies = self.gmail.get_emails_subject_bodies()

        for subject, bodies in subject_bodies.items():
            description = self.gmail.get_bodies_as_string(bodies)
            card  = self.trello.get_card_by_title(subject)
            assert card["desc"] == description





