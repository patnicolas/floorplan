__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2023. All rights reserved."

from typing import AnyStr, NoReturn, TypeVar
import os
import smtplib, ssl

Instancetype = TypeVar('Instancetype', bound='SmtpClient')

"""
    Class that wraps the SMTP client with 2 constructors
    - Explicit SMTP/email parameters
    - SMTP/email parameters loaded from a configuration file
    version 0.1
"""


class SmtpClient(object):
    # SSL context as a static variables
    context = ssl.create_default_context()

    def __init__(self, smtp_server: AnyStr, user_name: AnyStr, password_key: AnyStr, receiver: AnyStr):
        """
        Default constructor for the SMTP client. An alternative constructor is to load a configuration
        file with the parameters
        :param smtp_server: DNS name for the SMTP server
        :param user_name: Username for the email
        :param password_key: Key to retrieve the password from environment variables
        :param receiver: Email address of the receiver (configurable)
        """
        self.smtp_server = smtp_server
        self.user_name = user_name
        self.password = os.getenv(password_key)
        self.receiver = receiver

    @classmethod
    def build_from_conf(cls) -> Instancetype:
        """
        Build a SMTP client from a CSV configuration file
        :return: Instance of SMTP client
        """
        from util.configutil import configuration_parameters
        is_test: bool = bool(configuration_parameters['is_test'] == 'True')
        if is_test:
            email_pwd = configuration_parameters['test_email_password_key']
            return cls(
                    configuration_parameters['test_smtp_server'],
                    configuration_parameters['test_email_name'],
                    email_pwd,
                    configuration_parameters['test_receiver'])
        else:
            email_pwd = configuration_parameters['email_password_key']
            email_pwd = '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'
            return cls(
                configuration_parameters['smtp_server'],
                configuration_parameters['email_name'],
                email_pwd,
                configuration_parameters['email_receiver'])

    def send_email_with_attachment(self, sender: AnyStr, attached_filename: AnyStr) -> bool:
        """
        Generate and send an email with attachment using parameters defined in the constructor, sender and
        attachment defined as arguments
        :param sender: Email address of the sender
        :param attached_filename: Absolute path for the file to attach
        :return: Return True if no exception if thrown, False otherwise
        """
        from email import encoders
        from email.mime.base import MIMEBase
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        try:
            from datetime import date
            today_date = date.today()

            # Step 1: Prepare the email
            subject, content = SmtpClient.__message_content(attached_filename)
            message = MIMEMultipart()
            message["From"] = sender
            message["To"] = self.receiver
            message["Subject"] = subject
            message["Date"] = str(today_date)
            message.attach(MIMEText(content, "html"))

            # Step 2: Load the attachment
            with open(attached_filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Step 3: Apply encoding
            encoders.encode_base64(part)

            # Step 4: Specify the minimum header
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={attached_filename}",
            )

            # Step 5: Add attachment to message and convert message to string
            message.attach(part)
            text = message.as_string()

            # Step 6: Fire/send email before a asynchronous sleep
            self.__fire_email(sender, text)
            # asyncio.sleep(2)
            return True
        except Exception as e:
            print(f'ERROR: {str(e)}')
            return False

        # ------------------  Helper methods ----------------------------
    @staticmethod
    def __message_content(filename: AnyStr) -> (AnyStr, AnyStr):
        subject = f"""Subject: Floor plan {filename} uploaded!"""
        content = f"""A new floor plan has been uploaded as {filename} into directory floorplan/floorplans\n\n"""
        return subject, content

    def __fire_email(self,sender: AnyStr, text: AnyStr) -> NoReturn:
        try:
            with smtplib.SMTP(self.smtp_server, 587) as server:
                server.starttls(context=SmtpClient.context)
                server.login(self.user_name, self.password)
                server.sendmail(sender, self.receiver, text)
                server.quit()
        except Exception as e:
            print(f'ERROR: {str(e)}')
            raise e


if __name__ == '__main__':
    smtp_client = SmtpClient.build_from_conf(True)
    test_sender = 'pnicolas57@yahoo.com'
    test_attachment = '../../floorplans/test.pdf'
    smtp_client.send_email_with_attachment(test_sender, test_attachment)

