import sys, os, re
import subprocess



def single_normalize(loc):
    return "--not-yet-implemented--"


def execute_normalize(loc):
    if (len(modeargs) != 0):
        for loc in modeargs:
            single_normalize(loc)
    else:
        print("no targets specified")
    return
