########################################################################
# ds_opts.py
########################################################################
import sys, os, argparse



def show_usage(prog, errorstr):
    if (len(errorstr) > 0):
        print("ERROR:  {}".format(errorstr))
    print("usage:  {} summary <dir>|<s3prefix> [...]".format(prog))


def process_args():

    options = { 'prog' : os.path.basename(sys.argv[0]) }
    if (len(sys.argv) == 1):
        show_usage(options['prog'], "")
        sys.exit(0)

    options['mode'] = sys.argv[1]
    del sys.argv[1];
    if (options['mode'] not in ['summary', 'normalize', 'flatten-links', 'pack', 'check']):
        show_usage(options['prog'], "mode '{}' not recognized".format(mode))
        sys.exit(1)

    parser = argparse.ArgumentParser(prog = "{} <mode>".format(options['prog']))
    group  = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose",
                       help="show verbose output",
                       action="count")
    group.add_argument("-q", "--quiet",
                       help="minimize output",
                       action="store_true")
    parser.add_argument("-r", "--recursive",
                        help="recursive",
                        action="store_true")
    parser.add_argument("--remove",
                        help="remove if pack succeeds",
                        action="store_true")
    (parsed_args, options['targets']) = parser.parse_known_args()

    if (parsed_args.verbose is not None):
        options['verbose']   = parsed_args.verbose
    else:
        options['verbose']   = 0
    if (parsed_args.quiet):
        options['verbose']   = -1
    if (parsed_args.recursive):
        options['recursive'] = True
    else:
        options['recursive'] = False
    if (parsed_args.remove):
        options['remove']    = True
    else:
        options['remove']    = False

    return options
