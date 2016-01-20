# -*- coding: utf-8 -*-
"""
    7A
    ~~
    Significance and correlation between two sets of data.

    Application: The application entry point object.
"""
import argparse
import sys

from lib import io
from lib import statistics


class Application(object):
    def execute(self):
        """Run the program"""
        parser = argparse.ArgumentParser()
        parser.add_argument('CSVFILE', help='path to csv file with data.')
        args = parser.parse_args()
        csv_data = io.read_csv_file(args.CSVFILE)

        if not csv_data:
            print 'ERROR: Invalid csv data file.'
            sys.exit(1)

        columns = csv_data[0].keys()
        x_column = io.choose_from_list('X Column:', columns)
        y_column = io.choose_from_list('Y Column:', columns)
        x_data = [float(each[x_column]) for each in csv_data]
        y_data = [float(each[y_column]) for each in csv_data]

        print 'R:', statistics.correlation(x_data, y_data)
        print 'T:', statistics.t_value(x_data, y_data)
        print 'Significance:', statistics.significance(x_data, y_data)


if __name__ == '__main__':
    Application().execute()
