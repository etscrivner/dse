# -*- coding: utf-8 -*-
"""
    lib.chi_squared
    ~~~~~~~~~~~~~~~
    Contains interfaces for performing chi-squared test.

    SegmentRange: Representation of a numeric range.
    ChiSquared: Reusable service component for performing chi-squared test.
"""
import math

from lib import statistics
from lib import integration


class SegmentRange(object):
    """Represents a, possibly infinite, range of values on the real-number
    line. The values on either end of the range are inclusive.

    Example:
        >>> SegmentRange(None, 1) # Represents (-infinity, 1]
        >>> SegmentRange(-10, 10) # Represents [-10, 10]
        >>> SegmentRange(10, None) # Represents [10, infinity)
    """

    def __init__(self, lower_bound, upper_bound):
        """Initializes the segment range with the given bounds.

        Arguments:
            lower_bound(float, None): The lower-bound, None = -infinity.
            uppper_bound(float, None): The upper-bound, None = infinity.
        """
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def __hash__(self):
        return hash((self.lower, self.upper))

    def in_range(self, value):
        """Indicates whether or not the given value falls within this range.

        Arguments:
            value(float): The value to be checked.

        Returns:
            bool: True if the value false within this range, False otherwise.
        """
        return ((self.lower_bound is None or value >= self.lower_bound) and
                (self.upper_bound is None or value <= self.upper_bound))


class ChiSquared(object):
    """Reusable service interface that performs the chi-squared test."""

    def execute(self, data):
        """Performs the chi-squared test on the given data returning the
        results.

        Arguments:
            data(list): A list of data points to be evaluated.

        Returns:
            (float, float): A tuple containing the chi-squared sum and the
                p-value indicating the probability that the data is NOT
                normally distributed.

        Raises:
            ValueError: If there is insufficient data.x
        """
        if len(data) < 20:
            raise ValueError('Fewer than 20 items in data set')
        if len(data) % 5 != 0 or len(data) % 2 != 0:
            raise ValueError('Number of items is not an even multiple of 5')

        normalized_data = self.normalized_data(data)
        num_segments = self.get_number_of_segments(len(data))
        chi_squared = self.get_chi_squared(normalized_data)
        p_value = self.get_p_value(chi_squared, num_segments)

        return (chi_squared, p_value)

    def normalized_data(self, data):
        """Return the given data in normalized form.

        Arguments:
            data(list): A list of data points

        Returns:
            list: Same data points, normalized.
        """
        mean = statistics.mean(data)
        stddev = statistics.standard_deviation(data)
        return [(each - mean)/stddev for each in data]

    def get_number_of_segments(self, num_items):
        """This routine returns the number of even-sized segments the normal
        distribution should be divided into. This number corresponds to the
        number of buckets to be constructed.

        Arguments:
            num_items(int): The total number of items in data set.

        Returns:
            float: The total number of segments.
        """
        return 5.0 * math.ceil(math.sqrt(float(num_items)) / 5.0)

    def get_normal_distribution_buckets(self, num_segments):
        """This routine returns a dict with segment ranges corresponding to
        each of the buckets the normal distribution is divided into.

        Arguments:
            num_segments(float): The number of buckets required.

        Returns:
            dict: A hash map with a segment range for each bucket.
        """
        segment_probability = 1.0 / num_segments
        integrator = integration.Integrator(20, 1E-10)
        func = lambda x: integrator.integrate_minus_infinity_to(
            statistics.normal_distribution, x)

        results = {}
        previous_upper_bound = None
        for i in range(1, int(num_segments)):
            next_upper_bound = integration.approximate_inverse(
                func, i * segment_probability)
            results[SegmentRange(previous_upper_bound, next_upper_bound)] = 0
            previous_upper_bound = next_upper_bound

        results[SegmentRange(previous_upper_bound, None)] = 0
        return results

    def get_chi_squared(self, normalized_data, num_segments):
        """Return the chi-squared value for the given data.

        Arguments:
            normalized_data(list): The data in normalized form
            num_segments(int): The number of segments

        Returns:
            float: The chi-squared result
        """
        buckets = self.get_normal_distribution_buckets(num_segments)

        for item in normalized_data:
            for segment_range in buckets.keys():
                if segment_range.in_range(item):
                    buckets[segment_range] += 1

        expected_items_per_bucket = len(normalized_data) / num_segments
        return sum([
            (expected_items_per_bucket - each)**2 / expected_items_per_bucket
            for each in buckets.values()
        ])

    def get_p_value(self, chi_squared, num_segments):
        """Return the probability that the given values are NOT normally
        distributed.

        Arguments:
            chi_squared(float): The chi-squared test result
            num_segments(int): The number of segments

        Returns:
            float: The probability that the data is not normally distributed.
        """
        integrator = integration.Integrator(20, 1E-10)
        func = statistics.make_t_distribution(num_segments - 1)
        return integrator.integrate_minus_infinity_to(func, chi_squared)
