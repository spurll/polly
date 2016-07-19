"""
Send a Slack message when polly registers a change.
"""
from getpass import getpass
from slackutils import Slack

from trigger import Trigger


class SlackTrigger(Trigger):
    """
    Send a Slack message when polly registers a change.
    """
    def __init__(self, recipients, token, message=None, name=None, icon=None):
        self.recipients = recipients
        self.name = name if name is not None else "Polly"
        self.icon = icon if icon is not None else ":bird:"
        self.token = token
        self.message = message if message is not None else (
            "A site you're watching has been updated!"
        )

    def at_startup(self, address, initial):
        if self.token is None:
            self.token = getpass('slack api token: ')

        # authenticate and test
        self.slack = Slack(self.token, self.name, self.icon)
        if self.slack.error:
            raise Exception("Slack Error: {}".format(self.slack.error))

        # build message
        self.message += " A change has occurred at: {}".format(address)

    def on_change(self, old, new):
        for recipient in self.recipients:
            self.slack.send(recipient, self.message, notify=True,
                            unfurl_links=True)

            if self.slack.error:
                print("Slack Error: {}".format(self.slack.error))

    @classmethod
    def get_name(cls):
        return 'slack'

    @classmethod
    def from_file(cls, options):
        return cls(**options)
