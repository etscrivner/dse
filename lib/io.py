# -*- coding: utf-8 -*-
"""
    lib.io
    ~~~~~~
    General methods useful for I/O.

    binary_choice(): Prompt user for a choice between two options.
    yes_no_prompt(): Ask user a yes-no question and return result.
    prompt_try_again_or_abort(): Prompt a user to try an operation again or
        abort the program.
    get_and_confirm_input(): Prompt a user for input and confirm value is
        correct.
    get_and_confirm_float(): Prompt a user for input, confirm value, and verify
        that it is a valid floating point number.
    choose_from_list(): Ask a user to choose an option from a list of options.
    read_csv_file(): Read the contents of a CSV file into a dictionary.
    write_numbers_to_file(): Write numbers to given file one per line.
    read_numbers_from_file(): Read numbers from file, one per line, and return
        in a list.
    find_files_matching(): Find all files matching pattern in path and its
        subdirectories.
    is_valid_file_name(): Indicates whether or not a file name is valid.
    prompt_valid_file_name(): Asks the user to input a valid file name.
    prompt_existant_file_name(): Asks the user to input a valid file name that
        also corresponds to an existing file.
    read_lists_from_file(): Read and return data from file containing lines
        of lists.
    write_lists_to_file(): Write lists to the given file.
    get_and_confirm_list(): Prompt user for a list of values and return the
        list given.
"""
import csv
import fnmatch
import os
import re
import sys


def binary_choice(prompt, first_choice, second_choice):
    """Displays a prompt asking for one of two possible choices.

    Arguments:
        prompt(basestring): The prompt to be displayed.
        first_choice(basestring): The first possible choice.
        second_choice(basestring): The second possible choice.

    Returns:
        basestring: The choice selected by the user.

    Raises:
        RuntimeError: If the choice given is not one of the two available.
    """
    choice = raw_input(prompt)
    if choice.lower() not in (first_choice, second_choice):
        raise RuntimeError('Value {} is not one of {} or {}'.format(
            choice, first_choice, second_choice
        ))
    return choice


def yes_no_prompt(prompt):
    """Displays a prompt and asks for yes or no input.

    Arguments:
        prompt(basestring): The prompt to be displayed.

    Returns:
        bool: True if yes, false otherwise.
    """
    yes_no = binary_choice('{} (y/n) '.format(prompt), 'y', 'n')
    if yes_no.lower() == 'y':
        return True
    return False


def prompt_try_again_or_abort():
    """Prompt the user to try an operation again or abort the program.

    Raises:
        RuntimeError: If the user decides to abort the program
    """
    choice = binary_choice("(t)ry again or (a)bort? ", 't', 'a')
    if choice == 'a':
        sys.exit("Aborting program")


def get_and_confirm_input(prompt, max_attempts=5):
    """Get a value from standard input and confirm correctness.

    Arguments:
        prompt(basestring): The prompt to be used
        max_attempts(int): The maximum number of confirmation attempts.

    Returns:
        basestring: The input given by the user

    Raises:
        RuntimeError: If the maximum number of attempts is exceeded.
    """
    num_attempts = 0
    while num_attempts < max_attempts:
        value = raw_input(prompt)
        is_correct_value = yes_no_prompt(
            'You entered {}. Is this correct?'.format(value))
        if is_correct_value:
            return value
        num_attempts += 1
    raise RuntimeError('Maximum retries exceeded')


def get_and_confirm_float(prompt, max_attempts=5):
    """Get a floating point value from standard input and confirm correctness.

    Arguments:
        prompt(basestring): The prompt to be used
        max_attempts(int): The maximum number of confirmation attempts.

    Returns:
        float: The input given by the user

    Raises:
        RuntimeError: If the maximum number of attempts is exceeded, or the
            user opts to abort after invalid input.
    """
    num_attempts = 0
    while num_attempts < max_attempts:
        value = raw_input(prompt)
        try:
            value = float(value)
            is_correct_value = yes_no_prompt(
                'You entered {}. Is this correct?'.format(value))
            if is_correct_value:
                return value
        except ValueError:
            print "ERROR: {} is not a valid real number.".format(value)
            prompt_try_again_or_abort()
        num_attempts += 1
    raise RuntimeError('Maximum retries exceeded')


def choose_from_list(prompt, values, max_attempts=5):
    """Displays a prompt of all the values in the list and asks the user to
    pick the number associated with one item.

    Example:
    >>> choose_from_list('Which is better', ['Dog', 'Cat'])
    Which is better:
    1) Dog
    2) Cat
    Enter a number: 1
    You entered 1. Is this correct? (y/n) y
    'Dog'

    Arguments:
        prompt(basestring): The prompt to be used before the list.
        values(iterable): An iterable containing values to list.
        max_attempts(int): The maximum number of confirmation attempts.

    Returns:
        mixed: A single value from the list selected by the user.

    Raises:
        RuntimeError: If the maximum number of attempts is exceeded.
    """
    num_attempts = 0
    while num_attempts < max_attempts:
        print prompt
        for num, each in enumerate(values):
            print '{}) {}'.format(num + 1, each)

        item_num = raw_input('Enter a number: ')
        is_correct_value = yes_no_prompt(
            'You entered {}. Is this correct?'.format(item_num))

        try:
            item_num = int(item_num)
        except ValueError:
            print 'ERROR: {} is an invalid number.'.format(item_num)
            prompt_try_again_or_abort()
            is_correct_value = False

        if is_correct_value:
            if item_num > len(values):
                print 'ERROR: {} is an invalid option.'.format(item_num)
                prompt_try_again_or_abort()
            else:
                return values[(item_num - 1)]

        num_attempts += 1
    raise RuntimeError('Maximum retries exceeded')


