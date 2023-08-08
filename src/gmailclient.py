from __future__ import print_function

__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2023. All rights reserved."

import os.path
import time

from src.configutil import configuration_parameters
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sys
import base64
from src.util.keyencryption import KeyEncryption
from email.message import EmailMessage
from typing import AnyStr


"""
    All scopes/functions used to recieve, create and send email using GMAIL SMTP server
    If modifying these scopes, delete the file token.json.
"""
SCOPES = [
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://mail.google.com/',
    'https://www.googleapis.com/auth/gmail.send'
]

"""
    Client for GMAIL SMTP server. The credentials file is encrypted for security reasons.
    
"""


class GmailClient(object):
    def __init__(self, credential_file: AnyStr = None):
        credentials = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time
        if os.path.exists('token.json'):
            credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if not credential_file:
                GmailClient.__decrypt_token()
                # We need to sleep this thread to allow the token file to be written
                time.sleep(3)
                credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
            else:
                if credentials and credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())
                else:
                    # To be safe we load the encrypted GMAIL credentials from local file.
                    key_encryption = KeyEncryption()
                    key_encryption.decrypt_file('encrypted_credentials', credential_file)
                    flow = InstalledAppFlow.from_client_secrets_file(credential_file, SCOPES)
                    credentials = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(credentials.to_json())
        self.service = build('gmail', 'v1', credentials=credentials)

    def send(self, sender: AnyStr, username: AnyStr, email: AnyStr, attachment: AnyStr) -> None:
        self.__notify_company(sender, username, email, attachment)
        self.__notify_sender(sender, attachment)
        time.sleep(2)

        # -------------  Supporting/Helper methods ------------------------

    def __notify_company(self, sender: AnyStr, username: AnyStr, email: AnyStr, attachment: AnyStr) -> None:
        try:
            subject, content = GmailClient.__notification_content(username, email, attachment)

            message = EmailMessage()
            message.set_content(content)
            message['To'] = configuration_parameters['email_receiver']
            message['From'] = sender
            message['Subject'] = subject

            with open(attachment, 'rb') as content_file:
                content = content_file.read()
                message.add_attachment(
                    content,
                    maintype='application',
                    subtype=(attachment.split('.')[1]),
                    filename=attachment)

            create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
            message = (self.service.users().messages().send(userId="me", body=create_message).execute())
            print(f'Notify Selections.ai from {sender} Message Id: {message["id"]}')
            sys.stdout.flush()
        except HttpError as error:
            print(f'An error occurred: {error}')
            sys.stdout.flush()

    def __notify_sender(self, sender: AnyStr, attachment: AnyStr):
        try:
            subject, content = GmailClient.__acknowledgment_message(attachment)

            message = EmailMessage()
            message.set_content(content)
            message['From'] = configuration_parameters['email_receiver']
            message['To'] = sender
            message['Subject'] = subject

            create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
            message = (self.service.users().messages().send(userId="me", body=create_message).execute())
            print(f'Notify sender {sender} Message Id: {message["id"]}')
            sys.stdout.flush()
        except HttpError as error:
            print(f'An error occurred: {error}')
            sys.stdout.flush()

    @staticmethod
    def __notification_content(user_name: AnyStr, email: AnyStr, filename: AnyStr) -> (AnyStr, AnyStr):
        subject = f"""Subject: Floor plan {filename} from {user_name} uploaded!"""
        content = f"""A new floor plan {filename} has been uploaded by {user_name} / {email} and attached to this email.\nA back up of the floor plan is stored at floorplan/floorplans\n\n"""
        return subject, content

    @staticmethod
    def __acknowledgment_message(filename: AnyStr) -> (AnyStr, AnyStr):
        subject = f"""Subject: Floor plan {filename} has been uploaded!"""
        content = f"""Your floor plan {filename} has been uploaded to Selections.ai\nFuture communication will use this email\nContact support@selections.ai for any questions\n\nWe appreciate your support"""
        return subject, content

    @staticmethod
    def __decrypt_token():
        import json
        import os
        keys = ['TOKEN', 'REFRESH_TOKEN', 'TOKEN_URI', 'CLIENT_ID', 'CLIENT_SECRET', 'EXPIRY']
        gmail_vars = {k.lower(): v for k, v in os.environ.items() if k in keys}
        gmail_vars['scopes'] = ['https://www.googleapis.com/auth/gmail.compose',
                                'https://www.googleapis.com/auth/gmail.modify',
                                'https://mail.google.com/',
                                'https://www.googleapis.com/auth/gmail.send']
        gmail_token_json = json.dumps(gmail_vars)
        with open('token.json', 'wt') as f:
            f.write(gmail_token_json)


if __name__ == '__main__':
    gmail_client = GmailClient()
    gmail_client.send('patrick@selections.ai', '../floorplans/test.pdf')

