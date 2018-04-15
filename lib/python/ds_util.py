########################################################################
# ds_util.py
########################################################################
import sys, os, re



def rename(src, dst, options = {}):
    "file rename utility, w/ text output"
    # BUG: consider case of destination being a directory
    if (not os.path.exists(src)):
        raise FileNotFoundError
    if (os.path.exists(dst)):
        if (not('force' in options)  or  not options['force']):
            blocked  = True
            qualtest = "  (name conflict - blocked)"
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

    if (('verbose' in options  and  options['verbose']>0)):
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


def touchfile(path):
    with open(path, 'a'):
        os.utime(path, None)


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
