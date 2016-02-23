# -*- coding: utf-8 -*-
"""
    lib.probe
    ~~~~~~~~~
    Interfaces for using the PRoxy-Based Estimation (PROBE) methods.


    trim_to_equal_length(): Trim two lists to be of equal length.
    collect(): Collect key values into a list from a dict.
    HistoricalData: Represents historical estimation data.
    NoPredictionIntervalMixin: Prediction interval mixin that does nothing.
    CorrelationMixin: Mixin that adds correlation and significance
        computations.
    PredictionIntervalRangeMixin: Mixin that adds prediction intervals using
        historical range.
    PredictionIntervalProductivityMixin: Mixin that adds prediction intervals
        using historical productivity.
    EstimationMethod: Base class for all size and time estimation methods.
    ProbeEstimation: Interface for perform probe size and time estimation.
    ProbeSizeA: The linear regression proxy and actual size estimation.
    ProbeSizeB: The linear regression planned and actual size estimation.
    ProbeSizeC: Simple average between planned and actual size estimation.
    ProbeTimeA: The linear regression proxy size and actual time estimation.
    ProbeTimeB: The linear regression planned size and actual time estimation.
    ProbeTimeC1: The average proxy size and actual time.
    ProbeTimeC2: The average planned size and actual time.
    ProbeTimeC3: The average actual size and actual time.
"""
from lib import io
from lib import statistics


def trim_to_equal_length(x_data, y_data):
    """Trim the given lists to the same length by trimming data off the front
    of the longer list.

    Arguments:
        x_data(list): A list
        y_data(list): Another list

    Returns:
        tuple: Tuple containing trimmed first and second list.
    """
    if len(x_data) == len(y_data):
        return x_data, y_data
    elif len(x_data) > len(y_data):
        return x_data[-len(y_data):], y_data
    else:
        return x_data, y_data[-len(x_data):]


def collect(key, data):
    """Collects all the values from the given key into a single list
    of values.

    Arguments:
        key: The key to be collected
        data(list): A list of dictionaries

    Returns:
        list: A list of values under the given key.
    """
    return map(float, filter(None, [each.get(key) for each in data]))


class HistoricalData(object):
    """Interface for storing historical data"""

    def __init__(self,
                 planned_sizes,
                 proxy_sizes,
                 actual_sizes,
                 planned_times,
                 actual_times):
        """Initialize."""
        self.planned_sizes = planned_sizes
        self.proxy_sizes = proxy_sizes
        self.actual_sizes = actual_sizes
        self.planned_times = planned_times
        self.actual_times = actual_times

    @classmethod
    def from_csv_file(cls, filename):
        """Reads historical data from a CSV file.

        Arguments:
            filename(str): A file name

        Returns:
            HistoricalData: Historical data read from CSV file.
        """
        data = io.read_csv_file(filename)
        planned_sizes = collect('Planned A+M Size', data)
        proxy_sizes = collect('Proxy Size Estimate', data)
        actual_sizes = collect('Actual A+M Size', data)
        planned_times = collect('Planned Time', data)
        actual_times = collect('Actual Time', data)
        return cls(planned_sizes=planned_sizes,
                   proxy_sizes=proxy_sizes,
                   actual_sizes=actual_sizes,
                   planned_times=planned_times,
                   actual_times=actual_times)


class CorrelationMixin(object):
    """Mixin that defines correlation and signficance methods."""

    def get_correlation(self):
        """Returns the correlation between estimation data values.

        Returns:
            float: The correlation (R^2) value.
        """
        return statistics.correlation(self.x_values, self.y_values)**2

    def get_significance(self):
        """Returns the correlation significance.

        Returns:
            float: The percent chance that values were generated randomly.
        """
        return statistics.significance(self.x_values, self.y_values)


class NoPredictionIntervalMixin(object):
    """Prediction interval which does nothing"""

    def get_interval_range(self, estimated_value):
        return "N/A"

    def get_upi(self, estimated_value):
        return "N/A"

    def get_lpi(self, estimated_value):
        return "N/A"

    def get_interval_percent(self):
        return "N/A"


