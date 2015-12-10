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
    remove_outliers(): Returns lists of values with outliers removed.
    size_ranges(): Computes log-normal size ranges for a given set of data.
    beta_0(): Returns the beta0 linear regression parameter
    beta_1(): Returns the beta1 linear regression parameter
    beta_0_warnings(): Returns warning messages for beta_0 value.
    beta_1_warnings(): Returns warning messages for beta_1 value.
    normal_distribution(): Returns the probability density of the normal
        distribution at a given x value.
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
        raise RuntimeError('Too few values given to upper quartile')

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
        raise RuntimeError('Too few values given to lower quartile')

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

    Raises:
        RuntimeError: If too few values given
    """
    if len(data) < 2:
        raise RuntimeError('Too few values given to outliers')

    first_quartile = lower_quartile(data)
    third_quartile = upper_quartile(data)
    iqr = interquartile_range(data)

    lower_limit = (first_quartile - 1.5 * iqr)
    upper_limit = (third_quartile + 1.5 * iqr)

    results = []
    for each in data:
        if each < lower_limit or each > upper_limit:
            results.append(each)
    return results


def remove_outliers(*data_sets):
    """Removes outlier items from the given data sets.

    Arguments:
        data_sets(tuple): A list of data sets

    Returns:
        tuple: Update data sets with outliers removed.

    Raises:
        RuntimeError: If the data sets do not all have the same length
    """
    operating_sets = [each[:] for each in data_sets]
    unique_lengths = set([len(each) for each in operating_sets])
    if len(unique_lengths) != 1:
        raise RuntimeError(
            'Data sets of different lengths passed to remove outliers')
    all_outliers = [outliers(each) for each in operating_sets]
    for idx, item_outliers in enumerate(all_outliers):
        for outlier in item_outliers:
            outlier_index = operating_sets[idx].index(outlier)
            for each in operating_sets:
                each.pop(outlier_index)
    return operating_sets


def size_ranges(data):
    """Computes size ranges characterizing given data set.

    Arguments:
        data(list): A list of real numbered values

    Returns:
        list: A list containing size ranges characterizing data organized as
            [Very Small, Small, Medium, Large, Very Large]
    """
    log_normal_data = [math.log(each) for each in data]
    log_avg = mean(log_normal_data)
    std_dev = standard_deviation(log_normal_data)
    log_results = [
        log_avg - 2 * std_dev,
        log_avg - std_dev,
        log_avg,
        log_avg + std_dev,
        log_avg + 2 * std_dev]
    return [math.exp(each) for each in log_results]


def beta_1(x_data, y_data):
    """Calculate the beta_0 linear regression parameter for two sets of related
    data.

    Arguments:
        x_data(list): A list of values
        y_data(list): A list of values

    Returns:
        float: The beta_0 linear regression parameter

    Raises:
        RuntimeError: If the data lists are of unequal length
    """
    if len(x_data) != len(y_data):
        raise RuntimeError('X and Y data do not have same number of items')
    x_avg = mean(x_data)
    y_avg = mean(y_data)
    n = len(x_data)
    dividend = sum([x * y for x, y in zip(x_data, y_data)])
    dividend -= n * x_avg * y_avg
    divisor = sum([x**2 for x in x_data])
    divisor -= n * (x_avg)**2
    return dividend / float(divisor)


def beta_0(x_data, y_data):
    """Calculate the beta_0 linear regression parameter for two sets of related
    data.

    Arguments:
        x_data(list): A list of values
        y_data(list): A list of values

    Returns:
        float: The beta_0 linear regression parameter

    Raises:
        RuntimeError: If the data lists are of unequal length
    """
    if len(x_data) != len(y_data):
        raise RuntimeError('X and Y data do not have same number of items')
    x_avg = mean(x_data)
    y_avg = mean(y_data)
    return y_avg - beta_1(x_data, y_data) * x_avg


def beta_0_warnings(beta0):
    """Print warnings for the given beta0 value.

    Arguments:
        beta0(float): A beta_0 linear regression parameter

    Returns:
        list: Contains warning messages for beta value
    """
    warnings = []
    if beta0 > 1.0:
        warnings.append('Beta0 is not near 0')
    return warnings


def beta_1_warnings(beta1):
    """Print warnings for the given beta1 value.

    Arguments:
        beta1(float): A beta_1 linear regression parameter.

    Returns:
        list: Contains warning messages for beta value
    """
    warnings = []
    if beta1 < 0.5 or beta1 > 2:
        warnings.append('Beta1 is not near 1')
    return warnings


def normal_distribution(x):
    """Computes the value of the normal distribution probability density
    function at the given x value.

    Arguments:
        x(float): The x value at which to compute the probability density.

    Returns:
        float: The normal distribution value at the given x.
    """
    return (1 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * x**2)
