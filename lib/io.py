# -*- coding: utf-8 -*-
"""
    lib.io
    ~~~~~~
    General methods useful for I/O.


"""
import csv


def yes_no_prompt(prompt):
    """Displays a prompt and asks for yes or no input.

    Arguments:
        prompt(basestring): The prompt to be displayed.

    Returns:
        bool: True if yes, false otherwise.
    """
    yes_no = raw_input('{} (y/n) '.format(prompt))
    if yes_no.lower() == 'y':
        return True
    return False


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
        idx = raw_input('Enter a number: ')
        is_correct_value = yes_no_prompt(
            'You entered {}. Is this correct?'.format(idx))
        if is_correct_value:
            return values[(int(idx) - 1)]
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
