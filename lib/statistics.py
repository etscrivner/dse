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
    make_t_distribution(): Construct a t-distribution function with the given
        number of degrees of freedom.
    variance_around_regression(): Computes the variance around the regression
        of the given values.
    standard_deviation_around_regression(): Computes the standard deviation
        around the regression of the given values.
    prediction_range(): Compute the prediction range for a given estimated
        value.
    correlation(): Computes the correlation between two data sets.
    significance(): Returns the correlation significance of the given data
        sets.
    LinearRegression: Represents a linear regression.
"""
import math

from lib import integration


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
    above the third quartile. Or, more succintly

    Outlier If
        Value < 1.5 * Q1 or
        Value > 1.5 * Q3

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


def make_t_distribution(degrees_of_freedom):
    """Great a t-distribution function with the given number of degrees of
    freedom.

    Arguments:
        degrees_of_freedom(float): The degrees of freedom

    Returns:
        callable: t-distribution function
    """
    const = math.gamma((degrees_of_freedom + 1) / 2.0)
    const /= (
        math.sqrt(degrees_of_freedom * math.pi) *
        math.gamma(degrees_of_freedom / 2.0)
    )

    def tdist(x):
        result = math.pow(
            1 + (x**2 / degrees_of_freedom),
            -((degrees_of_freedom + 1) / 2.0)
        )
        return const * result

    return tdist


def variance_around_regression(xvalues, yvalues):
    """Compute the variance around the regression of the given values.

    Arguments:
        xvalues(list): A list of values
        yvalues(list): A list of values

    Returns:
        float: The variance around the regression
    """
    n = len(xvalues)
    b0 = beta_0(xvalues, yvalues)
    b1 = beta_1(xvalues, yvalues)
    result = (1.0 / (n - 2))
    return result * sum([(y - b0 - b1*x)**2 for x, y in zip(xvalues, yvalues)])


def standard_deviation_around_regression(xvalues, yvalues):
    """Computes the standard deviation around the regression of the given
    lists of values.

    Arguments:
        xvalues(list): A list of x values.
        yvalues(list): A list of y values.

    Returns:
        float: The standard deviation around the regression
    """
    return math.sqrt(variance_around_regression(xvalues, yvalues))


def prediction_range(x_k, alpha, xvalues, yvalues):
    """Computes the prediction range for the given alpha value.

    Arguments:
        x_k(float): An estimated value
        alpha(float): The t-distribution alpha value.
        xvalues(list): A list of values
        yvalues(list): A list of values

    Returns:
        float: The prediction range
    """
    if len(xvalues) < 3 or len(yvalues) < 3:
        raise RuntimeError('Too few values to compute prediction interval')

    n = len(xvalues)
    tdist = make_t_distribution(n - 2)
    integ = integration.Integrator(20, 0.00001)
    h = lambda x: integ.integrate_minus_infinity_to(tdist, x)
    std_dev = standard_deviation_around_regression(xvalues, yvalues)
    t_value = integration.approximate_inverse(h, alpha)
    x_avg = mean(xvalues)

    const = t_value * std_dev
    result = 1 + 1.0/n
    result += (x_k - x_avg)**2 / sum([(x - x_avg)**2 for x in xvalues])

    return const * math.sqrt(result)


def correlation(x_data, y_data):
    """Returns the correlation between two data sets.

    Arguments:
        x_data(list): The first data set
        y_data(list): The second data set

    Raises:
        RuntimeError: If the data sets do not have the same length.

    Returns:
        float: The correlation between the two data sets.
    """
    if len(x_data) != len(y_data):
        raise RuntimeError('Size mismatch between data sets')

    num_items = len(x_data)

    numerator = num_items * sum([x*y for x, y in zip(x_data, y_data)])
    numerator -= sum(x_data) * sum(y_data)

    denominator = (
        (num_items * sum([x**2 for x in x_data]) - sum(x_data)**2) *
        (num_items * sum([y**2 for y in y_data]) - sum(y_data)**2)
    )

    return numerator / math.sqrt(denominator)


def t_value(x_data, y_data):
    """Computes the t-distribution significance value for the given two data
    sets.

    Arguments:
        x_data(list): The first data set.
        y_data(list): The second data set.

    Returns:
        float: The significance t value.
    """
    if len(x_data) == 0 or len(y_data) == 0:
        raise RuntimeError('Must have data in data set')
    if len(x_data) != len(y_data):
        raise RuntimeError('Data sets must be of equal length')

    corr = correlation(x_data, y_data)
    if corr == 1:
        raise RuntimeError('Invalid data, identical data sets.')

    return abs(corr) * math.sqrt(len(x_data) - 2.0) / math.sqrt(1.0 - corr**2)


def significance(x_data, y_data):
    """Returns the significance of the correlation between the two data
    sets.

    Arguments:
        x_data(list): The first data set
        y_data(list): The second data set

    Returns:
        float: The probability of the correlation between the two data sets
            occurring by chance.
    """
    if len(x_data) < 3 or len(y_data) < 3:
        raise RuntimeError(
            'Too few items to perform significance calculation')

    if len(x_data) != len(y_data):
        raise RuntimeError('Size mismatch between data sets')

    t_val = t_value(x_data, y_data)
    tdist = make_t_distribution(len(x_data) - 2)
    integ = integration.Integrator(10, 10E-6)
    p_value = integ.integrate_minus_infinity_to(tdist, t_val)
    return 2 * (1 - p_value)


class LinearRegression(object):
    """Interface for performing a linear regression"""

    def __init__(self, beta0, beta1):
        """Initialize linear regression.

        Arguments:
            beta0(float): The beta 0 value.
            beta1(float): The beta 1 value.
        """
        self.beta0 = beta0
        self.beta1 = beta1

    def estimate(self, proxy_value):
        """Perform linear regression with the given estimation value.

        Arguments:
            proxy_value(float): The estimation value

        Returns:
            float: The project value from the linear regression
        """
        return self.beta0 + self.beta1 * proxy_value
