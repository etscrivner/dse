# -*- coding: utf-8 -*-
"""
    lib.statistics
    ~~~~~~~~~~~~~~
    Methods for performing statistical calculations


    mean(): Return the average of an iterable of values.
    standard_deviation(): Return the standard deviation of an iterable of
        values.
    median(): Return the median value from a list of values.
    upper_quartile(): Returns the upper quartile value (Q3) from a list of
        values.
    lower_quartile(): Returns the lower quartile value (Q1) from a list of
        values.
    interquartile_range(): Returns the interquartile range of a list of values.
    outliers(): Returns a list of all of the outliers in a given list of
        values.
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


def median(data):
    """Returns the median value in the given set of data.

    Arguments:
        data(list): A list of numbers

    Returns:
        int or float: The median value from the list
    """
    sorted_data = sorted(data)
    middle = len(data) / 2.0

    if len(data) % 2 == 0:
        lower = middle - 1
        upper = middle
        return (sorted_data[int(lower)] + sorted_data[int(upper)]) / 2.0
    else:
        return sorted_data[int(middle)]


def upper_quartile(data):
    """Computes the upper quartile of the given set of data.

    Arguments:
        data(list): A list of numbers

    Returns:
        float: The upper quartile for the data set
    """
    if len(data) < 2:
        raise RuntimeError('Too few values given to interquartile range')

    sorted_data = sorted(data)
    middle = len(data) / 2

    if len(data) % 2 == 0:
        return median(sorted_data[middle:])
    return median(sorted_data[(middle + 1):])


def lower_quartile(data):
    """Computes the lower quartile of the given set of data.

    Arguments:
        data(list): A list of numbers

    Returns:
        float: The lower quartile for the data set
    """
    if len(data) < 2:
        raise RuntimeError('Too few values given to interquartile range')

    sorted_data = sorted(data)
    middle = len(data) / 2

    return median(sorted_data[:middle])


def interquartile_range(data):
    """Computes the interquartile range for the given set of data.

    Arguments:
        data(list): A list of numbers

    Returns:
        float: The interquartile range for the data set

    Raises:
        RuntimeError: If there are too few values in the data set.
    """
    if len(data) < 2:
        raise RuntimeError('Too few values given to interquartile range')

    return upper_quartile(data) - lower_quartile(data)


def outliers(data):
    """Returns all items considered outliers in the given set of data.

    The test to determine if a value is an outlier is if it is less than 1.5
    interquartile ranges (IQRs) below the first quartile, or more than 1.5 IQRs
    above the third quartile.

    Arguments:
        data(list): A list of numbers

    Returns:
        list: The outliers from the given set of data
    """
    first_quartile = lower_quartile(data)
    third_quartile = upper_quartile(data)
    iqr = interquartile_range(data)

    results = []
    for each in data:
        if (each < (first_quartile - 1.5 * iqr) or
                each > (third_quartile + 1.5 * iqr)):
            results.append(each)
    return results
