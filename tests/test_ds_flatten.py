#!/usr/bin/env python3
########################################################################
# test_ds_flatten.py
########################################################################

import os, sys, re, tempfile
from shutil import rmtree
import unittest

import ds_util
import ds_flatten



class flatten_tests(unittest.TestCase):
    """
    Tests for module 'ds_flatten'
    """

    def test_single(self):
        savedir = os.getcwd()
        testdir = tempfile.mkdtemp()
        os.chdir(testdir)

        ds_util.touchfile('file1')
        ds_util.touchfile('file2')
        ds_util.touchfile('file3')
        file1    = 'file1'                       # simple link
        link1    = 'link1'
        file2    = '{0}/file2'.format(testdir)   # path in link target
        link2    = 'link2'
        file3    = 'file3'                       # indirect link
        indirect = 'indirect'
        link3    = 'link3'
        tgt4     = 'no-such-file'
        link4    = 'link4'

        os.symlink(file1, link1)
        os.symlink(file2, link2)
        os.symlink(file3, indirect)
        os.symlink(indirect, link3)
        os.symlink(tgt4, link4)

        ds_flatten.execute_flatten([testdir])

        self.assertEqual(True, os.path.exists(link1))
        self.assertEqual(True, os.path.exists(link2))
        self.assertEqual(True, os.path.exists(link3))
        self.assertEqual(True, os.path.islink(link4))

        ds_flatten.execute_flatten([link1,link2,link3,link4])

        self.assertEqual(False, os.path.exists(link1))
        self.assertEqual(False, os.path.exists(link2))
        self.assertEqual(False, os.path.exists(link3))
        self.assertEqual(False, os.path.islink(link4))
        self.assertEqual(True,
            os.path.exists("{0}/link1__linkto__file1".format(testdir)))
        file2fmt = re.compile('/').sub(' ', file2)
        file2fmt = ds_util.normalize_name(file2fmt)
        self.assertEqual(True,
            os.path.exists("{0}/link2__linkto__{1}".format(testdir,file2fmt)))
        self.assertEqual(True,
            os.path.exists("{0}/link3__linkto__indirect".format(testdir)))
        self.assertEqual(True,
            os.path.exists("{0}/link4__broken-linkto__{1}".format(testdir,tgt4)))

        os.chdir(savedir)
        rmtree(testdir)

    def test_recursive(self):
        savedir = os.getcwd()
        testdir = tempfile.mkdtemp()
        os.chdir(testdir)

        ds_util.touchfile('file1')
        ds_util.touchfile('file2')
        ds_util.touchfile('file3')
        file1    = 'file1'                       # simple link
        link1    = 'link1'
        file2    = '{0}/file2'.format(testdir)   # path in link target
        link2    = 'link2'
        file3    = 'file3'                       # indirect link
        indirect = 'indirect'
        link3    = 'link3'
        tgt4     = 'no-such-file'
        link4    = 'link4'

        os.symlink(file1, link1)
        os.symlink(file2, link2)
        os.symlink(file3, indirect)
        os.symlink(indirect, link3)
        os.symlink(tgt4, link4)

        ds_flatten.execute_flatten([testdir], recursive=True)

        self.assertEqual(False, os.path.exists(link1))
        self.assertEqual(False, os.path.exists(link2))
        self.assertEqual(False, os.path.exists(link3))
        self.assertEqual(False, os.path.islink(link4))
        self.assertEqual(True,
            os.path.exists("{0}/link1__linkto__file1".format(testdir)))
        file2fmt = re.compile('/').sub(' ', file2)
        file2fmt = ds_util.normalize_name(file2fmt)
        self.assertEqual(True,
            os.path.exists("{0}/link2__linkto__{1}".format(testdir,file2fmt)))
        self.assertEqual(True,
            os.path.exists("{0}/link3__linkto__indirect".format(testdir))
            or
            os.path.exists("{0}/link3__broken-linkto__indirect".format(testdir)))
        self.assertEqual(True,
            os.path.exists("{0}/link4__broken-linkto__{1}".format(testdir,tgt4)))

        os.chdir(savedir)
        rmtree(testdir)



if __name__ == '__main__':
    unittest.main()
