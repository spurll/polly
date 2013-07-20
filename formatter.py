"""
An object that can be used to format polly contents.
"""
import abc


class Formatter(object):
    """
    An object that can be used to format polly contents.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def format(self, contents):
        raise NotImplementedError

    @classmethod
    def get_name(cls):
        """
        Get the command-line name of the formatter
        """
        raise NotImplementedError

    @classmethod
    def from_file(cls, options):
        """
        Load the formatter from json-serialized data.

        options: The options from the data.
        """
        raise NotImplementedError
