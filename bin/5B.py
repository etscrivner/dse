# -*- coding: utf-8 -*-
"""
    5B
    ~~
    PSP Exercise 5B, in which we add handling arrays of values to the B-series
    programs, and I also venture a rewrite of the program so far.

    print_results_so_far(): Print summary of data entered so far.
    prompt_for_output_file(): Prompt a user for an optional new file name.
    ReadFile: Use case for reading data from a file.
    WriteFile: Use case for writing data to a file.
    AddToFile: Use case for going through file line-by-line and adding data.
    ModifyFile: Use case for going through file line-by-line and modifying
        data.
    Application: The application entry point
"""
import os
import sys

from lib import io


def print_results_so_far(results):
    """Display the results so far to the user.

    Arguments:
        results(list): A list of input results so far
    """
    print 'Data so far:'
    for index, each in enumerate(results):
        print '{}: {}'.format(index, each)


def prompt_for_output_file(original_file_name):
    """Prompt for the file to output data into

    Arguments:
        original_file_name(str): The original file name.

    Returns:
        str: The new file name if a new file is entered, otherwise the original
             file name.
    """
    print 'Original file: {}'.format(original_file_name)
    choice = io.binary_choice('Output file (s)ame/(n)ew file? ', 's', 'n')
    if choice == 'n':
        new_file_name = io.prompt_valid_file_name('New file name: ')
        return new_file_name
    return original_file_name


class ReadFile(object):
    """Mode where a user is prompted for a file and the values from that file
    are read and displayed."""

    def execute(self, maximum_list_length):
        """Prompt user for a file and display the values from that file.

        Arguments:
            maximum_list_length(int): The maximum allowed list length (Unused)
        """
        input_file = io.prompt_existant_file_name(
            'Please enter the file to read: ')
        values = io.read_lists_from_file(input_file)
        for each in values:
            print each


class WriteFile(object):
    """Mode where a user is prompted for a file to write and then asked to
    input values to be written to that file."""

    def execute(self, maximum_list_length):
        """Prompt user for a file and have them enter values to write into it.

        Arguments:
            maximum_list_length(int): The maximum allowed list length.
        """
        output_file = io.prompt_valid_file_name(
            'Please enter the file to write: ')

        if os.path.isfile(output_file):
            self.prompt_overwrite_or_change(output_file, maximum_list_length)

        if not os.path.exists(os.path.dirname(output_file)):
            self.directory_does_not_exist(output_file, maximum_list_length)

        total_num_entries = int(io.get_and_confirm_input(
            'How many numbers will you enter: '))
        num_entries_given = 0
        entries = []

        while num_entries_given < total_num_entries:
            value = io.get_and_confirm_list(
                'Entry {}: '.format(num_entries_given + 1),
                max_list_length=maximum_list_length)
            entries.append(value)
            num_entries_given += 1

        io.write_lists_to_file(output_file, entries)
        print 'Results written to {}'.format(output_file)

    def directory_does_not_exist(self, file_path, maximum_list_length):
        """Indicate that the directory does not exist and given user the option
        to try again.

        Arguments:
            file_path(basestring): The path to the file.
            maximum_list_length(int): The maximum allowed list length.
        """
        print 'error: Directory for file {} does not exist'.format(
            file_path)
        io.prompt_try_again_or_abort()
        self.execute(maximum_list_length)
        sys.exit()

    def prompt_overwrite_or_change(self, file_path, maximum_list_length):
        """Prompt user to either opt to overwrite the given file or enter a
        new file name.

        Arguments:
            file_path(basestring): The path to the file
            maximum_list_length(int): The maximum allowed list length.
        """
        should_overwrite = io.yes_no_prompt(
            'File {} exists. Overwrite?'.format(file_path))
        if not should_overwrite:
            enter_different_file = io.yes_no_prompt(
                'Would you like to enter a different file name?')
            if enter_different_file:
                self.execute(maximum_list_length)
                sys.exit()
            sys.exit('Aborting. Not overwriting existing file.')


class AddToFile(object):
    """Go through file line-by-line and add data above or below lines."""

    def execute(self, maximum_list_length):
        """Prompt user for input file and output file and go through input
        file line-by-line adding data.

        Arguments:
            maximum_list_length(int): The maximum allowed list length.
        """
        input_file = io.prompt_existant_file_name(
            'Please enter file to read from: ')
        data = io.read_lists_from_file(input_file)
        output_file = prompt_for_output_file(input_file)

        updated_results = []
        for index, each in enumerate(data):
            if updated_results:
                print_results_so_far(updated_results)

            print 'Next Item:'
            print each

            choice = io.choose_from_list(
                'What would you like to do',
                ['Keep', 'Add Item Before', 'Add Item After', 'Keep Rest'])

            if choice == 'Keep':
                updated_results.append(each)
            elif choice == 'Add Item Before':
                new_list = io.get_and_confirm_list(
                    'New item: ', max_list_length=maximum_list_length)
                updated_results.append(new_list)
                updated_results.append(each)
            elif choice == 'Add Item After':
                new_list = io.get_and_confirm_list(
                    'New item: ', max_list_length=maximum_list_length)
                updated_results.append(each)
                updated_results.append(new_list)
            else:
                updated_results += data[index:]

        io.write_lists_to_file(output_file, updated_results)
        print 'Results written to {}'.format(output_file)


class ModifyFile(object):
    """Go through file line-by-line and modify lines"""

    def execute(self, maximum_list_length):
        """Prompt user for input and output files then go through input file
        line-by-line, updated values, and write results to output file.

        Arguments:
            maximum_list_length(int): The maximum allowed list length
        """
        input_file = io.prompt_existant_file_name(
            'Please enter file to modify: ')
        output_file = prompt_for_output_file(input_file)
        data = io.read_lists_from_file(input_file)

        updated_results = []
        for index, each in enumerate(data):
            if updated_results:
                print_results_so_far(updated_results)

            print 'Next Item:'
            print each

            choice = io.choose_from_list(
                'What would you like to do',
                ['Keep', 'Change', 'Delete', 'Keep Rest'])
            if choice == 'Keep':
                updated_results.append(each)
            elif choice == 'Change':
                new_item = io.get_and_confirm_list(
                    'New Item: ', max_list_length=maximum_list_length)
                updated_results.append(new_item)
            elif choice == 'Delete':
                pass
            else:
                updated_results += data[index:]

        io.write_lists_to_file(output_file, updated_results)
        print 'Results written to {}'.format(output_file)


class Application(object):
    """The application entry point object"""

    # The maximum length allowed for input lists
    MAXIMUM_LIST_LENGTH = 1

    def __init__(self):
        self.mode_map = {
            'Read': ReadFile,
            'Write': WriteFile,
            'Add': AddToFile,
            'Modify': ModifyFile
        }

    def execute(self):
        """Ask the user for a mode selection and then execute the object
        corresponder to that mode."""
        print 'This program is used to edit lists of numerical values in text'
        print 'files. It can be used in any of the following modes:'
        print 'Read - Read and display lists of numbers in a file.'
        print 'Write - Input lists of numbers to write to a file.'
        print 'Add - Go through a file line-by-line and add new values.'
        print 'Modify - Go through a file line-by-line and modify values.'

        mode = io.choose_from_list('Choose a mode', self.mode_map.keys())
        mode_class = self.mode_map[mode]
        mode_class().execute(self.MAXIMUM_LIST_LENGTH)


if __name__ == '__main__':
    Application().execute()
