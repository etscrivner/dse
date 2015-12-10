# -*- coding: utf-8 -*-
"""
    1A
    ~~
    The PSP Exercise 1A executable program.

    This program takes a CSV file and computes the mean and standard deviation
    for a single row from that CSV file.
"""
from lib import io
from lib import linked_list
from lib import statistics


def main():
    """The application entry point"""
    print 'EXERCISE 1A'
    print '==========='
    print 'This program takes a CSV file, asks you to select a row from that'
    print 'file, and then computes the mean and standard deviation of the'
    print 'values in that row.'
    print
    file_path = io.get_and_confirm_input('Enter csv file with values: ')
    data = io.read_csv_file(file_path)

    if not data:
        raise RuntimeError('No data found in file {}'.format(file_path))

    column = io.choose_from_list(
        'Which column would you like to use:', data[0].keys())

    if column not in data[0]:
        raise RuntimeError('Invalid column {}'.format(column))

    values = linked_list.LinkedList()
    for each in data:
        values.insert(each[column])

    for each in values:
        print each

    print 'Mean: ', statistics.mean(values)
    print 'Std Dev: ', statistics.standard_deviation(values)


if __name__ == '__main__':
    main()
