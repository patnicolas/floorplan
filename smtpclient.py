__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

from typing import AnyStr, NoReturn, TypeVar
import os
import smtplib, ssl
import asyncio

Instancetype = TypeVar('Instancetype', bound='SmtpClient')



class SmtpClient(object):
    context = ssl.create_default_context()

    def __init__(self, smtp_server: AnyStr, user_name: AnyStr, password_key: AnyStr, receiver: AnyStr):
        self.smtp_server = smtp_server
        self.user_name = user_name
        self.password = os.getenv(password_key)
        self.receiver = receiver

    @classmethod
    def build_from_conf(cls, config_file: AnyStr) -> Instancetype:
        from util.testutil import TestUtil

        test_util = TestUtil(config_file)
        test_variables = test_util.load_test_variables()
        return cls(
                test_variables['test_smtp_server'],
                test_variables['test_email_name'],
                test_variables['test_email_password_key'],
                test_variables['test_receiver'])

    async def send_email_with_attachment(self, sender: AnyStr, attached_filename: AnyStr) -> bool:
        from email import encoders
        from email.mime.base import MIMEBase
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        try:
            from datetime import date
            today_date = date.today()

            subject, content = SmtpClient.__message_content(attached_filename)
            message = MIMEMultipart()
            message["From"] = sender
            message["To"] = self.receiver
            message["Subject"] = subject
            message["Date"] = str(today_date)
            message.attach(MIMEText(content, "plain"))

            with open(attached_filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={attached_filename}",
            )

            # Add attachment to message and convert message to string
            message.attach(part)
            text = message.as_string()
            self.__fire_email(sender, receiver, text)
            await asyncio.sleep(1)
            return True
        except Exception as e:
            print(str(e))
            return False

    @staticmethod
    def __message_content(filename: AnyStr) -> (AnyStr, AnyStr):
        subject = f"""Subject: Floor plan {filename} uploaded!"""
        content = f"""A new floor plan has been uploaded as {filename} into directory floorplan/floorplans\n\n"""
        return subject, content

    def __fire_email(
            self,
            sender: AnyStr,
            receiver: AnyStr,
            text: AnyStr) -> NoReturn:
        try:
            with smtplib.SMTP(self.smtp_server, 587) as server:
                server.starttls(context=SmtpClient.context)
                server.login(self.user_name, self.password)
                server.sendmail(sender, receiver, text)
                server.quit()
        except Exception as e:
            print(str(e))
            raise e


if __name__ == '__main__':
    smtp_client = SmtpClient.build_from_conf('test_input/test.csv')
    test_sender = 'pnicolas57@yahoo.com'
    test_attachment = 'floorplans/test.pdf'
    asyncio.run(smtp_client.send_email_with_attachment(test_sender, test_attachment))