def read_csv_file(file_path):
    """Reads a comma-separated value (CSV) file and returns data.

    Arguments:
        file_path(basestring): The path to the CSV file.

    Returns:
        list: The CSV data as a list of dicts
    """
    with open(file_path) as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)


def write_numbers_to_file(file_name, values):
    """Writes the given numbers to a file.

    Arguments:
        file_name(str): The path to the file to write.
        values(list): A list of values to be written.
    """
    with open(file_name, 'w') as out_file:
        for each in values:
            out_file.write('{}\n'.format(each))


def read_numbers_from_file(file_name):
    """Reads a list of numbers from a file.

    Arguments:
        file_name(str): The path to the file to read.

    Returns:
        list: The numbers from the file as float values.
    """
    with open(file_name, 'r') as in_file:
        results = []
        for line in in_file.readlines():
            stripped_line = line.strip()
            if stripped_line:
                results.append(float(stripped_line))
        return results


def find_files_matching(path, pattern):
    """Find all files under the given path matching the given pattern.

    Arguments:
        path(basestring): A file system path
        pattern(basestring): The file name pattern to match

    Returns:
        list: The path of all the matching files found
    """
    matches = []
    for root, _, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches


def is_valid_file_name(file_name):
    """Indicates whether or not the given file name is valid.

    Arguments:
        file_name(basestring): A file name

    Returns:
        bool: True if the file name is valid, False otherwise.
    """
    regex = re.compile(
        r'^(\{pathsep}?[A-Za-z0-9\-\_\.]+\{pathsep}?)+$'.format(
            pathsep=os.path.sep))
    return regex.match(file_name)


def prompt_valid_file_name(prompt, max_attempts=5):
    """Prompt the user to enter a valid file name. Fail after the given number
    of attempts.

    Arguments:
        prompt(basestring): The prompt to display to the user
        max_attempts(int): The maximum number of times the user can attempt to
            provide a valid file name. Optional, default is 5.

    Returns:
        basestring: The file name provided by the user

    Raises:
        RuntimeError: If the user exceeds max_attempts attempts to provide
            valid input.
    """
    while max_attempts > 0:
        file_name = raw_input(prompt)

        if is_valid_file_name(file_name):
            return file_name

        print "ERROR: Invalid file name {}".format(file_name)
        prompt_try_again_or_abort()
        max_attempts -= 1
    raise RuntimeError(
        'ERROR: More than {} attempts made to entire valid file name'.format(
            max_attempts))


def prompt_existant_file_name(prompt, max_attempts=5):
    """Prompt the user to enter a valid file name. Fail after the given number
    of attempts.

    Arguments:
        prompt(basestring): The prompt to display to the user
        max_attempts(int): The maximum number of times the user can attempt to
            provide a valid file name. Optional, default is 5.

    Returns:
        basestring: The file name provided by the user

    Raises:
        RuntimeError: If the user exceeds max_attempts attempts to provide
            valid input.
    """
    while max_attempts > 0:
        file_name = raw_input(prompt)

        if is_valid_file_name(file_name):
            if os.path.exists(file_name):
                return file_name

            print 'ERROR: File {} does not exist'.format(file_name)
            prompt_try_again_or_abort()
            max_attempts
        else:
            print "ERROR: Invalid file name {}".format(file_name)
            prompt_try_again_or_abort()
            max_attempts -= 1
    raise RuntimeError(
        'ERROR: More than {} attempts made to entire valid file name'.format(
            max_attempts))


def read_lists_from_file(file_path):
    """Read a file containing a list of real numbers per line and returns all
    the lists in order.

    Arguments:
        file_path(basestring): The path to the file to be read.

    Returns:
        list: A list of all of the lists found
    """
    with open(file_path, 'r') as list_file:
        results = []
        for each in list_file.readlines():
            results.append(eval(each))
        return results


def write_lists_to_file(file_path, data):
    """Write the given list of lists to the given file.

    Arguments:
        file_path(basestring): The path to the file to write.
        data(list): A list of lists
    """
    with open(file_path, 'w') as list_file:
        for each in data:
            list_file.write('{!r}\n'.format(each))


def get_and_confirm_list(prompt, max_list_length, max_attempts=10):
    """Prompt user to enter a comma-separated list of values. Consider invalid
    any list that exceeds max_list_length. If the input is invalid than allow
    max_attempts chances to correct it.

    Arguments:
        prompt(basestring): The prompt to the user.
        max_list_length(int): Maximum allowed list length.
        max_attempts(int): Maximum number of attempts to input valid data.

    Raises:
        RuntimeError: If user exceeds max_attempts tries to input valid data.
    """
    while max_attempts > 0:
        print 'A list is a comma-separated series of values (Ex. 1.23, 3.45)'
        raw_list = get_and_confirm_input(prompt)
        parts = re.split(r',\s+', raw_list)

        if len(parts) > max_list_length:
            print 'error: List {} has more than {} items'.format(
                raw_list, max_list_length)
            prompt_try_again_or_abort()
            max_attempts -= 1
            continue

        cleaned_parts = []
        for each in parts:
            try:
                cleaned_parts.append(float(each))
            except ValueError:
                print 'error: {} is an invalid real number'.format(each)
                prompt_try_again_or_abort()
                max_attempts -= 1
                continue

        return cleaned_parts
