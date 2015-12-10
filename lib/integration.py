# -*- coding: utf-8 -*-
"""
    lib.math
    ~~~~~~~~
    Math-related modules and classes.n

    Integrator: Interface that uses Simpson's Rule to numerically integrate a
        function.
    is_even(): Indicates whether or not the given integer value is even.
"""


def is_even(x):
    """Indicates whether or not the given value is even.

    Arguments:
        x(int): An integer value

    Returns:
        bool: True if the value is even, False otherwise.
    """
    return (x % 2 == 0)


class Integrator(object):
    """Interface that uses Simpson's Rule to numerically integrate a function.
    """

    def __init__(self, number_of_segments, acceptable_error):
        """Initialize the integrator with tolerance values.

        Arguments:
            number_of_segments(int): Even number indicating the number of
                segments to initially divide ranges into.
            acceptable_error(float): The acceptable degree of error in the
                result.
        """
        if not is_even(number_of_segments):
            raise ValueError(
                "Simpson's rule requires an even number of segments")
        self.number_of_segments = number_of_segments
        self.acceptable_error = acceptable_error

    def integrate(self, func, lower_limit, upper_limit):
        """Integrate the given function from lower limit to higher limit.

        Arguments:
            func(callable): The function to be integrated
            lower_limit(float): The lower limit for the integration.
            upper_limit(float): The upper limit for the integration.

        Returns:
            float: The approximation to the integral.
        """
        previous_result = 0
        num_segments = self.number_of_segments
        while True:
            segment_width = (upper_limit - lower_limit) / num_segments
            result = func(lower_limit) + func(upper_limit)
            for point in range(1, (num_segments / 2)):
                result += 2 * func(lower_limit + (2 * point * segment_width))
            for point in range(1, (num_segments / 2) + 1):
                result += 4 * func(
                    lower_limit + ((2 * point - 1) * segment_width))
            result *= (segment_width / 3)
            if abs(result - previous_result) < self.acceptable_error:
                return result
            previous_result = result
            num_segments = 2 * num_segments

    def integrate_minus_infinity_to(self, func, upper_limit):
        """Integrate the given function from negative infinity to the
        given upper limit.

        Arguments:
            func(callable): The function to be integrated
            upper_limit(float): THe upper limit for the integration.

        Returns:
            float: The approximation to the integral.
        """
        result = self.integrate(func, 0, abs(upper_limit))
        if upper_limit < 0:
            return 0.5 - result
        return 0.5 + result
