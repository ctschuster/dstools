########################################################################
# ds_flatten.py
########################################################################
import sys, os, re
import ds_util



def execute_flatten(options):
    def flatten_link(loc):
        if (os.path.islink(loc)):
            mydir     = os.path.dirname(loc)

            src       = os.path.basename(loc)
            src1      = ds_util.normalize_name(src)
            tgt       = os.readlink(loc)
            tgt0      = re.compile('/').sub(' ', tgt)
            tgt1      = ds_util.normalize_name(tgt0)

            linktext  = "linkto" if (os.path.exists(tgt) or os.path.islink(tgt)) else "broken-linkto"

            myfilenew = "{0}__{1}__{2}".format(src1, linktext, tgt1)
            newloc    = "{0}/{1}".format(mydir, myfilenew) if (len(mydir)>0) else myfilenew

            os.unlink(loc)
            ds_util.touchfile(loc)
            ds_util.rename(loc, newloc, { 'verbose' : options['verbose'] })

    def flatten_recursive(loc):
        if (os.path.islink(loc)):
            flatten_link(loc)
        elif (os.path.isdir(loc)):
            filesindir = os.listdir(loc)
            for file in filesindir:
                flatten_recursive("{0}/{1}".format(loc, file))

    if (len(options['targets']) != 0):
        for loc in options['targets']:
            loc = os.path.normpath(loc)
            if (not os.path.exists(loc) and not os.path.islink(loc)):
                if (options['verbose'] >= 0):
                    print("not found - '{0}'".format(loc))
                raise FileNotFoundError
            if(options['recursive']):
                flatten_recursive(loc)
            else:
                flatten_link(loc)
    else:
        print("no targets specified")
