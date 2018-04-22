########################################################################
# ds_check.py
########################################################################
import sys, os, re
import subprocess



def single_check(loc):
    sys.stderr.write("--not-yet-implemented--\n")
    exit(1)


def execute_check(targets):
    if (len(targets) != 0):
        for loc in targets:
            single_check(loc)
    else:
        print("no targets specified")
