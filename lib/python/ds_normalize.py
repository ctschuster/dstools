########################################################################
# ds_normalize.py
########################################################################
import sys, os, re, errno
import argparse
import subprocess

import ds_util



def execute_normalize(options):
    def normalize_single_file(loc, verbose=0):
        if (os.path.exists(loc)):
            mydir     = os.path.dirname(loc)
            myfile    = os.path.basename(loc)
            myfilenew = ds_util.normalize_name(myfile)
            if (myfile != myfilenew):
                newfile = myfilenew if (len(mydir) == 0) else "{0}/{1}".format(mydir, myfilenew)
                renamed = ds_util.rename(loc, newfile, verbose=verbose, force=False)
                if (renamed):
                    return newfile
            return loc
        return

    def normalize_recursive(loc):
        newloc = normalize_single_file(loc)
        if (newloc  and  not os.path.islink(newloc)  and  os.path.isdir(newloc)):
            filesindir = os.listdir(newloc)
            for file in filesindir:
                normalize_recursive("{0}/{1}".format(newloc,file))

    if (len(options['targets']) != 0):
        for loc in options['targets']:
            loc = os.path.normpath(loc)
            if (not os.path.exists(loc)):
                if (options['verbose']>=0):
                    print("not found - '{0}'".format(loc))
                raise FileNotFoundError
            if(options['recursive']):
                normalize_recursive(loc)
            else:
                normalize_single_file(loc)
    else:
        print("no targets specified")
