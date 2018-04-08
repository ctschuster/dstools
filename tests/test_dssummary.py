#!/usr/bin/env python3

import sys, io, os, tempfile
import unittest

import dssummary



def run_dssummary(file):
    backup = sys.stdout
    sys.stdout = io.StringIO()
    dssummary.single_summary(file)
    out = sys.stdout.getvalue()
    sys.stdout.close()
    sys.stdout = backup
    tokens = out.splitlines()[0]
    return (tokens.split()[0], tokens.split()[5], tokens.split()[6])



class TestDssummary(unittest.TestCase):
    """
    Tests for dssummary
    """

    def test_dssummary(self):
        backup = sys.stdout
        sys.stdout = io.StringIO()                 # capture output
        dssummary.single_summary("no-such-file")
        out = sys.stdout.getvalue()                # release output
        sys.stdout.close()                         # close the stream
        sys.stdout = backup                        # restore original stdout
        result = out.splitlines()[0].split()[0]
        self.assertEqual(result, "--not-found--")

        testdir = tempfile.mkdtemp()
        (nbytes, nfiles, name) = run_dssummary(testdir)
        self.assertEqual(int(nbytes), 0)
        self.assertEqual(int(nfiles), 0)
        self.assertEqual(name, testdir)

        subdir1 = "{0}/{1}".format(testdir,"dir1")
        subdir2 = "{0}/{1}".format(testdir,"dir2")
        os.mkdir(subdir1)
        os.mkdir(subdir2)
        (nbytes, nfiles, name) = run_dssummary(testdir)
        self.assertEqual(int(nbytes), 0)
        self.assertEqual(int(nfiles), 0)
        self.assertEqual(name, testdir)



if __name__ == '__main__':
    unittest.main()
