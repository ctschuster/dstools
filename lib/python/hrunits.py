########################################################################
# hrutils.py
########################################################################
# Reference:
#     https://en.wikipedia.org/wiki/Kilobyte
########################################################################

# intended on to be used with base = 1000 or 1024
def _computeSizeOrder(nbytes,base,symbols):
    "compute size / order of magnitude"
    order = 0
    size  = nbytes
    while(size>=base  and  order<=7):
        order += 1
        size /= base

    unit = symbols[order]
    if (order==0  or  size>=100):
        numstr = "{0:0.0f}".format(size)
    elif (size>=10):
        numstr = "{0:0.1f}".format(size)
    else:
        numstr = "{0:0.2f}".format(size)
    sizestr = "{0} {1}".format(numstr, unit)

    return(sizestr)

def getSizeStringBytesBinary(nbytes):
    "human readable byte count (based 1024)"
    symbols = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
    str = _computeSizeOrder(nbytes, 1024, symbols)
    return str

def getSizeStringBytesDecimal(nbytes):
    "human readable byte count (based 1000)"
    symbols = ["B", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    str = _computeSizeOrder(nbytes, 1000, symbols)
    return str

def getSizeStringBitsBinary(nbytes):
    "human readable bit count (based 1024)"
    symbols = ["bit", "Kibit", "Mibit", "Gibit", "Tibit", "Pibit", "Eibit", "Zibit", "Yibit"]
    str = _computeSizeOrder(nbytes, 1024, symbols)
    return str

def getSizeStringBitsDecimal(nbytes):
    "human readable bit count (based 1000)"
    symbols = ["bit", "kbit", "Mbit", "Gbit", "Tbit", "Pbit", "Ebit", "Zbit", "Ybit"]
    str = _computeSizeOrder(nbytes, 1000, symbols)
    return str
