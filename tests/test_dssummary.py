#!/usr/bin/env python3

import sys, io, tempfile
import unittest

import dssummary



class TestDssummary(unittest.TestCase):
    """
    Test encoding of small sizes up to and around the 1000-1024 range
    """

    def test_dssummary(self):
        backup = sys.stdout
        sys.stdout = io.StringIO()     # capture output
        dssummary.single_summary("no-such-file")
        out = sys.stdout.getvalue() # release output
        sys.stdout.close()  # close the stream 
        sys.stdout = backup # restore original stdout
        result = out.splitlines()[0].split()[0]
        self.assertEqual(result, "--not-found--")



if __name__ == '__main__':
    unittest.main()
