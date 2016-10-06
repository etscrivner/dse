# -*- coding: utf-8 -*-
"""
    lib.chi_squared
    ~~~~~~~~~~~~~~~
    Contains interfaces for performing chi-squared test.

    SegmentRange: Representation of a numeric range.
    ChiSquaredTest: Reusable service component for performing chi-squared test.
    GeneralChiSquaredTest: Reusable service component for performing
        chi-squared test that does not require data be equally divisible into
        segments.
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
        return hash((self.lower_bound, self.upper_bound))

    def __repr__(self):
        lower_repr = self.lower_bound if self.lower_bound else "-∞"
        upper_repr = self.upper_bound if self.upper_bound else "∞"
        return "[{}, {}]".format(lower_repr, upper_repr)

    def in_range(self, value):
        """Indicates whether or not the given value falls within this range.

        Arguments:
            value(float): The value to be checked.

        Returns:
            bool: True if the value false within this range, False otherwise.
        """
        return ((self.lower_bound is None or value >= self.lower_bound) and
                (self.upper_bound is None or value <= self.upper_bound))


class ChiSquaredTest(object):
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
            ValueError: If there is insufficient data.
        """
        if len(data) < 20:
            raise ValueError('Fewer than 20 items in data set')
        if len(data) % 5 != 0 or len(data) % 2 != 0:
            raise ValueError('Number of items is not an even multiple of 5')

        normalized_data = self.normalized_data(data)
        num_segments = self.get_number_of_segments(len(data))
        chi_squared = self.get_chi_squared(normalized_data, num_segments)
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


class GeneralChiSquaredTest(ChiSquaredTest):
    """Reusable service for performing the chi-squared test in a general
    way.

    Usage:
    >>> chi_squared, p_value = GeneralChiSquaredTest().execute(data_list)

    """

    # [Integer] The minimum number of items required to perform the test.
    MINIMUM_ITEMS_REQUIRED = 15

    class TooFewItems(Exception):
        pass

    def execute(self, data):
        """Perform the chi-squared test and return the resulting chi-squared
        and p value.

        Arguments:
            data(list): List of numeric values to be tested for normality.

        Returns:
            (float, float): In order: the Q value and p value.

        Raises:
            TooFewItems: Error if too few items are provided for the test to
                be properly performed.
        """
        if len(data) < self.MINIMUM_ITEMS_REQUIRED:
            raise self.TooFewItems(
                'Expected {} items, found {}'.format(
                    self.MINIMUM_ITEMS_REQUIRED, len(data)))

        normalized_data = self.normalized_data(data)
        num_segments = self.get_number_of_segments(len(data))
        chi_squared = self.get_chi_squared(normalized_data, num_segments)
        p_value = self.get_p_value(chi_squared, num_segments)

        return (chi_squared, p_value)

    def get_chi_squared(self, normalized_data, num_segments):
        """This routine performs the chi-squared test and returns the value
        representing the probability that the data is not normally distributed.

        Arguments:
            normalized_data(list): The normalized data to be tested.
            num_segments(int): The number of segments to divide the normal
                distribution into.

        Returns:
            float: The resulting chi-squared test value.
        """
        assert(num_segments > 0,
               "Expected num_segments > 0, found {}".format(num_segments))

        buckets = self.get_normal_distribution_buckets(
            len(normalized_data), num_segments)
        items_per_bucket = [0] * len(buckets)

        for item in normalized_data:
            for bucket_index, bucket in enumerate(buckets):
                if bucket.in_range(item):
                    items_per_bucket[bucket_index] += 1

        segment_allocation = self.get_segment_allocation(
            len(normalized_data), num_segments)

        return sum([
            (expected - actual)**2 / float(expected)
            for expected, actual in zip(segment_allocation, items_per_bucket)
        ])

    def get_segment_allocation(self, num_items, num_segments):
        """This routine divides the normal distribution into the given number
        of segments. If the given number of data points cannot be divided
        evenly into the number of segments, then unequal segments are created
        beginning from the center and working outward.

        Arguments:
            num_items(int): The number of items to be tested.
            num_segments(int): The number of segments to divide the normal
                distribution into.

        Returns:
            list: A list containing the number of items allocated to each
                segment, where segments are taken to be ordered as the list is.

        Raises:
            AssertionError: If the number of segments is invalid.
        """
        assert(num_segments > 0,
               "number of segments is fewer than 1: {}".format(num_segments))

        # Record the integer number of items in each segment
        items_per_segment = int(num_items / float(num_segments))
        # Create an initial even allocation of items to segments
        results = [items_per_segment] * int(num_segments)

        # If the number of items cannot be evenly divided into the number of
        # segments
        if not self.divides_evenly_into_segments(num_items, num_segments):
            # Compute the number of extra items after equal allocation
            num_extra_items = (
                num_items - int(items_per_segment * num_segments)
            )
            # Allocate the extra items starting from the center and working out
            offset = 0
            center = (num_segments + 1) / 2.0
            for i in range(num_extra_items):
                # Verify the loop precondition
                assert(int(math.floor(center + offset)) < num_segments,
                       "offset index {} is out of range {}".format(
                           int(math.floor(center + offset)), num_segments))

                if offset < 0:
                    results[int(math.floor(center + offset))] += 1
                    offset = -offset
                else:
                    results[int(math.floor(center + offset))] += 1
                    offset = -(offset + 1)

        return results

    def divides_evenly_into_segments(self, num_items, num_segments):
        """This predicate indicates whether or not the given number of items
        can be divided evenly into the given number of segments.

        Arguments:
            num_items(int): The number of items to be tested.
            num_segments(int): The number of segments to divide the normal
                distribution into.

        Returns:
            bool: True if the items can be divided evenly, False otherwise.
        """
        ratio = num_items / float(num_segments)
        return int(ratio) == ratio

    def get_normal_distribution_buckets(self, num_items, num_segments):
        """This routine divides the normal distribution into the given number
        of segments. It then creates a segment range for each segment based on
        the number of items expected to fall within it. It returns a list of
        segment ranges.

        Arguments:
            num_items(int): The number of items to be tested.
            num_segments(int): The number of segments to divide the normal
                distribution into.

        Returns:
            list: A list of SegmentRange objects for each segment.
        """
        assert(num_segments > 0,
               "number of segments is less than 1: {}".format(num_segments))

        integrator = integration.Integrator(20, 1E-10)
        func = lambda x: integrator.integrate_minus_infinity_to(
            statistics.normal_distribution, x)

        results = []
        cumulative_probability = 0
        previous_upper_bound = None
        segment_allocation = self.get_segment_allocation(
            num_items, num_segments)

        for items_in_segment in segment_allocation[:-1]:
            cumulative_probability += items_in_segment / float(num_items)
            upper_bound = integration.approximate_inverse(
                func, cumulative_probability)
            results.append(SegmentRange(previous_upper_bound, upper_bound))
            previous_upper_bound = upper_bound

        results.append(SegmentRange(previous_upper_bound, None))
        return results
