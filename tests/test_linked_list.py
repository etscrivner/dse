# -*- coding: utf-8 -*-
import unittest

from lib import linked_list


class BaseLinkedListTestCase(unittest.TestCase):
    def setUp(self):
        super(BaseLinkedListTestCase, self).setUp()
        self.lst = linked_list.LinkedList()    


class TestIsEmpty(BaseLinkedListTestCase):
    def test_should_initially_return_true(self):
        self.assertTrue(self.lst.is_empty())

    def test_should_return_false_after_insert(self):
        self.lst.insert(1)
        self.assertFalse(self.lst.is_empty())


class TestInsert(BaseLinkedListTestCase):
    def test_should_contain_value_after_insert(self):
        self.assertNotIn(1, self.lst)
        self.lst.insert(1)
        self.assertFalse(self.lst.is_empty())
        self.assertIn(1, self.lst)

    def test_should_correctly_insert_values_in_order(self):
        self.lst.insert(1)
        self.lst.insert(2)
        self.lst.insert(3)
        self.assertEqual([1, 2, 3], list(self.lst))
