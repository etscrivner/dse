# -*- coding: utf-8 -*-
"""
    9A
    ~~
    PSP Exercise 9A, perform the chi-squared test on given data.

    Application: The application entry point
"""
from lib import chi_squared
from lib import io


class Application(object):
    """Request a CSV file from the user containing data to be tested. Then
    perform test and display results"""

    def execute(self):
        """Prompt the user for a CSV file and column selection. Then, perform
        chi-squared test on the data given.
        """
        print 'PSP Exercise 9A'
        print 'This program performs the chi-squared test on data given.'
        print
        file_path = self.get_file_name()
        data = io.read_csv_file(file_path)
        test_data = self.get_test_column(data)
        q_val, p_val = chi_squared.ChiSquaredTest().execute(test_data)
        print 'Q: ', q_val
        print 'P: ', 1.0 - p_val

    def get_file_name(self):
        """Display a prompt to the user requesting data.

        Returns:
            str: The file name given by the user.
        """
        return io.prompt_valid_file_name('Enter test data file:')

    def get_test_column(self, data):
        """Prompt the user to select the column from the given data to test.

        Arguments:
            data(dict): An association column name => data

        Returns:
            list: The data to be tested.

        Raises:
            ValueError: If selected column does not contain only numeric data.
        """
        test_data = io.choose_from_list('Choose test column', data)
        return [float(each) for each in test_data]


if __name__ == '__main__':
    Application().execute()
