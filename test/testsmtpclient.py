from unittest import TestCase
from src.smtpclient import SmtpClient
import asyncio


class TestSmtpClient(TestCase):
    def test_smtp_with_attachment(self):
        test_script_file = '../config.csv'
        smtp_client = SmtpClient.build_from_conf(test_script_file)
        test_sender = 'pnicolas57@yahoo.com'
        test_attachment = '../floorplans/test.pdf'
        asyncio.run(smtp_client.send_email_with_attachment(test_sender, test_attachment))
