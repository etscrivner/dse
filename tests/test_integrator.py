# -*- coding: utf-8 -*-
import unittest

from lib import integration
from lib import statistics


class TestIntegrator(unittest.TestCase):
    def setUp(self):
        super(TestIntegrator, self).setUp()
        self.integrator = integration.Integrator(20, 0.0001)

    def test_it_should_integrate_to_positive_value(self):
        result = self.integrator.integrate_minus_infinity_to(
            statistics.normal_distribution, 2.5)
        self.assertAlmostEqual(result, 0.9938, 4)

    def test_it_should_integrate_to_almost_zero_value(self):
        result = self.integrator.integrate_minus_infinity_to(
            statistics.normal_distribution, 0.2)
        self.assertAlmostEqual(result, 0.5793, 4)

    def test_it_should_integrate_to_negative_value(self):
        result = self.integrator.integrate_minus_infinity_to(
            statistics.normal_distribution, -1.1)
        self.assertAlmostEqual(result, 0.1357, 4)
