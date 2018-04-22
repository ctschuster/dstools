#!/usr/bin/env python3
########################################################################
# test_ds_util.py
########################################################################

import sys, io
import unittest

import ds_util


# BUG: no tests for ds_util.touchfile()
# BUG: no tests for ds_util.rename()


class normalize_name_tests(unittest.TestCase):
    """
    Tests for ds_util.normalize_name()
    """

    def test_normalize_name(self):
        "string rewrite mechanism (non-file)"
        # basic space handling test:
        input = "     abc    123    "
        result = ds_util.normalize_name(input)
        self.assertEqual(result, "abc-123")

        # test pass-through of allowed special characters:     !, -, _, ., *, ', (, and )
        input = "brown-fox.lazy_dog.!*\'().txt"
        result = ds_util.normalize_name(input)
        self.assertEqual(result, input)


class run_command_tests(unittest.TestCase):
    """
    Tests for ds_util.run_command()
    """
    def test_normalize_name(self):
        # test return values:
        ret = ds_util.run_command(["/bin/true"])
        self.assertEqual(ret, 0)
        # test return values:
        ret = ds_util.run_command(["/bin/false"])
        self.assertEqual(ret, 1)


if __name__ == '__main__':
    unittest.main()