class PredictionIntervalRangeMixin(object):
    """Mixin that produces prediction interval ranges."""

    def get_interval_range(self, estimated_value):
        """Return the prediction interval range for the given estimated value.

        Arguments:
            estimated_value(float): The estimated value.

        Returns:
            float: The prediction interval range.
        """
        return statistics.prediction_range(
            estimated_value, 0.85, self.x_values, self.y_values)

    def get_upi(self, estimated_value):
        """Return the upper prediction interval (UPI).

        Arguments:
            estimated_value(float): The estimated value.

        Returns:
            float: The upper part of the prediction interval.
        """
        regression = self.get_regression()
        predicted_value = regression.estimate(estimated_value)
        return predicted_value + self.get_interval_range(estimated_value)

    def get_lpi(self, estimated_value):
        """Return the lower prediction interval (LPI).

        Arguments:
            estimated_value(float): The estimated value.

        Returns:
            float: The upper part of the prediction interval.
        """
        regression = self.get_regression()
        predicted_value = regression.estimate(estimated_value)
        return predicted_value - self.get_interval_range(estimated_value)

    def get_interval_percent(self):
        """Returns the interval percent.

        Returns:
            basestring: The interval percent as a string.
        """
        return "70%"


class PredictionIntervalProductivityMixin(object):
    """Prediction interval for time only, using historical productivity"""

    def get_interval_range(self, estimated_value):
        return "N/A"

    def get_upi(self, estimated_value):
        """Get upper prediction interval (UPI) using minimum historical
        productivity.

        Returns:
            float: The longest estimated time.
        """
        regression = self.get_regression()
        predicted_value = regression.estimate(estimated_value)
        productivities = self.get_productivities()
        if not productivities:
            return "N/A"
        min_productivity = min(productivities)
        return (predicted_value / min_productivity) * 60.0

    def get_lpi(self, estimated_value):
        """Get lower prediction interval (LPI) using maximum historical
        productivity.

        Returns:
            float: The shortest estimated time.
        """
        regression = self.get_regression()
        predicted_value = regression.estimate(estimated_value)
        productivities = self.get_productivities()
        if not productivities:
            return "N/A"
        max_productivity = max(productivities)
        return (predicted_value / max_productivity) * 60.0

    def get_interval_percent(self):
        return "N/A"

    def get_productivities(self):
        """Return historical productivity data.

        Returns:
            list: List of productivity in LOC / Hour.
        """
        actual_sizes = self.historical_data.actual_sizes
        actual_times = self.historical_data.actual_times
        return [
            (size / float(time)) * 60
            for size, time in zip(actual_sizes, actual_times)
        ]


class EstimationMethod(CorrelationMixin):
    """Base class for all PROBE estimation methods"""

    def __init__(self, historical_data):
        """Initialize.

        Arguments:
            historical_data(HistoricalData): Historical data for estimation.
        """
        self.historical_data = historical_data
        self.name = None

    def get_name(self):
        """Return the name of this estimation method.

        Returns:
            basestring: The name of this estimation method.
        """
        return self.name


class ProbeEstimation(object):
    """Interface for performing PROBE size and time estimations"""

    def __init__(self, historical_data):
        """Initialize.

        Arguments:
            historical_data(HistoricalData): Historical data to be used.
        """
        self.historical_data = historical_data
        # Size estimation methods in order of desirability
        self.size_estimation_methods = [ProbeSizeA, ProbeSizeB, ProbeSizeC]
        # Time estimation methods in order of desirability
        self.time_estimation_methods = [
            ProbeTimeA, ProbeTimeB, ProbeTimeC1, ProbeTimeC2, ProbeTimeC3
        ]

    def get_size_method(self, proxy_value):
        """Return the appropriate size estimation method for the given proxy
        value.

        Arguments:
            proxy_value(float): The proxy size estimate

        Returns:
            EstimationMethod: The appropriate estimation method.
        """
        for size_method in self.size_estimation_methods:
            if size_method.satisfies_preconditions(
                    self.historical_data, proxy_value):
                return size_method(self.historical_data)

    def get_time_method(self, proxy_value):
        """Return the appropriate time estimation method for the given proxy
        value.

        Arguments:
            proxy_value(float): The proxy size estimate

        Returns:
            EstimationMethod: The appropriate estimation method.
        """
        for time_method in self.time_estimation_methods:
            if time_method.satisfies_preconditions(
                    self.historical_data, proxy_value):
                return time_method(self.historical_data)


