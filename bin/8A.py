# -*- coding: utf-8 -*-
"""
    8A
    ~~
    Exercise 8A: Load a file and sort by the selected column.

    Application: The application object.
"""
import sys

from lib import io
from lib import display_table


class Application(object):
    def execute(self):
        print '8A: Load CSV file and sort by selected column'
        print

        file_name = io.prompt_existant_file_name('CSV file to sort: ')
        data = io.read_csv_file(file_name)

        if not data:
            print 'ERROR: File contains no data.'
            sys.exit(1)

        column_names = data[0].keys()
        sort_column = io.choose_from_list('Column to sort on', column_names)

        try:
            for each in data:
                each[sort_column] = int(each[sort_column])
        except ValueError:
            print 'ERROR: Column {} contains non-integer value.'.format(
                sort_column)
            sys.exit(1)

        sorted_data = sorted(data, key=lambda item: item[sort_column])

        table = display_table.DisplayTable(column_names)
        for each in sorted_data:
            table.add_row(each.values())
        table.display()


if __name__ == '__main__':
    Application().execute()
