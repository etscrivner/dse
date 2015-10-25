# -*- coding: utf-8 -*-
"""
    lib.linked_list
    ~~~~~~~~~~~~~~~
    A simple linked list implementation.


"""


class LinkedList(object):
    """Implements a linked list."""

    # pylint: disable=too-few-public-methods
    class Node(object):
        """Represents a node in a linked list"""

        def __init__(self, value, before, after):
            """Initialize.

            Arguments:
                value(mixed): The value of the node
                before(Node or None): The node before this one in the list.
                after(Node or None): The node after this one in the list.
            """
            self.value = value
            self.before = before
            self.after = after

    def __init__(self):
        self.first = None
        self.last = None

    def is_empty(self):
        """Indicates whether or not this linked list is empty.

        Returns:
            bool: True if empty, false otherwise.
        """
        return self.first is None and self.last is None

    def insert(self, value):
        """Insert a value into this linked list.

        Arguments:
            value(mixed): The value to be inserted.
        """
        new_node = self.Node(value, self.last, None)
        if self.last:
            self.last.after = new_node
            self.last = new_node
        else:
            self.first = new_node
            self.last = new_node

    def __iter__(self):
        """Iterate through the items in this linked list.

        Returns:
            mixed: The next value in the linked list.
        """
        current_node = self.first
        while current_node:
            yield current_node.value
            current_node = current_node.after
