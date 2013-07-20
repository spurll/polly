"""
An object that can be used to hook actions into polly.
"""


class Trigger(object):
    """
    An object that can be used to hook actions into polly.
    """
    def at_startup(self, address, initial):
        """
        Hook method for any initialization that needs to occur prior
        to the start of polling.

        address: The address being monitored.
        initial: The initial contents.

        NOTE: initial is not guaranteed to be a string.
        """
        pass

    def on_change(self, old, new):
        """
        Hook method for any action that should be taken upon a change
        being detected.

        old: The contents prior to the change.
        new: The new contents.

        NOTE: old, new are not guaranteed to be strings.
        """
        pass

    def at_exit(self, contents):
        """
        Hook method for any teardown that needs to occur prior to
        exitting the poll loop.

        contents: The last value contents held.

        NOTE: contents is not guaranteed to be a string.
        """
        pass

    @classmethod
    def get_name(cls):
        """
        Get the command-line name of the trigger
        """
        raise NotImplementedError

    @classmethod
    def from_file(cls, options):
        """
        Load the trigger from json-serialized data.

        options: The options from the data.
        """
        raise NotImplementedError
