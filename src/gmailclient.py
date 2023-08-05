from __future__ import print_function

__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2023. All rights reserved."

import os.path
from util.configutil import configuration_parameters
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from util.keyencryption import KeyEncryption
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
    def __init__(self, credential_file: AnyStr):
        credentials = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time
        if os.path.exists('token.json'):
            credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
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

    def send(self, sender: AnyStr, attachment: AnyStr):
        try:
            subject, content = GmailClient.__message_content(attachment)

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
            print(f'sent message to {message} Message Id: {message["id"]}')
        except HttpError as error:
            print(f'An error occurred: {error}')

    @staticmethod
    def __message_content(filename: AnyStr) -> (AnyStr, AnyStr):
        subject = f"""Subject: Floor plan {filename} uploaded!"""
        content = f"""A new floor plan has been uploaded as {filename} into directory floorplan/floorplans\n\n"""
        return subject, content


if __name__ == '__main__':
    gmail_client = GmailClient('credentials.json')
    gmail_client.send('patrick@selections.ai', '../floorplans/test.pdf')

