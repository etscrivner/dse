# -*- coding: utf-8 -*-
"""
    lib.integration
    ~~~~~~~~~~~~~~~
    Module for handling numerical integration.

    Integrator: Interface that uses Simpson's Rule to numerically integrate a
        function.
    is_even(): Indicates whether or not the given integer value is even.
    derivative(): Return a function that returns derivative of given function.
    newton_raphson(): Uses the Newton-Raphson method to compute fixed point
        of the given function.
    approximate_inverse(): Approximate the inverse of a function at the given
        point.
"""


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


def is_even(x):
    """Indicates whether or not the given value is even.

    Arguments:
        x(int): An integer value

    Returns:
        bool: True if the value is even, False otherwise.
    """
    return (x % 2 == 0)


def derivative(f, dx=10E-8):
    """Returns a function that will compute the value of the derivative of the
    given function at any point x.

    Arguments:
        f(callable): A function
        dx(float): Very small dx value

    Returns:
        callable: Derivative function
    """
    def df(x):
        return (f(x + dx) - f(x)) / dx
    return df


def newton_raphson(f, guess, tolerance=10E-8):
    """Use the Newton-Raphson method to compute the fixed-point of the given
    function.

    Arguments:
        f(callable): A function that takes a single variable x.
        guess(float): The initial guess
        tolerance(float): The acceptable tolerance for an answer.

    Returns:
        float: The approximate fixed point for the given function.
    """
    df = derivative(f)
    newton = lambda x: (x - (f(x) / df(x)))
    current_guess = guess
    next_guess = newton(guess)
    while abs(next_guess - current_guess) > tolerance:
        current_guess = next_guess
        next_guess = newton(current_guess)
    return next_guess


def approximate_inverse(f, point):
    """Approximate the inverse of the function for the given point.

    Arguments:
        f(callable): A function
        point(float): The point to compute the inverse of

    Returns:
        float: The approximate inverse
    """
    h = lambda x: f(x) - point
    return newton_raphson(h, 0.5)
