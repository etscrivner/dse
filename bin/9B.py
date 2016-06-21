# -*- coding: utf-8 -*-
"""
    9B
    ~~
    PSP Exercise 9B, perform the generalized chi-squared test on given data.

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
        print 'PSP Exercise 9B'
        print 'This program performs the general chi-squared test on data '
        print 'given.'
        print
        file_path = self.get_file_name()
        data = io.read_csv_file(file_path)
        test_data = self.get_test_column(data)
        q_val, p_val = chi_squared.GeneralChiSquaredTest().execute(test_data)
        print 'Q: ', q_val
        print 'P: ', p_val
        print '1-P: ', 1.0 - p_val

    def get_file_name(self):
        """Display a prompt to the user requesting data.

        Returns:
            str: The file name given by the user.
        """
        try:
            return io.prompt_valid_file_name('Enter test data file:')
        except RuntimeError as re:
            self.display_error('Invalid or missing test file provided.')
            raise re

    def get_test_column(self, data):
        """Prompt the user to select the column from the given data to test.

        Arguments:
            data(dict): An association column name => data

        Returns:
            list: The data to be tested.

        Raises:
            ValueError: If selected column does not contain only numeric data.
        """
        try:
            column_name = io.choose_from_list(
                'Choose test column', data[0].keys())
        except RuntimeError as re:
            self.display_error('Invalid column selection')
            raise re

        try:
            return [float(each[column_name]) for each in data]
        except ValueError as ve:
            self.display_error('Non-numeric values found in selected column.')
            raise ve

    def display_error(self, message):
        """Display the given error message is a standard format.

        Arguments:
            message(str): The message to be displayed.
        """
        print 'error: 9B:', message


if __name__ == '__main__':
    Application().execute()
