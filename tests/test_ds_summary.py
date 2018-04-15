#!/usr/bin/env python3
########################################################################
# test_ds_summary.py
########################################################################

import sys, io, os, tempfile
import unittest
from shutil import rmtree

import ds_summary



def run_ds_summary(file):
    backup = sys.stdout
    sys.stdout = io.StringIO()
    ds_summary.single_summary(file)
    out = sys.stdout.getvalue()
    sys.stdout.close()
    sys.stdout = backup
    tokens = out.splitlines()[0]
    return (tokens.split()[0], tokens.split()[5], tokens.split()[6])



class TestDssummary(unittest.TestCase):
    """
    Tests for ds_summary
    """

    def test_ds_summary(self):
        # test handling of missing files
        backup = sys.stdout
        sys.stdout = io.StringIO()                 # capture output
        ds_summary.single_summary("no-such-file")
        out = sys.stdout.getvalue()                # release output
        sys.stdout.close()                         # close the stream
        sys.stdout = backup                        # restore original stdout
        result = out.splitlines()[0].split()[0]
        self.assertEqual(result, "--not-found--")

        # create a testing area
        testdir = tempfile.mkdtemp()
        (nbytes, nfiles, name) = run_ds_summary(testdir)
        self.assertEqual(int(nbytes), 0)
        self.assertEqual(int(nfiles), 0)
        self.assertEqual(name, testdir)

        # add some misc directories
        subdir1 = "{0}/{1}".format(testdir,"dir1")
        subdir2 = "{0}/{1}".format(testdir,"dir2")
        os.mkdir(subdir1)
        os.mkdir(subdir2)
        (nbytes, nfiles, name) = run_ds_summary(testdir)
        self.assertEqual(int(nbytes), 0)
        self.assertEqual(int(nfiles), 0)
        self.assertEqual(name, testdir)

        # add single file and symlink, test that symlinks are ignored:
        hellofile = "{0}/{1}".format(testdir,"hello.txt")
        text_file = open(hellofile, "w")
        text_file.write("hello world")
        text_file.close()

        stray_symlink = "{0}/{1}".format(testdir,"mysymlink")
        os.symlink(testdir, stray_symlink)

        (nbytes, nfiles, name) = run_ds_summary(testdir)
        self.assertEqual(int(nbytes), 11)
        self.assertEqual(int(nfiles), 1)
        self.assertEqual(name, testdir)

        # test that sym links are rejected:
        backup = sys.stdout
        sys.stdout = io.StringIO()                 # capture output
        ds_summary.single_summary(stray_symlink)
        out = sys.stdout.getvalue()                # release output
        sys.stdout.close()                         # close the stream
        sys.stdout = backup                        # restore original stdout
        result = out.splitlines()[0].split()[0]
        self.assertEqual(result, "--non-standard-file-type--")

        # Test single file
        (nbytes, nfiles, name) = (0,0,0)
        (nbytes, nfiles, name) = run_ds_summary(hellofile)
        self.assertEqual(int(nbytes), 11)
        self.assertEqual(int(nfiles), 1)
        self.assertEqual(name, hellofile)

        # cleanup testing dir
        rmtree(testdir)



if __name__ == '__main__':
    unittest.main()
