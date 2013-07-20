import re

from formatter import Formatter


class RegexFormatter(Formatter):
    """
    A formatter that applies a regular expression to the response
    contents.
    """
    def __init__(self, expression):
        self.expression = expression

    def format(self, contents):
        value = None

        match = re.search(self.expression, contents)

        if match:
            if match.groups():
                value = match.groups()
            else:
                value = True

        return value

    @classmethod
    def get_name(cls):
        return 'regex'

    @classmethod
    def from_file(cls, options):
        return cls(options)
