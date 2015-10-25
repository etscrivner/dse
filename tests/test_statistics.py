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
