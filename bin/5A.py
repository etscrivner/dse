# -*- coding: utf-8 -*-
"""
    5A
    ~~
    Exercise 5A, numerical integration using Simpson's Rule.

    Application: The application entry-point object.
"""
from lib import integration
from lib import statistics


class Application(object):
    """The application entry-point object"""

    def __init__(self):
        """Initialize."""
        self.integrator = integration.Integrator(20, 0.0001)

    def execute(self):
        print 'Exercise 5A'
        print '==========='
        print 'This program approximates the integral of the normal'
        print "distribution probability density function using Simpson's rule"
        print 'and displays the approximated result.'
        print
        print 'REPORT'
        print '======'
        print '∫(-∞, 2.5] = {}'.format(
            self.integrate_normal_minus_infinity_to(2.5))
        print '∫(-∞, 0.2] = {}'.format(
            self.integrate_normal_minus_infinity_to(0.2))
        print '∫(-∞, -1.1] = {}'.format(
            self.integrate_normal_minus_infinity_to(-1.1))

    def integrate_normal_minus_infinity_to(self, upper_limit):
        """Integrate the normal distribution from -infinity to upper_limit.

        Arguments:
            upper_limit(float): The upper limit of integration.

        Returns:
            float: The integral result
        """
        return self.integrator.integrate_minus_infinity_to(
            statistics.normal_distribution, upper_limit)


if __name__ == '__main__':
    Application().execute()
