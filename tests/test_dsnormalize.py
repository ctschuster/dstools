#!/usr/bin/env python3

import sys, io, os
import unittest

import dsnormalize



class test_dsnormalize(unittest.TestCase):
    """
    Tests for dsnormalize
    """

    def test_normalize_name(self):
        # basic space handling test:
        input = "     abc    123    "
        result = dsnormalize.normalize_name(input)
        self.assertEqual(result, "abc-123")

        # test pass-through of allowed special characters:     !, -, _, ., *, ', (, and ) 
        input = "brown-fox.lazy_dog.!*\'().txt"
        result = dsnormalize.normalize_name(input)
        self.assertEqual(result, input)



if __name__ == '__main__':
    unittest.main()
