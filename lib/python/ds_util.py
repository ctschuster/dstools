########################################################################
# ds_util.py
########################################################################
import sys, os, re
from datetime import datetime



# generate date/time in ISO8601 format
def now_timestamp():
    "current timestamp string - compact"
    date = datetime.now()
    return date.__format__('%Y%m%dT%H%M%S')


# generate date/time in ISO8601 format
def now_timestamp_pretty():
    "current timestamp string - pretty"
    date = datetime.now()
    return date.__format__('%Y-%m-%dT%H:%M:%S')


def touchfile(path):
    with open(path, 'a'):
        os.utime(path, None)


def show_output(output, *, indent="    "):
    for line in output:
        print("{0}{1}".format(indent, line))


# DESIGN BUG: consider behavior for destination being a directory/link
# DESIGN BUG/CONSIDERATION: os.rename() may not work between file systems  ??
def rename(src, dst, *, force=False, verbose=0):
    "utility to rename file"
    if (not os.path.exists(src)):
        raise FileNotFoundError
    if (os.path.exists(dst)):
        if (os.path.isdir(dst)  or  os.path.islink(dst)):
            blocked  = True
            qualtest = "  (conflict - blocked by directory or link)"
        elif (not force):
            blocked  = True
            qualtest = "  (conflict - blocked by file)"
        else:
            blocked  = False
            qualtest = "  (overwriting)"
    else:
        blocked = False
        qualtest = ""

    srcdir  = os.path.dirname(src)
    srcbase = os.path.basename(src)
    dstdir  = os.path.dirname(dst)
    dstbase = os.path.basename(dst)

    if (verbose > 0):
        actionstr = "===>" if (not blocked) else "=X=>"
        if (srcdir == dstdir):
            dir = srcdir if (len(srcdir) > 0) else "."
            print("{0}:  '{1}' {2} '{3}'{4}"
                  .format(dir, srcbase, actionstr, dstbase, qualtest))
        else:
            print("'{0}' {1} '{2}'{3}"
                  .format(src, actionstr, dst, qualtest))

    if (not blocked):
        if (os.path.exists(dst)):
            os.unlink(dst)
        os.rename(src, dst)
        return True
    return False


def normalize_name(namestr):
    "takes a filename (w/o path) and returns a 'cleaner' name"
    # apply lower case:
    namestr = namestr.lower()
    # remove leading / trailing spaces and hyphenate mid-string spaces:
    namestr = "-".join(namestr.strip().split())
    # remove non-standard-characters, allow only alpha, digits, !, -, _, ., *, ', (, and )
    p = re.compile('[^a-zA-Z0-9!\-_.\*\'\(\)]')
    namestr = p.sub('', namestr)
    return namestr
