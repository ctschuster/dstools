import sys, os, re, errno
import argparse
import subprocess


# Testing deficiency:
# - Should test the output in verbose modes 0 & 1 & 2


def normalize_entry_name(namestr):
    "returns a 'cleaner' name; use only on filename or single dirname, not a path"
    # apply lower case:
    namestr = namestr.lower()
    # remove leading / trailing spaces and hyphenate mid-string spaces:
    namestr = "-".join(namestr.strip().split())
    # remove non-standard-characters, allow only alpha, digits, !, -, _, ., *, ', (, and )
    p = re.compile('[^a-zA-Z0-9!\-_.\*\'\(\)]')
    namestr = p.sub('', namestr)
    return namestr


def execute_normalize(options):
    def normalize_single_file(loc):
        if (os.path.exists(loc)):
            mydir     = os.path.dirname(loc)
            myfile    = os.path.basename(loc)
            myfilenew = normalize_entry_name(myfile)
            if (myfile != myfilenew):
                newfile = "{0}/{1}".format(mydir, myfilenew)
                if (not os.path.exists(newfile)):
                    if (options['verbosity']==2):
                        print("{0}:  '{1}' ===> '{2}'".format(mydir,myfile,myfilenew))
                    os.rename(loc,newfile)
                    return newfile
                else:
                    if (options['verbosity']>=1):
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
                if (options['verbosity']>=0):
                    print("not found - '{0}'".format(loc))
                raise FileNotFoundError
            if(options['recursive']):
                normalize_recursive(loc)
            else:
                normalize_single_file(loc)
    else:
        print("no targets specified")
    return
