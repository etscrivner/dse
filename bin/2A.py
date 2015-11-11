#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    2A
    ~~
    The PSP Exercise 2A Program.

    This program takes a single python filename as a command-line argument and
    displays the number of physical lines of code in the file.

    is_single_line_comment(): Indicates whether the given line is a one-line
                              comment.
    is_multi_line_comment(): Indicates whether the given line is the start or
                             end of a multi-line comment.
    count_physical_loc(): Given a path to a python file this method will return
                          the number of physical lines of code (LOC) in the
                          file.
    main(): Parses command-line arguments and runs the program.
"""
import re
import sys


def is_single_line_comment(line):
    """Is this line a single-line comment?

    Arguments:
        line(str): The line of code

    Returns:
        bool: True if this is a single line comment, false otherwise
    """
    double_quote_comment = re.compile(r'""".*"""')
    single_quote_comment = re.compile(r"'''.*'''")
    return line.startswith("#") or double_quote_comment.match(line) or single_quote_comment.match(line)


def is_multi_line_comment(line):
    """Is this a multi-line comment?

    Arguments:
        line(str): The line of code

    Returns:
        bool: True if this represents a mult-line comment, false otherwise.
    """
    return line.startswith('"""') or line.startswith("'''")


def count_physical_loc(file_name):
    """Counts the number of physical lines of code in the given file.

    Given a file containing Python source code this method will return the
    number of physical lines of code in the file.

    Arguments:
        file_name(str): The path to the file.

    Returns:
        int: The number of physical lines of code in the file.
    """
    with open(file_name, 'r') as code_file:
        in_comment = False
        num_lines = 0
        for raw_line in code_file.readlines():
            line = raw_line.strip()
            # Skip blanks lines
            if not line:
                continue

            if is_single_line_comment(line):
                continue

            if is_multi_line_comment(line):
                # If already inside a multi-line comment, consider this the end
                # of that comment.
                if in_comment:
                    in_comment = False
                else:
                    # Otherwise, consider this the entry into a multi-line
                    # comment.
                    in_comment = True
                continue

            # If we're still inside of a comment, do not count this line.
            if in_comment:
                continue
            num_lines += 1
        return num_lines


def main():
    """The application entry point"""
    if len(sys.argv) < 2:
        print 'USAGE:'
        print 'program <FILENAME>'
        print 'FILENAME - A python file whose lines of code will be counted.'
        return
    file_name = sys.argv[1]
    physical_loc = count_physical_loc(file_name)
    print 'REPORT'
    print '======'
    print
    print 'Physical LOC: {}'.format(physical_loc)


if __name__ == '__main__':
    main()
