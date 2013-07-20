from argparse import ArgumentParser
from datetime import datetime
from email.mime.text import MIMEText
from getpass import getpass
from smtplib import SMTP
from time import sleep

from requests import get


DELAY = 60
SMTPHOST = 'smtp.gmail.com:587'


def poll(address, delay=DELAY, silent=False, recipients=None, user=None,
         password=None, host=SMTPHOST, bcc=False, eternal=False):
    """
    Poll a website, returning once the contents of the website have changed.

    address: The address to poll.
    delay: The delay (in seconds) between each poll.
    silent: Don't print alerts
    eternal: Don't quit when the site changes (just send the email)
    recipients: The list of email recipients.
    user: The user account for emailing (if not given, a prompt will be used).
    password: The password for emailing (if not given, a prompt will be used).
    host: The smtp host.
    bcc: Whether to bcc people
    """
    if recipients:
        if user is None:
            user = getpass('user: ')

        if password is None:
            password = getpass('password: ')

        # test smtp login
        smtp = SMTP(host)
        smtp.starttls()
        smtp.login(user, password)

        smtp.close()

    if '://' not in address:  # No protocol given, default to http
        address = 'http://{}'.format(address)

    contents = get(address).text

    while True:
        new_contents = get(address).text

        if contents != new_contents:
            if recipients:
                send_mail(host=host, user=user, password=password,
                          recipients=recipients, address=address, bcc=bcc)
            if eternal:
                contents = new_contents
                if not silent:
                    print 'A change has occured at: {}'.format(address)
            else:
                return True

        if not silent:
            print datetime.now().strftime('Last Checked: %Y/%m/%d %H:%M:%S')

        sleep(delay)


def send_mail(host, user, password, recipients, address, bcc=False):
    smtp = SMTP(host)
    smtp.starttls()
    smtp.login(user, password)

    message = MIMEText("A change has occured at: {}".format(address))
    message['Subject'] = "Polly: A website you're watching has been updated!"

    if bcc:
        for recipient in recipients:
            smtp.sendmail(user, [recipient], message.as_string())
    else:
        message['To'] = ', '.join(recipients)
        smtp.sendmail(user, recipients, message.as_string())

    smtp.close()


def main():
    parser = ArgumentParser(description="Poll a website for changes")
    parser.add_argument('address', help="The address to poll")
    parser.add_argument('--delay', type=int, default=DELAY,
                        help="Time (in seconds) to delay between polls.")
    parser.add_argument('--silent', action='store_true',
                        help="Don't display alerts.")
    parser.add_argument('--eternal', action='store_true',
                        help="Don't quit when the website changes; keep going.")
    parser.add_argument('--mail', '-m', dest='recipients', action='append',
                        help="An address to email when polling is finished "
                        "(flag can be used multiple times)")
    parser.add_argument('--host', default=SMTPHOST,
                        help="The SMTP host to use for emailing.")
    parser.add_argument('--user', '-u', default=None,
                        help="The username for SMTP login.")
    parser.add_argument('--password', '-p', default=None,
                        help="The password for SMTP login.")
    parser.add_argument('--bcc', action='store_true',
                        help="BCC recipients instead of putting names in 'To'")

    args = parser.parse_args()

    poll(args.address, delay=args.delay, silent=args.silent,
         recipients=args.recipients, user=args.user, password=args.password,
         host=args.host, bcc=args.bcc, eternal=args.eternal)


if __name__ == '__main__':
    main()
