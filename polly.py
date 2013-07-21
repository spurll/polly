from __future__ import print_function

from argparse import ArgumentParser
from datetime import datetime
import json
from time import sleep

from requests import get

from mailtrigger import MailTrigger, SMTPHOST
from regexformatter import RegexFormatter


DELAY = 60


def poll(address, delay=DELAY, triggers=None, formatter=None,
         silent=False, eternal=False):
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

    contents = get_content(get(address), formatter)

    for trigger in triggers:
        trigger.at_startup(address, contents)

    while True:
        new_contents = get_content(get(address), formatter)

        if contents != new_contents:
            for trigger in triggers:
                trigger.on_change(contents, new_contents)

            contents = new_contents

            if eternal:
                if not silent:
                    print('A change has occured at: {}'.format(address))
            else:
                break
        elif not silent:
            print(datetime.now().strftime('Last Checked: %Y/%m/%d %H:%M:%S'))

        sleep(delay)

    for trigger in triggers:
        trigger.at_exit(contents)


def get_content(response, formatter=None):
    """
    Get the filtered content from the response.
    """
    content = response.text

    if formatter:
        content = formatter.format(content)

    return content


def main():
    potential_triggers = {trigger.get_name(): trigger for trigger in
                          [MailTrigger]}
    potential_formatters = {formatter.get_name(): formatter for formatter in
                            [RegexFormatter]}

    parser = ArgumentParser(description="Poll a website for changes")
    parser.add_argument('address', help="The address to poll")
    parser.add_argument('--delay', type=int, default=DELAY,
                        help="Time (in seconds) to delay between polls.")
    parser.add_argument('--silent', action='store_true',
                        help="Don't display alerts.")
    parser.add_argument('--eternal', action='store_true',
                        help="Don't quit when the website changes; keep going.")

    parser.add_argument('--settings', help="A file containing settings")

    # ArgumentParser doesn't support optional groups or subparsers.
    # Until I find a workaround, mail, regex gets special status.
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
    parser.add_argument(
        '--regex', '-r', help="A regular expression to filter content with.")

    args = parser.parse_args()

    triggers = []

    if args.recipients:
        triggers.append(MailTrigger(args.recipients, username=args.username,
                                    password=args.password, bcc=args.bcc,
                                    host=args.host))

    formatter = RegexFormatter(args.regex) if args.regex else None

    if args.settings:
        with open(args.settings, 'r') as file_pointer:
            data = json.load(file_pointer)

        for name, options in data.get('triggers', {}).iteritems():
            triggers.append(potential_triggers[name].from_file(options))

        if 'formatter' in data:
            formatter = potential_formatters[
                data['formatter']['name']].from_file(
                    data['formatter']['options'])

    poll(args.address, delay=args.delay, triggers=triggers,
         formatter=formatter, silent=args.silent, eternal=args.eternal)


if __name__ == '__main__':
    main()
