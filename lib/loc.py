# -*- coding: utf-8 -*-
"""
    lib.loc
    ~~~~~~~
    Reusable components for lines of code counting.


    module_file_from_path(): Converts a file system path into a python module
        name.
    CountTree: Tree data structure for storing lines of code (LOC) counts.
    ParsedToken: Abstract of a token parsed from the source file.
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


class ParsedToken(object):
    """Represents a token parsed from a python source file"""

    def __init__(self, token_type, token_value):
        """Initialize.

        Arguments:
            token_type(int): The type of token
            token_value(basestring): The value of the token
        """
        self.token_type = token_type
        self.token_value = token_value

    @classmethod
    def from_token(cls, token_tuple):
        """Creates a new parsed token from the given token tuple.

        Arguments:
            token_tuple(tuple): A tuple of parsed token information

        Returns:
            ParsedToken: A new parsed token instance
        """
        assert token_tuple
        return cls(token_tuple[0], token_tuple[1])

    def is_comment(self):
        """Indicates whether or not this token is a comment.

        Returns:
            bool: True if this token is a comment, False otherwise.
        """
        return self.token_type == tokenize.COMMENT

    def is_newline(self):
        """Indicates whether or not this token is a newline.

        Returns:
            bool: True if this token is a newline, False otherwise
        """
        return self.token_type == tokenize.NEWLINE

    def is_docstring(self):
        """Indicates whether or not the given token value is a docstring.

        Returns:
            bool: True if element is a docstring, False otherwise.
        """
        return (
            self.token_type == tokenize.STRING and
            (self.token_value.startswith('"""') or
             self.token_value.startswith("'''"))
        )

    def is_named_element(self):
        """Indicates whether or not this token is a named element.

        A named element is either a function or class definition or the actual
        name of a defined function or class.

        Returns:
            bool: True if this token is a named element, False otherwise.
        """
        return self.token_type == tokenize.NAME

    def is_end_of_comment(self, node):
        """Indicates whether or not this token represents the end of a comment.

        Argument:
            node(CountTree): The current node in the counting tree

        Returns:
            bool: True if this token represents the end of a comment, False
                otherwise.
        """
        return node.in_comment and self.token_type == tokenize.NL

    def is_element_definition(self):
        """Indicates whether or not this token is an element definition.

        Returns:
            bool: True if the token is an element definition, False otherwise.
        """
        return self.token_value in ('def', 'class')

    def is_indent(self):
        """Indicates whether or not this token is an indent.

        Returns:
            bool: True if this token is an indent, False otherwise.
        """
        return self.token_type == tokenize.INDENT

    def is_dedent(self):
        """Indicates whether or not this token is an dedent.

        Returns:
            bool: True if this token is an dedent, False otherwise.
        """
        return self.token_type == tokenize.DEDENT


class SingleFileCounter(object):
    """Count the total logical lines of code in a single source file.

    This class parses the given python file and counts the logical lines of
    code. In addition, the sizes of various elements are counted and recorded.
    A tree structure containing the counts for the file and its various sub-
    components is then returned.

    Example:

    >>> count_tree = SingleFileCounter('loc.py').execute()
    >>> count_tree.total_logical_loc()
    121
    >>> count_tree.total_logical_loc_of_type(CountTree.NodeType.Class)
    119
    """

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
        """Parse the tokens from the given file and return a count tree.

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
        parsed_token = ParsedToken.from_token(token)

        if parsed_token.is_comment():
            node.in_comment = True
        elif parsed_token.is_end_of_comment(node):
            node.in_comment = False
        elif parsed_token.is_newline():
            return self.handle_end_of_line(node)
        elif parsed_token.is_docstring():
            node.in_docstring = True
        elif parsed_token.is_named_element():
            return self.handle_named_element(node, parsed_token)
        elif parsed_token.is_indent():
            node.indent_level += 1
        elif parsed_token.is_dedent():
            return self.handle_dedent(node)

        return node

    def handle_dedent(self, node):
        """Handle when indentation level for the program changes.

        Arguments:
            node(CountTree): The current counting tree node

        Returns:
            CountTree: The updated counting tree
        """
        node.indent_level -= 1
        # If we've left the current context, switch to parent context
        if node.parent and node.indent_level == 0:
            return node.parent
        return node

    def handle_named_element(self, node, parsed_token):
        """Handle parsing a named element.

        Arguments:
            node(CountTree): The current counting tree node
            parsed_token(ParsedToken): The parsed token

        Returns:
            CountTree: The updated counting tree.
        """
        if parsed_token.is_element_definition():
            return self.handle_element_definition(
                node, parsed_token.token_value
            )
        # Otherwise, this is the class, class method, or function name
        elif not node.name:
            node.name = parsed_token.token_value
        return node

    def handle_end_of_line(self, node):
        """Handle reaching the end of a line.

        Arguments:
            node(CountTree): The current counting tree node
        """
        if node.in_docstring:
            node.in_docstring = False
        else:
            node.logical_loc += 1
        return node

    def handle_element_definition(self, node, token_value):
        """Handle the definition of a class, class method, or function.

        Arguments:
            node(CountTree): The current node in the counting tree
            token_value(basestring): The value of the current token

        Returns:
            CountTree: The new node created for the element
        """
        new_node = CountTree(parent=node)
        node.children.append(new_node)
        if token_value == 'class':
            new_node.node_type = CountTree.NodeType.Class
        elif node.node_type == CountTree.NodeType.Class:
            new_node.node_type = CountTree.NodeType.ClassMethod
        else:
            new_node.node_type = CountTree.NodeType.Function
        return new_node