class ProbeSizeA(EstimationMethod, PredictionIntervalRangeMixin):
    """The proxy size estimate linear regression method for size."""

    def __init__(self, historical_data):
        super(ProbeSizeA, self).__init__(historical_data)
        self.name = 'A'
        self.x_values, self.y_values = trim_to_equal_length(
            self.historical_data.proxy_sizes,
            self.historical_data.actual_sizes)

    def get_regression(self):
        """Returns the linear regression for this estimation method.

        Returns:
            LinearRegression: A linear regression
        """
        return statistics.LinearRegression(
            statistics.beta_0(self.x_values, self.y_values),
            statistics.beta_1(self.x_values, self.y_values)
        )

    @classmethod
    def satisfies_preconditions(cls, historical_data, proxy_value):
        """Indicates whether or not the historical data allows this method to
        be used for the given proxy value.

        Arguments:
            historical_data(HistoricalData): The historical estimation data
            proxy_value(float): The proxy size estimate

        Returns:
            bool: True if this method can be used, False otherwise.
        """
        proxy_sizes, actual_sizes = trim_to_equal_length(
            historical_data.proxy_sizes, historical_data.actual_sizes
        )
        # Too few data points
        if len(actual_sizes) < 3:
            return False
        regression = cls(historical_data).get_regression()
        estimated_size = regression.estimate(proxy_value)
        # Beta0 is not close to zero
        if regression.beta0 > 0.25 * estimated_size:
            return False
        # Beta1 is out of bounds
        if regression.beta1 < 0.5 or regression.beta1 > 2.0:
            return False
        # Weakly correlated
        if statistics.correlation(proxy_sizes, actual_sizes)**2 < 0.5:
            return False
        # Weak statistical significance
        if statistics.significance(proxy_sizes, actual_sizes) > 0.05:
            return False
        return True


class ProbeSizeB(EstimationMethod, PredictionIntervalRangeMixin):
    """Estimation method using linear regression on planned and actual size"""

    def __init__(self, historical_data):
        super(ProbeSizeB, self).__init__(historical_data)
        self.name = 'B'
        self.x_values, self.y_values = trim_to_equal_length(
            self.historical_data.planned_sizes,
            self.historical_data.actual_sizes)

    def get_regression(self):
        """Returns the linear regression for this estimation method.

        Returns:
            LinearRegression: A linear regression
        """
        return statistics.LinearRegression(
            statistics.beta_0(self.x_values, self.y_values),
            statistics.beta_1(self.x_values, self.y_values)
        )

    @classmethod
    def satisfies_preconditions(cls, historical_data, proxy_value):
        """Indicates whether or not the historical data allows this method to
        be used for the given proxy value.

        Arguments:
            historical_data(HistoricalData): The historical estimation data
            proxy_value(float): The proxy size estimate

        Returns:
            bool: True if this method can be used, False otherwise.
        """
        planned_sizes, actual_sizes = trim_to_equal_length(
            historical_data.planned_sizes, historical_data.actual_sizes
        )
        if len(actual_sizes) < 3:
            return False
        regression = cls(historical_data).get_regression()
        estimated_size = regression.estimate(proxy_value)
        if regression.beta0 > 0.25 * estimated_size:
            return False
        if regression.beta1 < 0.5 or regression.beta1 > 2.0:
            return False
        if statistics.correlation(planned_sizes, actual_sizes)**2 < 0.5:
            return False
        if statistics.significance(planned_sizes, actual_sizes) > 0.05:
            return False
        return True


