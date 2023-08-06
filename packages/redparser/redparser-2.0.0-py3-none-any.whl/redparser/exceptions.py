import sys

from .constants import help

# define redparser user-defined exceptions
class RedParserError(Exception):
    """Base class for other exceptions"""
    pass

class HelpError():
    """
    Exception raised for command line with no arguments or with -h or --help in arguments
    in the command line arguments.

    Attributes:
        help -- redparser help output
    """
    def __init__(self, help=help):
        self.help = help
        print(self.help)
        # stop the program
        sys.exit(1)

class NonUniqueCmdlineArgumentError(HelpError):
    """
    Exception raised for errors in the command line arguments.

    Attributes:
        nonunique -- the command argument that was added multiple times
        message -- explanation of the error
    """

    def __init__(self, nonunique, message=" entered more than once. Please only enter command once"):
        self.nonunique = nonunique
        self.message = message
        print(self.nonunique + self.message)
        super().__init__()

class ArgumentError(HelpError):
    """
    Exception raised for errors in the command line arguments.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        print(self.message)
        super().__init__()

class LogReadError(HelpError):
    """
    Exception raised for errors in the reading log.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        print(self.message)
        super().__init__()