import sys



def show_usage(prog, errorstr):
    if (len(errorstr) > 0):
        print("ERROR:  {}".format(errorstr))
    print("usage:  {} summary <dir>|<s3prefix> [...]".format(prog))
