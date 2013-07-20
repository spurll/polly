"""
Send emails when polly registers a change.
"""
from email.mime.text import MIMEText
from getpass import getpass
from smtplib import SMTP

from trigger import Trigger


SMTPHOST = 'smtp.gmail.com:587'


class MailTrigger(Trigger):
    """
    Send emails when polly registers a change.
    """
    def __init__(self, recipients, username=None, password=None,
                 subject=None, bcc=False, host=SMTPHOST):
        if subject is None:
            subject = "Polly: A website you're watching has been updated"

        self.recipients = recipients
        self.username = username
        self.password = password
        self.subject = subject
        self.subject = subject
        self.bcc = bcc
        self.host = host

        self.message = None
        self.smtp = None

    def connect(self):
        """
        Connect to the smtp host.
        """
        self.smtp = SMTP(self.host)
        self.smtp.starttls()
        self.smtp.login(self.username, self.password)

    def disconnect(self):
        """
        Disconnect from the smtp host.
        """
        self.smtp.close()

    def at_startup(self, address, initial):
        # get login credentials
        if self.username is None:
            self.username = getpass('user: ')

        if self.password is None:
            self.password = getpass('password: ')

        # test smtp login
        self.connect()
        self.disconnect()

        # build message
        message = MIMEText("A change has occured at: {}".format(address))
        message['subject'] = "Polly: A site you're watching has been updated!"

        if not self.bcc:
            message['To'] = ', '.join(self.recipients)

        self.message = message.as_string()

    def on_change(self, old, new):
        self.connect()

        if self.bcc:
            for recipient in self.recipients:
                self.smtp.sendmail(self.username, [recipient], self.message)
        else:
            self.smtp.sendmail(self.username, self.recipients, self.message)

        self.disconnect()

    @classmethod
    def get_name(cls):
        return 'mail'

    @classmethod
    def from_file(cls, options):
        return cls(**options)
