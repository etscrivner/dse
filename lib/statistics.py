# -*- coding: utf-8 -*-
"""
    lib.statistics
    ~~~~~~~~~~~~~~
    Methods for performing statistical calculations


"""
import math


def mean(iterable):
    """Computes the mean of the numerical values in an iterable.

    Arguments:
        iterable(iterable): An iterable containing numerical values.

    Returns:
        float: The mean of the given of values.

    Raises:
        RuntimeError: If no values are given
    """
    total = 0
    num_items = 0

    for each in iterable:
        total += float(each)
        num_items += 1

    if num_items == 0:
        raise RuntimeError('No values given to mean')

    return total / num_items


def standard_deviation(iterable):
    """Computes the standard deviation for an iterable of numerical values.

    Arguments:
        iterable(iterable): An iterable containing numerical values.

    Returns:
        float: The standard deviation of the given values.

    Raises:
        RuntimeError: If any less than 2 values are given.
    """
    total = 0
    num_items = 0
    average = mean(iterable)

    for each in iterable:
        total += (float(each) - average)**2
        num_items += 1

    if num_items < 2:
        raise RuntimeError('Too few values given to standard deviation')

    return math.sqrt(total / (num_items - 1))
