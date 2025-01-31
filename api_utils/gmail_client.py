from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import base64
from email.mime.text import MIMEText
from typing import Dict, List

from config.config import Config


class GmailClient:
    def __init__(self):
        self.SCOPES = Config.GMAIL_SCOPES
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Handles Gmail authentication using OAuth 2.0"""
        if os.path.exists(Config.GMAIL_TOKEN_FILE):
            self.creds = Credentials.from_authorized_user_file(Config.GMAIL_TOKEN_FILE, self.SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(Config.GMAIL_CREDENTIALS_FILE, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open(Config.GMAIL_TOKEN_FILE, 'w') as token:
                token.write(self.creds.to_json())

        self.service = build('gmail', 'v1', credentials=self.creds)

    def send_email(self, subject: str, body: str):
        """Sends an email"""
        message = MIMEText(body)
        message['to'] = Config.GMAIL_USER
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        self.service.users().messages().send(userId='me', body={'raw': raw}).execute()

    def get_inbox_emails(self) -> List[Dict]:
        """Gets all inbox emails"""
        results = self.service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
        messages = results.get('messages', [])
        return [self._get_email_details(msg['id']) for msg in messages]

    def _get_email_details(self, msg_id: str) -> Dict:
        """Gets detailed email information"""
        msg = self.service.users().messages().get(userId='me', id=msg_id).execute()
        headers = msg['payload']['headers']
        subject = next(h['value'] for h in headers if h['name'].lower() == 'subject')

        return {
            'id': msg_id,
            'subject': subject,
            'body': msg['snippet']
        }

    def get_emails_subject_bodies(self):
        emails = [email for email in self.get_inbox_emails() if email['subject'] != "התראת אבטחה"]
        subject_bodies = {}

        for email in emails:
            subject = email['subject'].replace("Task: ", "").strip()
            body = email['body']

            # If the subject already exists in the dictionary, append the body
            if subject in subject_bodies:
                if body not in subject_bodies[subject] and body != "":
                    subject_bodies[subject].append(body)
            else:
                # If the subject doesn't exist, create a new entry with the body as the first element in the list
                subject_bodies[subject] = [body]
        return subject_bodies

    def get_bodies_as_string(self, bodies):
        if len(bodies) > 1:
            description = "\n".join(reversed(bodies))
        else:
            description = bodies[0]
        return description