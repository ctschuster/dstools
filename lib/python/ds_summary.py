########################################################################
# ds_summary.py
########################################################################
import sys, os, re
import subprocess

import hrunits



def _summarize_s3(loc):
    "compute aggregate size of files for S3 prefix"

    # Earlier implementation used s3cmd tools:
    # %   s3cmd du s3://my-bucket/my-project
    # >>>   73852450544 70 objects s3://my-bucket/my-project

    # Current implementation uses awscli tools:
    # %   aws s3 ls --recursive --summarize s3://my-bucket/my-project
    # >>> Total Objects: 26
    # >>>    Total Size: 383037453399

    (nbytes, nfiles, errmessage) = (-1, -1, "")
    errmessage = "--not-yet-implemented--"

#   cmd = "aws s3 ls --recursive --summarize {0}".format(loc)
#   os.system(cmd)
# ..... WORKING HERE ....
#     my @alloutput = `$cmd`;
#     if (!$?) {
#         # >>> Total Objects: 26
#         # >>>    Total Size: 383037453399
#         my $out1 = $alloutput[$#alloutput-1];    chomp $out1;
#         my $out2 = $alloutput[$#alloutput];      chomp $out2;
#         $nfiles = [split /:\s+/, $out1]->[1];
#         $nbytes = [split /:\s+/, $out2]->[1];
#     }
#     $found = 1;
    return (nbytes, nfiles, errmessage)


def _summarize_local_path(loc):
    "compute aggregate size of files for local server path"
    (nbytes, nfiles, errmessage) = (-1, -1, "")
    if (not os.path.exists(loc)):
        errmessage = "--not-found--"
    elif (os.path.islink(loc)):
        errmessage = "--non-standard-file-type--"
    elif (os.path.isfile(loc)):
        nfiles = 1
        nbytes = os.path.getsize(loc)
    elif (os.path.isdir(loc)):
        absdir = os.path.abspath(loc)
        findproc = subprocess.Popen(["find",absdir,"-type","f"], stdout=subprocess.PIPE)
        output = findproc.communicate()[0].splitlines()
        findproc.wait()
        nbytes = 0
        nfiles = 0
        for file in output:
            nbytes += os.path.getsize(file)
            nfiles += 1
    else:
        errmessage = "--non-standard-file-type--"
    return (nbytes, nfiles, errmessage)


# loc argument to this function will be of the form:
# - /my-abs-path/my-dataset        (relative paths supported)
# - s3://my-bucket/my-dataset
def single_summary(loc):
    "summarize dataset in nbytes/nfiles"
    if (re.match("s3://", loc)  or  re.match("S3://", loc)):
        (nbytes, nfiles, errmessage) = _summarize_s3(loc)
    else:
        loc    = os.path.normpath(loc)
        (nbytes, nfiles, errmessage) = _summarize_local_path(loc)

    if (not os.path.isabs(loc)):
        wd     = os.getcwd()
        absloc = os.path.abspath(loc)
        locstr = "{0} ({1}, relative to {2})".format(absloc, loc, wd)
    else:
        locstr = loc

    if (nbytes >= 0  and nfiles >= 0):
        sizestr_dec = hrunits.getSizeStringBytesDecimal(nbytes)
        sizestr_bin = hrunits.getSizeStringBytesBinary(nbytes)
        print("{0}  ({1}, {2})  {3}  {4}".format(nbytes, sizestr_dec, sizestr_bin, nfiles, locstr))
    else:
        if (len(errmessage) == 0):
            errmessage = "--failed-reason-unknown--"
        print("{0}  {1}".format(errmessage, loc))
    return



def execute_summary(targets):
    if (len(targets) != 0):
        for loc in targets:
            single_summary(loc)
    else:
        print("no targets specified")
