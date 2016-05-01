# -*- coding: utf-8 -*-
"""
    3A
    ~~
    The PSP Exercise 3A. Create a new LOC counter that will also count and
    display the LOC and number of methods in individual classes.


"""
import argparse

from lib import display_table
from lib import io
from lib import loc


class ModuleReport(object):
    """Count LOC in given python file and display a single file report"""

    def __init__(self, file_path):
        """Initialize.

        Arguments:
            file_path(basestring): File system path to module
        """
        self.file_path = file_path

    def execute(self):
        """Count the lines of code in the given file and display a report."""
        tree = loc.SingleFileCounter(self.file_path).execute()

        self.print_title('REPORT')
        print
        print
        self.print_heading('Module Breakdown')
        print
        self.print_module_breakdown(tree)
        print
        print
        self.print_heading('Module Totals')
        print
        class_methods = tree.num_of_type(loc.CountTree.NodeType.ClassMethod)
        print 'Logical LOC', tree.total_logical_loc()
        print 'Classes', tree.num_of_type(loc.CountTree.NodeType.Class)
        print 'Class Methods', class_methods
        print 'Functions', tree.num_of_type(loc.CountTree.NodeType.Function)
        print
        if class_methods > 0:
            class_method_loc = tree.total_logical_loc_of_type(
                loc.CountTree.NodeType.ClassMethod)
            print 'LOC / Class Method: ', class_method_loc / class_methods
            print

    def print_module_breakdown(self, tree, indent_level=0):
        """Print module breakdown for the given tree.

        Arguments:
            tree(loc.CountTree): A module line counting tree
            indent_level(int): The level of indentation to be used
        """
        print '{}\- {}: {}'.format(
            '  '*indent_level, tree.name, tree.total_logical_loc()
        )
        for kid in tree.children:
            self.print_module_breakdown(kid, (indent_level + 1))

    def print_title(self, title):
        """Print the given title to standard output.

        Arguments:
            title(basestring): The title to be printed
        """
        print title
        print '=' * len(title)

    def print_heading(self, heading):
        """Print a section heading to standard output.

        Arguments:
            heading(basestring): The section heading
        """
        print heading
        print '-' * len(heading)


class ProgramReport(object):
    """Count LOC of all files in a given path and display report"""

    def __init__(self, file_path):
        """Initialize.

        Arguments:
            file_path(basestring): A file path
        """
        self.file_path = file_path
        self.table = display_table.DisplayTable([
            "File", "Logical LOC", "Classes", "Class Methods", "Functions"
        ])

    def execute(self):
        """Count lines of code and display tabular report"""
        matching_files = io.find_files_matching(self.file_path, '*.py')
        file_roots = [
            loc.SingleFileCounter(each).execute() for each in matching_files
        ]
        for root in file_roots:
            self.table.add_row([
                root.name,
                root.total_logical_loc(),
                root.num_of_type(loc.CountTree.NodeType.Class),
                root.num_of_type(loc.CountTree.NodeType.ClassMethod),
                root.num_of_type(loc.CountTree.NodeType.Function)
            ])
        self.table.add_row(self.get_final_row(file_roots))
        self.table.display()

    def get_final_row(self, file_roots):
        """Return the final table row for the given file count trees.

        Arguments:
            file_roots(list): A list of CountTrees for various files.

        Returns:
            list: Contains final total row for table
        """
        final_row = ["TOTAL"]
        final_row.append(
            sum([each.total_logical_loc() for each in file_roots])
        )
        final_row.append(
            sum([
                each.num_of_type(loc.CountTree.NodeType.Class)
                for each in file_roots])
        )
        final_row.append(
            sum([
                each.num_of_type(loc.CountTree.NodeType.ClassMethod)
                for each in file_roots])
        )
        final_row.append(
            sum([
                each.num_of_type(loc.CountTree.NodeType.Function)
                for each in file_roots])
        )
        return final_row


class Application(object):
    """Entry point for the application"""

    def execute(self):
        """Execute the application and handle any errors"""
        parser = argparse.ArgumentParser(
            description=(
                'Count logical lines of code in a python file or in a set '
                'of python modules'))
        parser.add_argument(
            'PATH', help='file system path or single file name to be counted.')
        parser.add_argument(
            '-r', '--recursive', action='store_true',
            help='recursively count lines in all subdirectories of path.')
        args = parser.parse_args()
        file_path = args.PATH
        if args.recursive:
            ProgramReport(file_path).execute()
        else:
            ModuleReport(file_path).execute()


if __name__ == '__main__':
    Application().execute()
