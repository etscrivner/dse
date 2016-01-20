# -*- coding: utf-8 -*-
import unittest

from lib import statistics


class TestMean(unittest.TestCase):
    def test_should_raise_error_if_no_values_given(self):
        self.assertRaisesRegexp(
            RuntimeError,
            'No values given to mean',
            statistics.mean,
            []
        )

    def test_should_return_value_for_single_value(self):
        self.assertEqual(12, statistics.mean([12]))

    def test_should_correctly_compute_the_mean(self):
        self.assertAlmostEqual(5.0, statistics.mean(range(1, 10)))


class TestStandardDeviation(unittest.TestCase):
    def test_should_raise_error_if_no_values_given(self):
        self.assertRaisesRegexp(
            RuntimeError,
            'No values given to mean',
            statistics.standard_deviation,
            []
        )

    def test_should_raise_error_if_only_one_value_given(self):
        self.assertRaisesRegexp(
            RuntimeError,
            'Too few values given to standard deviation',
            statistics.standard_deviation,
            [1]
        )

    def test_should_correctly_compute_standard_deviation(self):
        self.assertAlmostEqual(
            2.73861,
            statistics.standard_deviation(range(1, 10)),
            places=5)


class TestMedian(unittest.TestCase):
    def test_should_return_middle_value_if_odd_num_items(self):
        self.assertEqual(2, statistics.median([1, 2, 3]))

    def test_should_return_average_of_middle_values_if_even_num_items(self):
        self.assertEqual(2.5, statistics.median([1, 2, 3, 4]))


class TestUpperQuartile(unittest.TestCase):
    def test_should_raise_error_if_too_few_items(self):
        self.assertRaisesRegexp(
            RuntimeError,
            'Too few values given to upper quartile',
            statistics.upper_quartile,
            [])

    def test_should_return_correct_value_for_odd_num_items(self):
        self.assertEqual(
            6,
            statistics.upper_quartile([1, 2, 3, 4, 5, 6, 7]))

    def test_should_return_correct_value_for_even_num_items(self):
        self.assertEqual(
            5, statistics.upper_quartile([1, 2, 3, 4, 5, 6]))


class TestLowerQuartile(unittest.TestCase):
    def test_should_raise_error_if_too_few_items(self):
        self.assertRaisesRegexp(
            RuntimeError,
            'Too few values given to lower quartile',
            statistics.lower_quartile,
            [])

    def test_should_return_correct_value_for_odd_num_items(self):
        self.assertEqual(2, statistics.lower_quartile([1, 2, 3, 4, 5, 6, 7]))

    def test_should_return_correct_value_for_even_num_items(self):
        self.assertEqual(2, statistics.lower_quartile([1, 2, 3, 4, 5, 6]))


class TestInterquartileRange(unittest.TestCase):
    def test_should_raise_error_if_too_few_items(self):
        self.assertRaisesRegexp(
            RuntimeError,
            'Too few values given to interquartile range',
            statistics.interquartile_range,
            [])

    def test_should_return_correct_value_for_odd_num_items(self):
        self.assertEqual(
            4, statistics.interquartile_range([1, 2, 3, 4, 5, 6, 7]))

    def test_should_return_correct_value_For_even_num_items(self):
        self.assertEqual(
            3, statistics.interquartile_range([1, 2, 3, 4, 5, 6]))


class TestOutliers(unittest.TestCase):
    def test_should_raise_error_if_too_few_values_given(self):
        self.assertRaisesRegexp(
            RuntimeError,
            'Too few values given to outliers',
            statistics.outliers,
            [])

    def test_should_return_empty_list_if_no_outliers(self):
        self.assertEqual([], statistics.outliers([1, 2, 3, 4, 5, 6, 7]))

    def test_should_return_outliers_if_present(self):
        self.assertEqual([209], statistics.outliers([1, 2, 3, 4, 5, 209]))


class TestSizeRanges(unittest.TestCase):
    def test_should_return_correct_size_ranges(self):
        expected = [0.8591994480026335,
                    1.7041441133233817,
                    3.3800151591412964,
                    6.703953255306071,
                    13.296682746460451]
        self.assertEqual(
            expected, statistics.size_ranges([1, 2, 3, 4, 5, 6, 7]))


class TestRemoveOutliers(unittest.TestCase):
    def test_should_correctly_remove_outliers(self):
        x_data = [1, 2, 3, 4, 5, 209]
        y_data = [1, 2, 3, 4, 5, 6]
        x_result, y_result = statistics.remove_outliers(x_data, y_data)
        self.assertEqual(x_result, [1, 2, 3, 4, 5])
        self.assertEqual(y_result, [1, 2, 3, 4, 5])


class TestCorrelationAndSignificance(unittest.TestCase):
    def setUp(self):
        super(TestCorrelationAndSignificance, self).setUp()
        # Data from Table A12 in A Discipline for Software Engineering
        self.x_data = [186, 699, 132, 272, 291, 331, 199, 1890, 788, 1601]
        self.y_data = [
            15.0, 69.9, 6.5, 22.4, 28.4, 65.9, 19.4, 198.7, 38.8, 138.2
        ]

    def test_should_correctly_compute_correlation(self):
        result = statistics.correlation(self.x_data, self.y_data)
        self.assertAlmostEqual(result, 0.9543158)
        self.assertAlmostEqual(result**2, 0.9107, 4)

    def test_should_correctly_compute_significance(self):
        result = statistics.significance(self.x_data, self.y_data)
        self.assertAlmostEqual(result, 0.99999, 4)
