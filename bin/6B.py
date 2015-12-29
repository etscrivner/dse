# -*- coding: utf-8 -*-
"""
    6B
    ~~
    PSP Exercise 6A - Write a program that uses historical data to calculate
    linear regression parameters.


    Application: The application entry point object
"""
import argparse

from lib import probe


class Application(object):
    """The application object"""

    def execute(self):
        """The application entry point."""
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'CSVFILE', help='path to csv file with historical data.')
        parser.add_argument(
            'ESTVAL', help='proxy estimate value')
        args = parser.parse_args()

        historical_data = probe.HistoricalData.from_csv_file(args.CSVFILE)
        proxy_estimate = float(args.ESTVAL)

        estimation = probe.ProbeEstimation(historical_data)
        size_method = estimation.get_size_method(proxy_estimate)
        time_method = estimation.get_time_method(proxy_estimate)

        print 'REPORT'
        print '======'
        print

        regression = size_method.get_regression()
        print 'Size'
        print '----'
        print
        print 'Method: '  + size_method.get_name()
        print u'\u03B20: {}'.format(regression.beta0)
        print u'\u03B21: {}'.format(regression.beta1)
        print 'Projection: {}'.format(regression.estimate(proxy_estimate))
        print

        regression = time_method.get_regression()
        print 'Time'
        print '----'
        print
        print 'Method: '  + time_method.get_name()
        print u'\u03B20: {}'.format(regression.beta0)
        print u'\u03B21: {}'.format(regression.beta1)
        print 'Projection: {}'.format(regression.estimate(proxy_estimate))


if __name__ == '__main__':
    Application().execute()
