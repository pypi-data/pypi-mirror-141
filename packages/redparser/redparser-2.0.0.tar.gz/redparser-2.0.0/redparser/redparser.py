#!/usr/bin/python3
import sys

from .parser import Parser
from .arguments import Arguments
from .exceptions import HelpError, LogReadError

"""
Redparser - parsing log file based upon command line argument

This main function is the entry point to the redparser library

"""
def main():

    # exclude the python interpreter
    termargs = sys.argv[1:]
    
    # length of terminal arguments to be used for redparser
    termargs_length = len(termargs)

    # check if help was called or no arguments supplied
    if '-h' in termargs or '--help' in termargs or termargs_length == 0:
        HelpError()

    try:
        with open(sys.argv[-1], 'rb') as file_obj:
            mmap_possible = 1
            args = Arguments(termargs, mmap_possible)
            p = Parser(file_obj, args)
            p.run()
    except Exception:
        try:
            if not sys.stdin.isatty():
                file_obj = sys.stdin.buffer.read()
                mmap_possible = 0
                args = Arguments(termargs, mmap_possible)
                p = Parser(file_obj, args)
                p.run()

        except Exception:
            LogReadError("Error reading log file please pipe data to python file or have log file at end of command\n")

if __name__ == '__main__':

    main()