from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import json
from bs4 import BeautifulSoup
from datetime import datetime
from model.Message import Message, Attachment

user_id = 'me'
label_inbox = 'INBOX'
label_unread = 'UNREAD'
token_pickle_path = 'token.pickle'
credentials_path = 'credentials.json'

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class Mail:

    def __init__(self):
        creds = None
        service = None

    def build_service(self):
        if os.path.exists(token_pickle_path):
            with open(token_pickle_path, 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_pickle_path, 'wb') as token:
                pickle.dump(self.creds, token)
        self.service = build('gmail', 'v1', credentials=self.creds)

    def get_messages(self, labels = [], index = None):
        msgs = self.service.users().messages().list(userId='me', labelIds=labels).execute()
        messages = msgs.get('messages', [])

        if index is None:
            return messages
        else:
            return messages[index]

    def get_unread_mesages(self):
        return self.get_messages([label_inbox, label_unread])

    def get_last_message(self):
        return self.get_messages([label_inbox], 0)

    def get__inbox_message(self, index = 0):
        return self.get_messages([label_inbox], index)

    def get_message(self, msg_id):
        # possible formats: ['full', 'metadata', 'minimal', 'raw']
        subject = None
        msg = self.service.users().messages().get(userId='me', id=msg_id).execute()

        # parse date
        date = float(msg['internalDate']) / 1000
        date = datetime.utcfromtimestamp(date)

        # parse subject
        headers = msg['payload']['headers']
        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']

        # parse attachments
        attachments_raw = []
        for part in msg['payload']['parts']:
            if part['filename']:
                attachments_raw.append((part['filename'], part['body']['attachmentId']))

        attachments = []
        for attachment in attachments_raw:
            att = self.service.users().messages().attachments().get(
                userId='me', id=attachment[1], messageId=msg_id).execute()
            data = att['data']

            file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))

            attachments.append(Attachment(attachment[0], file_data))

        # parse body
        parts = msg['payload']['parts']
        if self.is_contains_attachment(parts):
            data =  parts[0]['parts'][0]['body']['data']
        else:
            data = parts[0]['body']['data']
        clean = base64.urlsafe_b64decode(data)
        soup = BeautifulSoup(clean, "lxml")
        body = soup.body()

        return Message(date, subject, body, attachments)


    def get_message_text(self, msg_id):
        # possible formats: ['full', 'metadata', 'minimal', 'raw']
        msg = self.service.users().messages().get(userId='me', id=msg_id, format='full', prettyPrint=True).execute()

        parts = msg['payload']['parts']
        if self.is_contains_attachment(parts):
            data =  parts[0]['parts'][0]['body']['data']
        else:
            data = parts[0]['body']['data']
        clean = base64.urlsafe_b64decode(data)
        soup = BeautifulSoup(clean, "lxml")
        mssg_body = soup.body()
        return mssg_body

    def is_contains_attachment(self, msgs):
        for part in msgs:
            if part['filename']:
                return True
        return False

def main():
    a = Mail()
    a.build_service()
    last_msg = a.get__inbox_message(3)

    msg = a.get_message(last_msg['id'])
    print(msg)

if __name__ == '__main__':
    main()