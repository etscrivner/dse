# -*- coding: utf-8 -*-
"""
    lib.loc
    ~~~~~~~
    Reusable components for lines of code counting.

    module_file_from_path(): Converts a file system path into a python module
        name.
    CountTree: Tree data structure for storing lines of code (LOC) counts.
    SingleFileCounter: Interface for counting lines of code in a single file.
"""
import os
import tokenize


def module_file_from_path(file_path):
    """Converts a file path into its module file name.

    Example:
    >>> module_file_from_path('a/b/c/my_module.py')
    'my_module'

    Arguments:
        file_path(basestring): A file system path

    Returns:
        basestring: The python module name or the file path if transformation
            fails.
    """
    parts = file_path.split(os.path.sep)
    if parts:
        module_name_parts = parts[-1].split('.py')
        if module_name_parts:
            return module_name_parts[0]
    return file_path


class CountTree(object):
    """Tree used to store lines of code (LOC) counts for a single file
    hierarchically. This preserves natural class and function structure and
    allows for traversals to provide counts for the various object types.
    """

    class NodeType(object):
        """Enumeration of node types"""
        Module = 0
        Class = 1
        ClassMethod = 2
        Function = 3

    def __init__(self, name=None, parent=None):
        """Initialize

        Arguments:
            name(basestring): The name of this particular node in the tree.
            parent(CountTree or None): The parent of this node.
        """
        self.name = name
        self.parent = parent
        # A list of the children of this node
        self.children = []
        # Flag saving state information for token parser about whether or not
        # this node is currently within a comment.
        self.in_comment = False
        # Indicates whether or not the previous item was a docstring
        self.in_docstring = False
        # Indicates the type of this node.
        self.node_type = self.NodeType.Module
        # The level of indentation this node is represented by. Used for
        # display as well as determining when to ascend hiearchy while parsing.
        self.indent_level = 0
        # The logical lines of code belonging to this node alone (this does
        # not include the logical lines of code for its children).
        self.logical_loc = 0

    def total_logical_loc(self):
        """Get the total logical lines of code for this node and all of its
        children.

        Returns:
            int: The sum of the logical lines of code for this node and its
                children.
        """
        total_loc = self.logical_loc
        total_loc += sum([kid.total_logical_loc() for kid in self.children])
        return total_loc

    def num_of_type(self, filter_node_type):
        """Returns the number of nodes, including this node and all of its
        children, of the given type.

        Arguments:
            filter_node_type(NodeType): The node type

        Returns:
            int: The number of nodes including this node of the given type.
        """
        number_of_type = 0
        if self.node_type == filter_node_type:
            number_of_type += 1
        for kid in self.children:
            number_of_type += kid.num_of_type(filter_node_type)
        return number_of_type

    def total_logical_loc_of_type(self, filter_node_type):
        """Returns the total logical lines of code within elements of the given
        type. This count includes their children.

        Arguments:
            filter_node_type(NodeType): The node type

        Returns:
            int: The total logical LOC within elements of the given type.
        """
        if self.node_type == filter_node_type:
            return self.total_logical_loc()
        logical_loc = 0
        for kid in self.children:
            logical_loc += kid.total_logical_loc_of_type(filter_node_type)
        return logical_loc


class SingleFileCounter(object):
    """Count the total logical lines of code in a single source file."""

    def __init__(self, file_path):
        """Initialize.

        Arguments:
            file_path(basestring): The path to the Python source file to count.
        """
        self.file_path = file_path
        self.root_node = CountTree(
            name=module_file_from_path(file_path)
        )

    def execute(self):
        """Parse te tokens from the given file and return a count tree.

        Returns:
            CountTree: The tree structure with parsed results.
        """
        with open(self.file_path, 'r') as count_file:
            tokens = tokenize.generate_tokens(count_file.readline)
            current_context = self.root_node
            for token in tokens:
                current_context = self.parse_token(token, current_context)

        return self.root_node

    def parse_token(self, token, node):
        """Parses the given token returning the updated context node.

        Arguments:
            token(tuple): The parsed token
            node(CountTree): The current counting node

        Returns:
            CountTree: The updated counting node or a new counting node
        """
        token_type = token[0]
        token_value = token[1]

        # If we have just started a comment
        if token_type == tokenize.COMMENT:
            # Update node state
            node.in_comment = True
        # If we have reached the end of a comment
        elif node.in_comment and token_type == tokenize.NL:
            # Update node state
            node.in_comment = False
        # If we have reached the end of a line we were parsing
        elif token_type == tokenize.NEWLINE:
            # If we're inside a docstring, do not count this line
            if node.in_docstring:
                node.in_docstring = False
            else:
                node.logical_loc += 1
        # If we're inside a string check if it is a docstring
        elif token_type == tokenize.STRING:
            if token_value.startswith('"""') or token_value.startswith("'''"):
                node.in_docstring = True
        # If we're in a named element, determine its type
        elif token_type == tokenize.NAME:
            if token_value in ('def', 'class'):
                new_node = CountTree(parent=node)
                node.children.append(new_node)
                if token_value == 'class':
                    new_node.node_type = CountTree.NodeType.Class
                elif node.node_type == CountTree.NodeType.Class:
                    new_node.node_type = CountTree.NodeType.ClassMethod
                else:
                    new_node.node_type = CountTree.NodeType.Function
                return new_node
            # Otherwise, this is the class, class method, or function name
            elif not node.name:
                node.name = token_value
        # Track the indent level to determine if we're changing scope
        elif token_type == tokenize.INDENT:
            node.indent_level += 1
        elif token_type == tokenize.DEDENT:
            node.indent_level -= 1
            # If we've left the current context, switch to parent context
            if node.parent and node.indent_level == 0:
                return node.parent

        return node
