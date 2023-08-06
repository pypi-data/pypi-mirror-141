import sys

from .validator import validate_first, validate_last, validate_ipv4, validate_ipv6, validate_timestamp
from .exceptions import NonUniqueCmdlineArgumentError, ArgumentError
from .constants import ip_argument_invalids


class Arguments:

    def __init__(self, terminal_arguments, mmap_possible):
        self.first = None
        self.last = None
        self.timestamps = None
        self.ipv4 = None
        self.ipv6 = None
        self.termargs = terminal_arguments
        self.termargs_length = len(terminal_arguments)
        self.mmap = mmap_possible
        self.skip = False

        self.enable_mmap()
        self.run()

    def unique(self, key):
        if self.termargs.count(key) - 1:
            NonUniqueCmdlineArgumentError(key)

    def enable_mmap(self):
        if self.mmap:
            # log file at end so no need to parse this
            self.termargs_length -= 1
            self.termargs = self.termargs[:self.termargs_length]

    def run(self):
        for index, argument in enumerate(self.termargs):
            if self.skip:
                self.skip = False
                continue

            if argument == '--first' or argument == '-f':
                self.unique(argument)
                if index + 1 >= self.termargs_length or not validate_first(self.termargs[index + 1]):
                    ArgumentError("Input a positive number for the --first command\n")

                self.first = int(self.termargs[index + 1])
                self.skip = True

            elif argument == '--last' or argument == '-l':
                self.unique(argument)
                if index + 1 >= self.termargs_length or not validate_last(self.termargs[index + 1]):
                    ArgumentError("Input a positive number for the --last command\n")

                self.last = int(self.termargs[index + 1])
                self.skip = True

            elif argument == '--timestamps' or argument == '-t':
                self.unique(argument)
                self.timestamps = True

            elif argument == '--ipv4' or argument == '-i':
                self.unique(argument)
                if index + 1 < self.termargs_length and (self.termargs[index + 1]not in ip_argument_invalids):
                    if not validate_ipv4(self.termargs[index + 1]):
                        ArgumentError("Input a valid ipv4 address for the --ipv4 command\n")

                    self.ipv4 = self.termargs[index + 1]
                    self.skip = True

                else:
                    self.ipv4 = True

            elif argument == '--ipv6' or argument == '-I':
                self.unique(argument)
                if index + 1 < self.termargs_length and (self.termargs[index + 1] not in ip_argument_invalids):
                    if not validate_ipv6(self.termargs[index + 1]):
                        ArgumentError("Input a valid ipv6 address for the --ipv6 command\n")

                    self.ipv6 = self.termargs[index + 1]
                    self.skip = True
                else:
                    self.ipv6 = True

            else:
                ArgumentError("You inputted an unknown commands\n")
