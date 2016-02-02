# -*- coding: utf-8 -*-
"""
    7B
    ~~
    PSP Exercise 7B - Write a program that uses historical data to calculate
    linear regression parameters with prediction intervals.

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
        projected_value = regression.estimate(proxy_estimate)
        print 'Size'
        print '----'
        print
        print 'Method:', size_method.get_name()
        print u'\u03B20:', regression.beta0
        print u'\u03B21:', regression.beta1
        print 'Projection:', projected_value
        print 'R^2:', size_method.get_correlation()
        print 'Significance:', size_method.get_significance()
        print 'Range:', size_method.get_interval_range(projected_value)
        print 'UPI:', size_method.get_upi(proxy_estimate)
        print 'LPI:', size_method.get_lpi(proxy_estimate)
        print 'Percent:', size_method.get_interval_percent()
        print

        regression = time_method.get_regression()
        projected_value = regression.estimate(proxy_estimate)
        print 'Time'
        print '----'
        print
        print 'Method:', time_method.get_name()
        print u'\u03B20:', regression.beta0
        print u'\u03B21:', regression.beta1
        print 'Projection:', regression.estimate(proxy_estimate)
        print 'R^2:', time_method.get_correlation()
        print 'Significance:', time_method.get_significance()
        print 'Range:', time_method.get_interval_range(projected_value)
        print 'UPI:', time_method.get_upi(proxy_estimate)
        print 'LPI:', time_method.get_lpi(proxy_estimate)
        print 'Percent:', time_method.get_interval_percent()

if __name__ == '__main__':
    Application().execute()
