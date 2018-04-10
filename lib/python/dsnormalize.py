import sys, os, re
import subprocess



def normalize_name(tok):
    "returns a 'cleaner' name; use only on filename or single dirname, not a path"
    # apply lower case:
    tok = tok.lower()
    # remove leading / trailing spaces and hyphenate mid-string spaces:
    tok = "-".join(tok.strip().split())
    # remove non-standard-characters, allow only alpha, digits, !, -, _, ., *, ', (, and ) 
    p = re.compile('[^a-zA-Z0-9!\-_.\*\'\(\)]')
    tok = p.sub('', tok)
    return tok

def normalize_entry(loc):
    locnew = normalize_name(loctok)
#   if (loc
    return "--not-yet-implemented--"


def execute_normalize(loc):
    if (len(modeargs) != 0):
        for loc in modeargs:
            normalize_entry(os.path.normpath(loc))
    else:
        print("no targets specified")
    return
