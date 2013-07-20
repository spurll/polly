from argparse import ArgumentParser
from datetime import datetime
import json
from time import sleep

from requests import get

from mailtrigger import MailTrigger, SMTPHOST


DELAY = 60


def poll(address, delay=DELAY, triggers=None, silent=False, eternal=False):
    """
    Poll a website for changes.

    address: The address to poll.
    delay: The delay (in seconds) between each poll.
    triggers: A list of triggers to call on site changes.
    silent: Don't print alerts.
    eternal: Don't quit when the site changes (just send the email).
    """
    if triggers is None:
        triggers = []

    if '://' not in address:  # No protocol given, default to http
        address = 'http://{}'.format(address)

    contents = get(address).text

    for trigger in triggers:
        trigger.at_startup(address, contents)

    while True:
        new_contents = get(address).text

        if contents != new_contents:
            for trigger in triggers:
                trigger.on_change(contents, new_contents)

            contents = new_contents

            if eternal:
                if not silent:
                    print 'A change has occured at: {}'.format(address)
            else:
                break
        elif not silent:
            print datetime.now().strftime('Last Checked: %Y/%m/%d %H:%M:%S')

        sleep(delay)

    for trigger in triggers:
        trigger.at_exit(contents)


def main():
    potential_triggers = {trigger.get_name(): trigger for trigger in
                          [MailTrigger]}

    parser = ArgumentParser(description="Poll a website for changes")
    parser.add_argument('address', help="The address to poll")
    parser.add_argument('--delay', type=int, default=DELAY,
                        help="Time (in seconds) to delay between polls.")
    parser.add_argument('--silent', action='store_true',
                        help="Don't display alerts.")
    parser.add_argument('--eternal', action='store_true',
                        help="Don't quit when the website changes; keep going.")

    parser.add_argument('--trigger_file', action='append',
                        help="A file containing trigger info")

    # ArgumentParser doesn't support optional groups or subparsers.
    # Until I find a workaround, mail gets special status.
    parser.add_argument('--mail', '-m', dest='recipients', action='append',
                        help="An address to email when polling is finished "
                        "(flag can be used multiple times)")
    parser.add_argument('--host', default=SMTPHOST,
                        help="The SMTP host to use for emailing.")
    parser.add_argument('--username', '-u', default=None,
                        help="The username for SMTP login.")
    parser.add_argument('--password', '-p', default=None,
                        help="The password for SMTP login.")
    parser.add_argument('--bcc', action='store_true',
                        help="BCC recipients instead of putting names in 'To'")

    args = parser.parse_args()

    triggers = []

    if args.recipients:
        triggers.append(MailTrigger(args.recipients, username=args.username,
                                    password=args.password, bcc=args.bcc,
                                    host=args.host))

    for trigger_file in args.trigger_file:
        with open(trigger_file, 'r') as file_pointer:
            data = json.load(file_pointer)

        for name, options in data.iteritems():
            triggers.append(potential_triggers[name].from_file(options))

    poll(args.address, delay=args.delay, triggers=triggers,
         silent=args.silent, eternal=args.eternal)


if __name__ == '__main__':
    main()