class ProbeSizeC(EstimationMethod, NoPredictionIntervalMixin):
    """Estimation method using historical average between planned and actual
    size."""

    def __init__(self, historical_data):
        super(ProbeSizeC, self).__init__(historical_data)
        self.name = 'C'
        self.x_values, self.y_values = trim_to_equal_length(
            self.historical_data.actual_sizes,
            self.historical_data.planned_sizes
        )

    def get_regression(self):
        """Returns the linear regression for this estimation method.

        Returns:
            LinearRegression: A linear regression
        """
        average = (sum(self.x_values) / float(sum(self.y_values)))
        return statistics.LinearRegression(0, average)

    @classmethod
    def satisfies_preconditions(cls, historical_data, proxy_value):
        """Indicates whether or not the historical data allows this method to
        be used for the given proxy value.

        Arguments:
            historical_data(HistoricalData): The historical estimation data
            proxy_value(float): The proxy size estimate

        Returns:
            bool: True if this method can be used, False otherwise.
        """
        if not historical_data.actual_sizes:
            return False
        if not historical_data.planned_sizes:
            return False
        if (len(historical_data.planned_sizes) !=
                len(historical_data.actual_sizes)):
            return False
        return True


class ProbeTimeA(EstimationMethod, PredictionIntervalRangeMixin):
    """The proxy size estimate linear regression method for time."""

    def __init__(self, historical_data):
        super(ProbeTimeA, self).__init__(historical_data)
        self.name = 'A'
        self.x_values, self.y_values = trim_to_equal_length(
            self.historical_data.proxy_sizes,
            self.historical_data.actual_times
        )

    def get_regression(self):
        """Returns the linear regression for this estimation method.

        Returns:
            LinearRegression: A linear regression
        """
        return statistics.LinearRegression(
            statistics.beta_0(self.x_values, self.y_values),
            statistics.beta_1(self.x_values, self.y_values))

    @classmethod
    def satisfies_preconditions(cls, historical_data, proxy_value):
        """Indicates whether or not the historical data allows this method to
        be used for the given proxy value.

        Arguments:
            historical_data(HistoricalData): The historical estimation data
            proxy_value(float): The proxy size estimate

        Returns:
            bool: True if this method can be used, False otherwise.
        """
        proxy_sizes, actual_times = trim_to_equal_length(
            historical_data.proxy_sizes, historical_data.actual_times)
        if len(proxy_sizes) < 3:
            return False
        regression = cls(historical_data).get_regression()
        # Beta0 should be small
        expected_time = regression.estimate(proxy_value)
        if regression.beta0 > 0.25 * expected_time:
            return False
        # Beta1 one should be close to historical productivity
        productivity = 1.0 / (float(sum(proxy_sizes)) / sum(actual_times))
        beta1_range = 0.5 * productivity
        if (regression.beta1 < (productivity - beta1_range) or
                regression.beta1 > (productivity + beta1_range)):
            return False
        # Correlation should be strong
        if statistics.correlation(proxy_sizes, actual_times)**2 < 0.5:
            return False
        # Correlation should be significant
        if statistics.significance(proxy_sizes, actual_times) > 0.05:
            return False
        return True


class ProbeTimeB(EstimationMethod, PredictionIntervalRangeMixin):
    """The planned size estimate linear regression method for time."""

    def __init__(self, historical_data):
        super(ProbeTimeB, self).__init__(historical_data)
        self.name = 'B'
        self.x_values, self.y_values = trim_to_equal_length(
            self.historical_data.planned_sizes,
            self.historical_data.actual_times
        )

    def get_regression(self):
        """Returns the linear regression for this estimation method.

        Returns:
            LinearRegression: A linear regression
        """
        return statistics.LinearRegression(
            statistics.beta_0(self.x_values, self.y_values),
            statistics.beta_1(self.x_values, self.y_values))

    @classmethod
    def satisfies_preconditions(cls, historical_data, proxy_value):
        """Indicates whether or not the historical data allows this method to
        be used for the given proxy value.

        Arguments:
            historical_data(HistoricalData): The historical estimation data
            proxy_value(float): The proxy size estimate

        Returns:
            bool: True if this method can be used, False otherwise.
        """
        planned_sizes, actual_times = trim_to_equal_length(
            historical_data.proxy_sizes, historical_data.actual_times)
        if len(planned_sizes) < 3:
            return False
        regression = cls(historical_data).get_regression()
        expected_time = regression.estimate(proxy_value)
        if regression.beta0 > 0.25 * expected_time:
            return False
        productivity = 1.0 / (sum(planned_sizes) / sum(actual_times))
        beta1_range = 0.5 * productivity
        if (regression.beta1 < (productivity - beta1_range) or
                regression.beta > (productivity + beta1_range)):
            return False
        if statistics.correlation(planned_sizes, actual_times)**2 < 0.5:
            return False
        if statistics.significance(planned_sizes, actual_times) > 0.05:
            return False
        return True


