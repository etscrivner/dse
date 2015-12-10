# -*- coding: utf-8 -*-
"""
    lib.display_table
    ~~~~~~~~~~~~~~~~~
    Reusable module that will display a nicely formatted table.


    DisplayTable: Interface for display data in a nicely formatted table.
"""
import sys


class DisplayTable(object):
    """Displays a nicely formatted table to standard output

    Example:

    >>> from lib import display_table
    >>> table = display_table.DisplayTable(['Project', 'Actual Time (Mins)'])
    >>> table.add_row(['1A', '120'])
    >>> table.add_row(['1B', '90'])
    >>> table.add_row(['2A', '60'])
    >>> table.display()
    +------------------------------+
    | Project | Actual Time (Mins) |
    +------------------------------+
    | 1A      | 120                |
    | 1B      | 90                 |
    | 2A      | 60                 |
    +------------------------------+

    """

    def __init__(self, column_names):
        """Initialize.

        Arguments:
            column_names(list): A list of column names
        """
        self.column_names = column_names
        self.rows = []

    def add_row(self, values):
        """Add a row to the display table.

        Arguments:
            values(list): A list of values

        Raises:
            ValueError: If there are fewer values than columns
        """
        if len(values) != len(self.column_names):
            raise ValueError(
                'Number of values does not match number of columns'
            )

        self.rows.append(values)

    def display(self):
        """Display data in table to standard output."""
        self.display_divider()
        self.display_row(self.column_names)
        self.display_divider()
        for row in self.rows:
            self.display_row(row)
        self.display_divider()

    def display_divider(self):
        """Display divider that separates rows to standard output."""
        column_sizes = self.get_column_sizes()
        # Create a divider with enough room for columns as well as lines and
        # spaces between columns. To do this accounting we add the column
        # sizes, then 3 additional marks for the 2 spaces and one line around
        # each word, and finally a single additional mark for the leading line.
        divider_length = sum(column_sizes) + (len(self.column_names) * 3) + 1
        print '+{}+'.format('-' * (divider_length - 2))

    def display_row(self, row):
        """Display the given row of data to standard output.

        Arguments:
            row(list): A row of column values
        """
        column_sizes = self.get_column_sizes()
        sys.stdout.write('|')
        for size, column in zip(column_sizes, row):
            sys.stdout.write(' ' + str(column).ljust(size) + ' |')
        print

    def get_column_sizes(self):
        """Returns the maximum size needed for each column.

        Returns:
            list: A list with the maximum size for each column at the index of
                that column.
        """
        column_sizes = [0] * len(self.column_names)
        all_rows = self.rows + [self.column_names]
        for row in all_rows:
            for index, col in enumerate(row):
                column_sizes[index] = max(column_sizes[index], len(str(col)))
        return column_sizes
