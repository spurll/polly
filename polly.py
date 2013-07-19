from argparse import ArgumentParser
from datetime import datetime
from time import sleep

from requests import get


DELAY = 60


def poll(address, delay=DELAY, silent=False):
    """
    Poll a website, returning once the contents of the website have changed.
    """
    if '://' not in address:  # No protocol given, default to http
        address = 'http://{}'.format(address)

    contents = get(address).text

    while True:
        new_contents = get(address).text

        if contents != new_contents:
            break

        if not silent:
            print datetime.now().strftime('Last Checked: %Y/%m/%d %H:%M:%S')

        sleep(delay)

    return True


def main():
    parser = ArgumentParser(description="Poll a website for changes")
    parser.add_argument('address', help="The address to poll")
    parser.add_argument('--delay', type=int, default=DELAY,
                        help="Time (in seconds) to delay between polls.")
    parser.add_argument('--silent', action='store_true',
                        help="Don't display alerts.")

    args = parser.parse_args()

    poll(args.address, delay=args.delay, silent=args.silent)


if __name__ == '__main__':
    main()
