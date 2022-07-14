import unittest
from apis import twilio
import helpers
import os
helpers.modify_system_path()

class TestSendgrid(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSendgrid, self).__init__(*args, **kwargs)

    def test_can_import_sendgrid(self, *args, **kwargs):
        from sendgrid.helpers.mail import Mail
        self.assertNotEqual(str(Mail).find('Mail'), -1)

    def test_can_import_sendgrid_api_module(self, *args, **kwargs):
        self.assertNotEqual(
            str(twilio.send_mail).find('function send_mail'), -1)

    def test_can_send_email(self, *args, **kwargs):
        email_address = input("Please enter your email address: ")
        self.assertTrue(twilio.send_mail(
                email_address,
                email_address,
                f"[CS 110] {os.getlogin()} Test Successful",
                "Twilio Test Successful.")
                )


if __name__ == '__main__':
    unittest.main()
