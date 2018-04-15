########################################################################
# ds_check.py
########################################################################
import sys, os, re
import subprocess



def single_check(loc):
    return "--not-yet-implemented--"


def execute_check(loc):
    if (len(modeargs) != 0):
        for loc in modeargs:
            single_check(loc)
    else:
        print("no targets specified")
    return
