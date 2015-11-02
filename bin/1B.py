# -*- coding: utf-8 -*-
"""
    1B
    ~~
    The PSP Exercise 1B Program.

    
"""
import os

from lib import io


def read_file(file_path):
    """Reads numerical values from a file a displays them to a user.

    Arguments:
        file_path(basestring): The path to the file
    """
    with open(file_path, 'r') as rfile:
        for each in rfile.readlines():
            print float(each)


def write_file(file_path):
    """Requests a series of numerical inputs and writes them to the file.

    Arguments:
        file_path(basestring): The path to the file
    """
    if os.path.isfile(file_path):
        should_overwrite = io.yes_no_prompt('File {} exists. Overwrite?')
        # If the file shouldn't be overwritten, abort
        if not should_overwrite:
            return

    total_num_entries = io.get_and_confirm_input(
        'How many numbers will you enter: ')
    total_num_entries = int(total_num_entries)

    num_entries_given = 0

    with open(file_path, 'w') as wfile:
        while num_entries_given < total_num_entries:
            value = io.get_and_confirm_input(
                'Entry #{}: '.format(num_entries_given + 1))
            value = float(value)
            wfile.write('{}\n'.format(value))
            num_entries_given += 1


def main():
    """Application entry point"""
    print "This program will read or write numbers to or from a given file."
    file_path = io.get_and_confirm_input('Please enter a file name: ')
    read_write = io.binary_choice('Mode ((r)ead/(w)rite): ', 'r', 'w')
    if read_write == 'r':
        read_file(file_path)
    else:
        write_file(file_path)


if __name__ == '__main__':
    main()