class ProbeTimeC1(EstimationMethod, PredictionIntervalProductivityMixin):
    """Estimation method using average of proxy sizes and actual times"""

    def __init__(self, historical_data):
        super(ProbeTimeC1, self).__init__(historical_data)
        self.name = 'C1'
        self.x_values, self.y_values = trim_to_equal_length(
            self.historical_data.actual_times,
            self.historical_data.proxy_sizes
        )

    def get_regression(self):
        """Returns the linear regression for this estimation method.

        Returns:
            LinearRegression: A linear regression
        """
        return statistics.LinearRegression(
            0, sum(self.x_values) / float(sum(self.y_values)))

    @classmethod
    def satisfies_preconditions(cls, historical_data, proxy_value):
        """Indicates whether or not the historical data allows this method to
        be used for the given proxy value.

        Arguments:
            historical_data(HistoricalData): The historical estimation data
            proxy_value(float): The proxy size estimate

        Returns:
            bool: True if this method can be used, False otherwise.
        """
        if not historical_data.proxy_sizes or not historical_data.actual_times:
            return False
        return True


class ProbeTimeC2(EstimationMethod, PredictionIntervalProductivityMixin):
    """Estimation method using average of planned sizes and actual times"""

    def __init__(self, historical_data):
        super(ProbeTimeC2, self).__init__(historical_data)
        self.name = 'C2'
        self.x_values, self.y_values = trim_to_equal_length(
            self.historical_data.actual_times,
            self.historical_data.planned_sizes
        )

    def get_regression(self):
        """Returns the linear regression for this estimation method.

        Returns:
            LinearRegression: A linear regression
        """
        return statistics.LinearRegression(
            0, sum(self.x_values) / float(sum(self.y_values)))

    @classmethod
    def satisfies_preconditions(cls, historical_data, proxy_value):
        """Indicates whether or not the historical data allows this method to
        be used for the given proxy value.

        Arguments:
            historical_data(HistoricalData): The historical estimation data
            proxy_value(float): The proxy size estimate

        Returns:
            bool: True if this method can be used, False otherwise.
        """
        if (not historical_data.planned_sizes or
                not historical_data.actual_times):
            return False
        return True


class ProbeTimeC3(EstimationMethod, PredictionIntervalProductivityMixin):
    """Estimation method using average of actual sizes and actual times"""

    def __init__(self, historical_data):
        super(ProbeTimeC3, self).__init__(historical_data)
        self.name = 'C3'
        self.x_values, self.y_values = trim_to_equal_length(
            self.historical_data.actual_times,
            self.historical_data.actual_sizes
        )

    def get_regression(self):
        """Returns the linear regression for this estimation method.

        Returns:
            LinearRegression: A linear regression
        """
        return statistics.LinearRegression(
            0, sum(self.x_values) / float(sum(self.y_values)))

    @classmethod
    def satisfies_preconditions(cls, historical_data, proxy_value):
        """Indicates whether or not the historical data allows this method to
        be used for the given proxy value.

        Arguments:
            historical_data(HistoricalData): The historical estimation data
            proxy_value(float): The proxy size estimate

        Returns:
            bool: True if this method can be used, False otherwise.
        """
        if (not historical_data.actual_sizes or
                not historical_data.actual_times):
            return False
        return True
