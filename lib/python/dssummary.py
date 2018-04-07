import sys, re



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
    cmd = "aws s3 ls --recursive --summarize {0}".format(loc)
    os.system(cmd)
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
#     ... TO BE INTEGRATED ...
#         if (-f $loc) {
#             $nfiles = 1;
#             $nbytes = -s $loc;
#             $found = 1;
#         } elsif (-d $loc) {
#             # cd /my-path
#             # find my-project/ -type f | xargs wc -c
#             # find my-project/ -type f | wc -l
#             my $dir = File::Spec->rel2abs($loc);
#             $dir =~ s#/+$##;    # remove trailing slashes
#             my ($name,$path) = fileparse($dir);
#             chdir $path || die "could not chdir";
#             my @filelist = `find $name -path $name/.snapshot -prune -o -type f -print`;
#             chomp @filelist;
# 
#             $nbytes = 0;
#             foreach my $f (@filelist) {
#                $nbytes += -s $f;
#             }
# 
#             $nfiles = scalar @filelist;
#             $found = 1;
#       } elsif (! -e $loc) {
#           $found = 0;
#       } else {
#           die "file type not supported\n";
#       }
    return (nbytes, nfiles, errmessage)


# loc argument to this function will be of the form:
# - s3://my-bucket/my-dataset
# - /my-abs-path/my-dataset
# - tbd - verify functionality of relative paths
def summary(loc):
    "summarize dataset in nbytes/nfiles"
    if (re.match("s3://", loc)  or  re.match("S3://", loc)):
        (nbytes, nfiles, errmessage) = _summarize_s3(loc)
    else:
        (nbytes, nfiles, errmessage) = _summarize_local_path(loc)

    if (nbytes >= 0  and nfiles >= 0):
        sizestr_dec = hrunits.getSizeStringBytesDecimal(nbytes)
        sizestr_bin = hrunits.getSizeStringBytesBinary(nbytes)
        print("{0}  ({1}, {2})  {3}  {4}".format(nbytes, sizestr_dec, sizestr_bin, nfiles, loc))
    else:
        if (len(errmessage) == 0):
            errmessage = "--failed-reason-unknown--"
        print("{0}  {1}".format(errmessage, loc))
    return
