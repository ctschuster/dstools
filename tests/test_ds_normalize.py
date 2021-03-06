#!/usr/bin/env python3
########################################################################
# test_ds_normalize.py
########################################################################

import sys, io, os, tempfile
import unittest
from shutil import rmtree

import ds_util
import ds_normalize


# BUG - Testing deficiency: Should test the output in verbose modes 0 & 1 & 2


def test_exception_FNF_thrown(self, recursive, verbose, file):
    try:
        ds_normalize.execute_normalize([file], recursive=recursive, verbose=verbose)
    except FileNotFoundError:
        pass
    except Exception as e:
        self.fail('Unexpected exception raised:', e)
    else:
        self.fail('ExpectedException not raised')



class test_ds_normalize(unittest.TestCase):
    """
    Tests for ds_normalize
    """

    def test_normalize_single(self):
        "test non-recursive normalization"
        testdir = tempfile.mkdtemp()

        file1         = "{}/   1Bc  540(3)   ".format(testdir)
        file1expected = "{}/1bc-540(3)".format(testdir)
        ds_util.touchfile(file1)
        ds_normalize.execute_normalize([file1], recursive=False, verbose=0)
        self.assertEqual(os.path.exists(file1),         False)
        self.assertEqual(os.path.exists(file1expected), True)

        file2         = "{}/normal-file.txt".format(testdir)
        ds_util.touchfile(file2)
        ds_normalize.execute_normalize([file2], recursive=False, verbose=0)
        self.assertEqual(os.path.exists(file2),         True)

        dir1            = "{}/dir with crazy spacing and chars@".format(testdir)
        dir1expected    = "{}/dir-with-crazy-spacing-and-chars".format(testdir)
        file1_in_dir1    = "{}/normal-file.txt".format(dir1)
        file1_in_dir1exp = "{}/normal-file.txt".format(dir1expected)
        file2_in_dir1    = "{}/file to convert.txt".format(dir1)
        file2_in_dir1exp = "{}/file to convert.txt".format(dir1expected)
        os.mkdir(dir1)
        ds_util.touchfile(file1_in_dir1)
        ds_util.touchfile(file2_in_dir1)
        ds_normalize.execute_normalize([dir1], recursive=False, verbose=0)
        self.assertEqual(os.path.exists(dir1),          False)
        self.assertEqual(os.path.exists(dir1expected),  True)
        self.assertEqual(os.path.exists(file1_in_dir1),    False)
        self.assertEqual(os.path.exists(file1_in_dir1exp), True)
        self.assertEqual(os.path.exists(file2_in_dir1),    False)
        self.assertEqual(os.path.exists(file2_in_dir1exp), True)
        dir2          = "{}/normal-dir".format(testdir)
        os.mkdir(dir2)
        ds_normalize.execute_normalize([dir2], recursive=False, verbose=0)
        self.assertEqual(os.path.exists(dir2),          True)

        rmtree(testdir)


    def test_normalize_recursive(self):
        "test recursive normalization"
        testdir = tempfile.mkdtemp()

        dir1         = "{}/first 1st/ second 2nd/tier#3/ next4@".format(testdir)
        dir1expected = "{}/first-1st/second-2nd/tier3/next4".format(testdir)
        os.makedirs(dir1)
        file1 = "{}/ y: 1Bc ^ & 540(3)   ".format(dir1)
        file2 = "{}/ z ? 2Bc ^ & 540(3) +-X  ".format(dir1)
        ds_util.touchfile(file1)
        ds_util.touchfile(file2)
        file1expected = "{}/y-1bc---540(3)".format(dir1expected)
        file2expected = "{}/z--2bc---540(3)--x".format(dir1expected)
        ds_normalize.execute_normalize([testdir], recursive=True, verbose=0)
        #raise FileNotFoundError
        self.assertEqual(os.path.exists(file1),         False)
        self.assertEqual(os.path.exists(file2),         False)
        self.assertEqual(os.path.exists(file1expected), True)
        self.assertEqual(os.path.exists(file2expected), True)

        rmtree(testdir)


    def test_non_overwrite(self):
        "test non-overwrite"
        testdir = tempfile.mkdtemp()

        file1 = "{}/MyFile1.txt".format(testdir)
        file2 = "{}/myfile1.txt".format(testdir)
        file3 = "{}/my file.txt".format(testdir)
        ds_util.touchfile(file1)
        ds_util.touchfile(file2)
        ds_util.touchfile(file3)
        ds_normalize.execute_normalize([file1, file2, file3], recursive=False, verbose=0)
        self.assertEqual(os.path.exists(file1),         True)
        self.assertEqual(os.path.exists(file2),         True)
        self.assertEqual(os.path.exists(file3),         False)

        rmtree(testdir)


    def test_no_path(self):
        lastdir = os.getcwd()
        testdir = tempfile.mkdtemp()
        os.chdir(testdir)
        testfile = "abc def |*# 123"
        expected = "abc-def-*-123"
        ds_util.touchfile(testfile)
        ds_normalize.execute_normalize([testfile], recursive=False, verbose=0)
        self.assertEqual(os.path.exists(testfile), False)
        self.assertEqual(os.path.exists(expected), True)
        os.chdir(lastdir)
        rmtree(testdir)


    def test_missing_target(self):
        testdir = tempfile.mkdtemp()

        dir1 = "{}/dir1".format(testdir)
        os.makedirs(dir1)
        nonfile1 = "no-such-file"
        nonfile2 = "{}/no-such-file.txt".format(testdir)
        nonfile3 = "{}/no-such-file.txt".format(dir1)
        nondir1  = "{}/no-such-dir".format(testdir)

        test_exception_FNF_thrown(self, False, -1, nonfile1 )
        test_exception_FNF_thrown(self, False, -1, nonfile2 )
        test_exception_FNF_thrown(self, False, -1, nonfile3 )
        test_exception_FNF_thrown(self, False, -1, nondir1  )
        test_exception_FNF_thrown(self, True,  -1, nonfile1 )
        test_exception_FNF_thrown(self, True,  -1, nonfile2 )
        test_exception_FNF_thrown(self, True,  -1, nonfile3 )
        test_exception_FNF_thrown(self, True,  -1, nondir1  )

        rmtree(testdir)



if __name__ == '__main__':
    unittest.main()
