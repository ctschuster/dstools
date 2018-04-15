#!/usr/bin/env python3
########################################################################
# test_ds_util.py
########################################################################

import sys
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



if __name__ == '__main__':
    unittest.main()
