# -*- coding: utf-8 -*-
"""
    2B
    ~~
    The PSP Exercise 2B Program. Modify program 1B to allow for addition and
    modification of values from a file.


    prompt_for_output_file(): Prompt a user for an optional new file name.
    read_file(): Read and display the contents of the given file.
    write_file(): Get a series of numbers from user and write to given file.
    add_file(): Go through file line-by-line and prompt user for new values to
        add to the file.
    modify_file(): Go through file line-by-line and prompt user for modified
        value or to delete value from file.
    main(): Application entry point
"""
import os

from lib import io
from lib.io import get_and_confirm_input


def prompt_for_output_file(original_file_name):
    """Prompt for the file to output data into

    Arguments:
        original_file_name(str): The original file name.

    Returns:
        str: The new file name if a new file is entered, otherwise the original
             file name.
    """
    print 'Origin file: {}'.format(original_file_name)
    choice = io.binary_choice('Output file (s)ame/(n)ew file? ', 's', 'n')
    if choice == 'n':
        new_file_name = io.get_and_confirm_input('New file name: ')
        return new_file_name
    return original_file_name


def read_file(file_path):
    """Reads numerical values from a file a displays them to a user.

    Arguments:
        file_path(basestring): The path to the file
    """
    numbers = io.read_numbers_from_file(file_path)
    for each in numbers:
        print each


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


def add_file(file_path):
    """Go through file line-by-line and ask for additions after given line.

    Arguments:
        file_path(str): The path to the file
    """
    numbers = io.read_numbers_from_file(file_path)
    output_file = prompt_for_output_file(file_path)

    # Go through each number one at a time
    results = []
    for idx, each in enumerate(numbers):
        # Display the results up to this point
        if results:
            print 'Numbers So Far:'
            for num in results:
                print num
        print 'Next number:'
        print each

        # Get the choice
        choice = io.choose_from_list('What would you like to do:', ['Keep', 'Add Number After', 'Keep Rest'])
        choice = choice.lower()
        if choice == 'keep':
            results.append(each)
        elif choice == 'add number after':
            # Get the new number and add it to the list
            results.append(each)
            number = get_and_confirm_input("New number: ")
            results.append(float(number))
        elif choice == 'keep rest':
            # Add remaining numbers to results and exit loop
            results += numbers[idx:]
            break

    # Write the updated numbers to the output file
    io.write_numbers_to_file(output_file, results)
    print 'Results written to', output_file


def modify_file(file_path):
    """Modifies the values in the given file.

    Arguments:
        file_path(str): A file to be modified
    """
    numbers = io.read_numbers_from_file(file_path)
    output_file = prompt_for_output_file(file_path)

    # Go through each number one at a time
    results = []

    for idx, each in enumerate(numbers):
        # Display the results up to this point
        if results:
            print 'Numbers So Far:'
            for num in results:
                print num
        # Otherwise display next number
        print 'Next Number:'
        print each
        # Let the user choose what to do with the number
        choice = io.choose_from_list('What would you like to do', ['Keep', 'Modify', 'Delete', 'Keep Rest'])
        choice = choice.lower()
        if choice == 'keep':
            results.append(each)
        elif choice == 'modify':
            number = get_and_confirm_input("New value: ")
            results.append(float(number))
        elif choice == 'keep rest':
            results += numbers[idx:]
            break
        elif choice == 'delete':
            # Do nothing
            pass

    # Write the updated numbers to the output file
    io.write_numbers_to_file(output_file, results)
    print 'Results written to ', output_file


def main():
    """Application entry point"""
    print "This program will read or write numbers to or from a given file."
    file_path = io.get_and_confirm_input('Please enter a file name: ')
    print 'Read - Read and display numbers in a file'
    print 'Write - Input numbers to write to a file'
    print 'Add - Go through file line-by-line and add new numbers'
    print 'Modify - Go through file line by line and modify numbers'
    mode = io.choose_from_list('Choose a mode', ['Read', 'Write', 'Add', 'Modify'])
    mode = mode.lower()
    if mode == 'read':
        read_file(file_path)
    elif mode == 'write':
        write_file(file_path)
    elif mode == 'add':
        add_file(file_path)
    elif mode == 'modify':
        modify_file(file_path)
    else:
        raise RuntimeError('Invalid option {}'.format(mode))


if __name__ == '__main__':
    main()
