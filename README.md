## DS Tools - tools for managing datasets

### Overview

This toolset is intended to solve some practical problems in managing
bulk data storage.  The tools included will generally be scripts and
should not require any build process.  The goal is to make management
of datasets between unix, s3 and perhaps other storage platforms
simpler and the transfer of data more efficient / reliable /
verifiable.

### Synopsis


### Considerations

This was written based upon a need to deal with issue involving:
 * archiving & long-term storage
 * migration of data
 * treatment of unstructured data
 * tolerating lossy data transfer mechanisms

Driving issues which impacted the design of these tools:
 * data file count
   * high file count tends to slow storage activities
 * portability issues
   * links, hard and soft, are not handled well in the general case
   * simple treatment of filenames to improve portability/usability

### Requirements

These tools have been developed to be used by unix-like shells, so unix,
linux, mac, cygwin.  Software dependencies will include minimal unix
tools, plus heavier weight tools (meaning you might need to install
packages on a minimal system) including:

    perl
    python
    awscli

Note: at this time, the tools presume that all included tools and
dependencies listed above are required to be in the user's path.
