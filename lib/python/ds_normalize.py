########################################################################
# ds_normalize.py
########################################################################
import sys, os, re, errno
import argparse
import subprocess

import ds_util



def execute_normalize(options):
    def normalize_single_file(loc):
        if (os.path.exists(loc)):
            mydir     = os.path.dirname(loc)
            myfile    = os.path.basename(loc)
            myfilenew = ds_util.normalize_name(myfile)
            if (myfile != myfilenew):
                newfile = "{0}/{1}".format(mydir, myfilenew)
                if (not os.path.exists(newfile)):
                    if (options['verbose']==2):
                        print("{0}:  '{1}' ===> '{2}'".format(mydir,myfile,myfilenew))
                    os.rename(loc,newfile)
                    return newfile
                else:
                    if (options['verbose']>=1):
                        print("{0}:  '{1}' =X=> '{2}'  Collision - target file exists"
                              .format(mydir,myfile,myfilenew))
            return loc

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
