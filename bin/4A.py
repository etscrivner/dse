# -*- coding: utf-8 -*-
"""
    4A
    ~~
    The PSP Exercise 4A program - calculate and display linear regression
    parameters.

    Application: The application entry point for exercise 4A.
"""
import argparse
import sys

from lib import io
from lib import statistics


class Application(object):
    """Application entry point"""

    def execute(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'CSVFILE', help='path to csv file with historical data.')
        args = parser.parse_args()
        file_path = args.CSVFILE
        csv_data = io.read_csv_file(file_path)

        if not csv_data:
            print 'ERROR: No data'
            sys.exit(1)

        columns = csv_data[0].keys()
        x_column = io.choose_from_list('X Column:', columns)
        y_column = io.choose_from_list('Y Column:', columns)
        x_data = [float(each[x_column]) for each in csv_data]
        y_data = [float(each[y_column]) for each in csv_data]
        #x_data, y_data = statistics.remove_outliers(x_data, y_data)
        print

        print 'X DATA: {}'.format(x_data)
        print 'Y DATA: {}'.format(y_data)
        print

        beta_0 = statistics.beta_0(x_data, y_data)        
        print u'\u03B20: {}'.format(beta_0)
        warnings = statistics.beta_0_warnings(beta_0)
        if warnings:
            print 'WARNINGS:'
            print '\n'.join(warnings)
        print

        beta_1 = statistics.beta_1(x_data, y_data)
        print u'\u03B21: {}'.format(beta_1)
        warnings = statistics.beta_1_warnings(beta_1)
        if warnings:
            print 'WARNINGS:'
            print '\n'.join(warnings)
        print


if __name__ == '__main__':
    Application().execute()
