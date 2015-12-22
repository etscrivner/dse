# -*- coding: utf-8 -*-
"""
    6A
    ~~
    The PSP Exercise 6A program - calculate and display the 70% and 90%
    prediction intervals for given data.

    Application: The application entry point for exercise 6A.
"""
import argparse
import sys

from lib import io
from lib import statistics
from lib import integration


class Application(object):
    """Application entry point"""

    def execute(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'CSVFILE', help='path to csv file with historical data.')
        parser.add_argument(
            'ESTVAL', help='an estimated value')
        args = parser.parse_args()
        file_path = args.CSVFILE
        estimated_value = float(args.ESTVAL)
        csv_data = io.read_csv_file(file_path)

        if not csv_data:
            print 'ERROR: No data'
            sys.exit(1)

        columns = csv_data[0].keys()
        x_column = io.choose_from_list('X Column:', columns)
        y_column = io.choose_from_list('Y Column:', columns)
        x_data = [float(each[x_column]) for each in csv_data]
        y_data = [float(each[y_column]) for each in csv_data]
        print

        print 'X DATA: {}'.format(x_data)
        print 'Y DATA: {}'.format(y_data)
        print

        beta_0 = statistics.beta_0(x_data, y_data)
        print u'\u03B20: {}'.format(beta_0)

        beta_1 = statistics.beta_1(x_data, y_data)
        print u'\u03B21: {}'.format(beta_1)

        integ = integration.Integrator(20, 0.000001)
        tdist = statistics.make_t_distribution(len(x_data) - 2)
        itdist = lambda x: integ.integrate_minus_infinity_to(tdist, x)

        std_dev = (
            statistics.standard_deviation_around_regression(x_data, y_data)
        )
        print "StdDev: ", std_dev

        projection = beta_0 + beta_1 * estimated_value
        print 'Projection: ', projection

        print 't(70 percent): ', integration.approximate_inverse(itdist, 0.85)
        print 't(90 percent): ', integration.approximate_inverse(itdist, 0.95)

        range70 = statistics.prediction_range(
            estimated_value, 0.85, x_data, y_data
        )
        range90 = statistics.prediction_range(
            estimated_value, 0.95, x_data, y_data
        )
        print 'Range(70 percent) =', projection + range70, \
            'UPI =', projection - range70, 'LPI =', range70
        print 'Range(90 percent) =', projection + range90, \
            'UPI =', projection - range90, 'LPI =', range90

if __name__ == '__main__':
    Application().execute()
