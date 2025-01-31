import allure

from api_utils.gmail_client import GmailClient
from api_utils.trello_client import TrelloClient


class TestGmailTrelloSync:
    def setup_method(self):
        self.gmail = GmailClient()
        self.trello = TrelloClient()

    @allure.title("Verify urgent email sync to Trello with 'Urgent' label")
    def test_urgent_email_sync(self):
        emails = [email for email in self.gmail.get_inbox_emails() if email['subject'] != "התראת אבטחה"]

        for email in emails:
            subject = email['subject'].replace("Task: ", "").strip()
            body = email['body']

            with allure.step(f"Retrieve Trello card for subject '{subject}'"):
                card = self.trello.get_card_by_title(subject)
                if card:
                    card_labels = self.trello.get_card_labels(card['id'])
                else:
                    card_labels = []

            with allure.step(f"Check if email body contains 'urgent'"):
                if "urgent" in body.lower():
                    assert "Urgent" in card_labels, f"Email with subject '{subject}' should have 'Urgent' label."

    @allure.title("Verify Trello card merging for same email subject")
    def test_merging(self):
        subject_bodies = self.gmail.get_emails_subject_bodies()

        for subject, bodies in subject_bodies.items():
            description = self.gmail.get_bodies_as_string(bodies)
            card  = self.trello.get_card_by_title(subject)

            with allure.step(f"Verify Trello card description matches email content for '{subject}'"):
                assert card["desc"] == description, f"Description mismatch for '{subject}'"





