""" SDA Custom Exceptions Docstring
This module serves as a holder for all custom exceptions this project will use.

Example:
    - InputError
    from exceptions import InputError

    try:
        raise: Exception("Some Exception")
    except Exception as exception:
        raise InputError("Could not perform task", exception.args)
"""


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InputError(Error):
    """Input Error, used to throw an error when user input is incorrect."""

    def __init__(self, message, args):
        """Initializes input error
        Args:
            message: User facing message. This is the message that will be
                displayed to the user.
            args: Additional arguments that should be passed up the stack.
                This will usually be the original exception that was caught.
        """
        Error.__init__(self)
        self.message = message
        self.args = args


class MySqlError(Error):
    """MySQL Error, used to throw an error when a MySQL Server error occurs"""

    def __init__(self, message, args):
        """
        Initializes MySql error
        Args:
            message: User facing message. This is the message that will be
                displayed to the user.
            args: Additional arguments that should be passed up the stack.
                This will usually be the original exception that was caught.
        """
        Error.__init__(self)
        self.message = message
        self.args = args
