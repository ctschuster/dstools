#!/usr/bin/env python3

import sys, io, os, tempfile
import unittest
from shutil import rmtree

import ds_normalize



def touchfile(path):
    with open(path, 'a'):
        os.utime(path, None)

class test_ds_normalize(unittest.TestCase):
    """
    Tests for ds_normalize
    """

    def test_normalize_name(self):
        "string rewrite mechanism (non-file)"
        # basic space handling test:
        input = "     abc    123    "
        result = ds_normalize.normalize_entry_name(input)
        self.assertEqual(result, "abc-123")

        # test pass-through of allowed special characters:     !, -, _, ., *, ', (, and ) 
        input = "brown-fox.lazy_dog.!*\'().txt"
        result = ds_normalize.normalize_entry_name(input)
        self.assertEqual(result, input)

    def test_normalize_single(self):
        "test single file normalization"
        testdir = tempfile.mkdtemp()

        file1         = "{}/   1Bc  540(3)   ".format(testdir)
        file1expected = "{}/1bc-540(3)".format(testdir)
        touchfile(file1)
        ds_normalize.normalize_single_file(file1)
        self.assertEqual(os.path.exists(file1),         False)
        self.assertEqual(os.path.exists(file1expected), True)

        file2         = "{}/normal-file.txt".format(testdir)
        touchfile(file2)
        ds_normalize.normalize_single_file(file2)
        self.assertEqual(os.path.exists(file2),         True)

        dir1          = "{}/dir with crazy spacing and chars@".format(testdir)
        dir1expected  = "{}/dir-with-crazy-spacing-and-chars".format(testdir)
        os.mkdir(dir1)
        ds_normalize.normalize_single_file(dir1)
        self.assertEqual(os.path.exists(dir1),          False)
        self.assertEqual(os.path.exists(dir1expected),  True)

        dir2          = "{}/normal-dir".format(testdir)
        os.mkdir(dir2)
        ds_normalize.normalize_single_file(dir2)
        self.assertEqual(os.path.exists(dir2),          True)

        # cleanup testing dir
        rmtree(testdir)

    def test_normalize_recursive(self):
        "test recursive normalization"
        testdir = tempfile.mkdtemp()

        dir1         = "{}/first 1st/ second 2nd/tier#3/ next4@".format(testdir)
        dir1expected = "{}/first-1st/second-2nd/tier3/next4".format(testdir)
        os.makedirs(dir1)
        file1 = "{}/ y: 1Bc ^ & 540(3)   ".format(dir1)
        file2 = "{}/ z ? 2Bc ^ & 540(3) +-X  ".format(dir1)
        touchfile(file1)
        touchfile(file2)
        file1expected = "{}/y-1bc---540(3)".format(dir1expected)
        file2expected = "{}/z--2bc---540(3)--x".format(dir1expected)
        ds_normalize.normalize_recursive(testdir)
        self.assertEqual(os.path.exists(file1),         False)
        self.assertEqual(os.path.exists(file2),         False)
        self.assertEqual(os.path.exists(file1expected), True)
        self.assertEqual(os.path.exists(file2expected), True)

        # cleanup testing dir
        rmtree(testdir)

    def test_non_overwrite(self):
        "test non-overwrite"
        testdir = tempfile.mkdtemp()

        file1 = "{}/MyFile1.txt".format(testdir)
        file2 = "{}/myfile1.txt".format(testdir)
        touchfile(file1)
        touchfile(file2)
        ds_normalize.normalize_recursive(testdir)
        self.assertEqual(os.path.exists(file1),         True)
        self.assertEqual(os.path.exists(file2),         True)

        # cleanup testing dir
        rmtree(testdir)


if __name__ == '__main__':
    unittest.main()
