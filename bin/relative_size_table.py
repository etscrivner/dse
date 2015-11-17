# -*- coding: utf-8 -*-
"""
    relative_size_table
    ~~~~~~~~~~~~~~~~~~~
    Compute and display a relative size table for given data.


    Application: The object defining the overall application entry point.
    DisplaySizeTableReport: Display report containing the relative size table
        for given data.
"""
import collections
import argparse

from lib import io
from lib import display_table
from lib import statistics


class DisplaySizeTableReport(object):
    """Display relative size table report for given data"""

    REQUIRED_KEYS = ('Name', 'Category', 'Parts', 'Total LOC')

    def __init__(self, file_path):
        self.file_path = file_path

    def execute(self):
        """Calculate and display the relative size table report"""
        data = io.read_csv_file(self.file_path)

        if not data:
            print "NO DATA"
            return

        if not all([self.are_valid_keys(each.keys()) for each in data]):
            raise RuntimeError(
                'Invalid data columns {}'.format(data[0].keys()))

        normalized_data = self.get_normalized_data(data)
        normalized_by_category = self.group_by_category(normalized_data)
        results = {}
        for category, items in normalized_by_category.iteritems():
            if len(items) < 2:
                results[category] = [items[0]] * 5
            else:
                results[category] = statistics.size_ranges(items)
        self.print_table(results)

    def are_valid_keys(self, keys):
        """Indicates whether or not the given list of keys contains the
        expected keys.

        Arguments:
            keys(list): A list of keys

        Returns:
            bool: True if the keys are valid, False otherwise.
        """
        return (
            len(keys) == len(self.REQUIRED_KEYS) and
            all([key in keys for key in self.REQUIRED_KEYS]))

    def get_normalized_data(self, data):
        """Returns the given object size data normalized by number of parts.

        Arguments:
            data(list): Contains a list of data including number of parts and
                total size.

        Returns:
            list: The given data normalized to size per part
        """
        results = []
        for each in data:
            loc_per_part = float(each['Total LOC']) / float(each['Parts'])
            results.append({
                'Name': each['Name'],
                'Category': each['Category'],
                'LOC': loc_per_part})
        return results

    def group_by_category(self, data):
        """Groups the given data by category

        Arguments:
            data(list): Contains normalized data

        Returns:
            dict: Keyed by category, containing list of lines of code for that
                category.
        """
        results = collections.defaultdict(list)
        for each in data:
            results[each['Category']].append(each['LOC'])
        return results

    def print_table(self, results):
        """Displays the given size range results in a table.

        Arguments:
            results(dict): A dictionary containing results data
        """
        table = display_table.DisplayTable([
            'Category', 'VS', 'S', 'M', 'L', 'VL'])
        for category, size_range in results.items():
            formatted_size_range = [
                '{:0.02f}'.format(each) for each in size_range]
            table.add_row([category] + formatted_size_range)
        table.display()


class Application(object):
    """Entry point for the application"""

    def execute(self):
        """Handle parsing command-line arguments and running program"""
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'PATH', help='CSV file containing object size data')
        args = parser.parse_args()
        file_path = args.PATH
        DisplaySizeTableReport(file_path).execute()

if __name__ == '__main__':
    Application().execute()
