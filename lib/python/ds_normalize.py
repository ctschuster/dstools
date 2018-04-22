########################################################################
# ds_normalize.py
########################################################################
import sys, os, re, errno
import argparse
import subprocess

import ds_util



def execute_normalize(targets, *, verbose=0, recursive=False):
    def normalize_single_file(loc):
        # Pre-condition:  **loc** _must_ exist (file/directory/link/whatever)
        mydir     = os.path.dirname(loc)
        myfile    = os.path.basename(loc)
        myfilenew = ds_util.normalize_name(myfile)
        if (myfile != myfilenew):
            newfile = myfilenew if (len(mydir) == 0) else "{0}/{1}".format(mydir, myfilenew)
            renamed = ds_util.rename(loc, newfile, verbose=verbose, force=False)
            if (renamed):
                return newfile
        return loc

    def normalize_recursive(loc):
        newloc = normalize_single_file(loc)
        if (newloc  and  not os.path.islink(newloc)  and  os.path.isdir(newloc)):
            filesindir = os.listdir(newloc)
            for file in filesindir:
                normalize_recursive("{0}/{1}".format(newloc,file))

    if (len(targets) != 0):
        for loc in targets:
            loc = os.path.normpath(loc)
            if (not os.path.exists(loc)  and  not os.path.islink(loc)):
                if (verbose>=0):
                    sys.stderr.write("not found - '{0}'\n".format(loc))
                raise FileNotFoundError
            if (recursive):
                normalize_recursive(loc)
            else:
                normalize_single_file(loc)
    else:
        print("no targets specified")
