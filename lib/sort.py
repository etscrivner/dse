# -*- coding: utf-8 -*-
"""
    lib.sort
    ~~~~~~~~
    Methods for sorting lists of data.

    merge_sort(): Perform a merge sort of the given list of data.
    merge(): Merge two lists in sorted order.
"""
from lib.integration import is_even


def merge_sort(lst, key=None):
    """Perform a merge sort of the given list of data.

    Arguments:
        lst(list): A list of data.
        key(None or callable): Method passed each item whose result will be
            used for comparison. Default is identity function.

    Returns:
        list: The sorted contents of the list.
    """
    if len(lst) <= 1:
        return lst

    left, right = [], []
    for idx, value in enumerate(lst):
        if is_even(idx):
            left.append(value)
        else:
            right.append(value)

    left = merge_sort(left)
    right = merge_sort(right)
    return merge(left, right)


def merge(left, right, key=None):
    """Merges two lists in sorted order using result of key method for
    comparison.

    Arguments:
        left(list): A list of data.
        right(list): A list of data.
        key(None or callable): Method passed each item whose result will be
            used for comparison. Default is identity function.

    Returns:
        list: The merged list composed of all elements from both lists.
    """
    result = []

    if key is None:
        key = lambda x: x

    while len(left) > 0 and len(right) > 0:
        if key(left) <= key(right):
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))

    result += left
    result += right

    return result
