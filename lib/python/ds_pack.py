########################################################################
# ds_pack.py
########################################################################
import sys, os, re
import socket
import subprocess
import ds_summary
import ds_util



def execute_pack(options):
    def _now():
        return ds_util.timestamp_iso8601_now()


    def _remove(loc):
        if (options['verbose'] > 0):
            print("deleting {}".format(loc))
        temploc = "{0}-DELETEME-{1}".format(loc, _now())
        os.rename(loc, temploc)
        subprocess.call(["/bin/rm", "-fr", temploc])


    def _packit(ds):
        def _pack_step1(dsdict):
            "generate header info"
            print("[{0}]  Dataset:  {1}".format(_now(), dsdict['ds']))
            if (not os.path.isabs(dsdict['ds'])):
                print("[{0}]  AbsPath:  {1}".format(_now(), dsdict['absds']))
            print("[{0}]  Server:   {1}".format(_now(), socket.gethostname()))

#           subprocess.call(["df", "-hP", dsdict['ds']], stdout=sys.stdout)
            print("[{0}]  File system info:".format(_now()))
            (ret,output) = subprocess.getstatusoutput("df -hP {}".format(dsdict['ds']))
            print(output)

            print("[{0}]  Dataset summary:".format(_now()))
            ds_summary.single_summary(dsdict['ds'])


        def _pack_step2(dsdict):
            "generate tarball"
            print("[{0}]  Generating tarball:  {1}".format(_now(), dsdict['tarfile']))
            # ( cd $dir && tar cvfz - --exclude-backups --exclude=.snapshot $opts ${base} ) > $tarfile 2>> $logfile
            # ret1=$?
            # if [ $ret1 = 0 ]; then
            #     status=success
            # else
            #     status=failure
            # fi
            # echo "[`date +'%F %T'`]  Tarball completion: $status" | tee -a $logfile

        def _pack_step3(dsdict):
            "show tarball contents"
            print("[{0}]  Generating file list".format(_now()))
            # tar tvfz $tarfile 2>&1 >> $logfile
            # ret2=$?
            # if [ $ret2 = 0 ]; then
            #     status=success
            # else
            #     status=failure
            # fi
            # echo "[`date +'%F %T'`]  Tarball listing: $status" | tee -a $logfile


        def _pack_step4(dsdict):
            "contruct checksum & closing info"
            print("[{0}]  Generating checksum:".format(_now()))
            # md5=`md5sum $tarfile | awk '{print $1}'`
            # size=`ls -l $tarfile | awk '{print $5}'`
            # if [ $ret1 = 0 -a $ret2 = 0 -a $size -gt 0 ]; then
            #     summary=PASS
            # else
            #     summary=FAIL
            # fi
            # echo "[`date +'%F %T'`]  Generating checksum/summary info" | tee -a $logfile
            # echo "[`date +'%F %T'`]  MD5:    ${md5}" | tee -a $logfile
            # echo "[`date +'%F %T'`]  Size:   ${size} (bytes)" | tee -a $logfile
            # echo "[`date +'%F %T'`]  Summary $tarfile - ${summary}" | tee -a $logfile

        def _pack_step5(dsdict):
            "postprocessing - permissions & remove if specified"
            print("step5:")
            # if [ "$USER" = "root" ]; then
            #     chmod ug+rw,o+r $tarfile $logfile
            #     chgrp TGAC $tarfile $logfile
            # fi
            # autodelete()

        if (not os.path.islink(ds) and os.path.isdir(ds)):
            base = os.path.basename(ds)
            tarfile = "{}.tgz".format(base)
            logfile = "{}.log".format(base)
            for targetfile in [
                tarfile,
                logfile,
                "{}.log.gz".format(base)
            ]:
                if (os.path.exists(targetfile)):
                    print("cannot pack - conflicting target file '{}'".format(targetfile))
                    raise FileExistsError

            save_stdout = sys.stdout
            sys.stdout = open(logfile, 'w')
            dsdict = {
                'ds'       : ds,
                'base'     : base,
                'tarfile'  : tarfile,
                'logfile'  : logfile,
                'absds'    : os.path.abspath(ds)
            }
            _pack_step1(dsdict)
            _pack_step2(dsdict)
            _pack_step3(dsdict)
            _pack_step4(dsdict)
            _pack_step5(dsdict)
            sys.stdout.close()
            sys.stdout = save_stdout
        else:
            print("non-compliant source location '{}'".format(ds))
            raise NotADirectoryError
        return


    if (len(options['targets']) != 0):
        for loc in options['targets']:
            _packit(os.path.normpath(loc))
    else:
        print("no targets specified")
    return




# ########################################################################
# # Option:
# #    -i   Allow tarball to succeed even if read errors occurred, such as
# #         from read permission errors.  [By default, this option is off,
# #         so any unreadable content will be treated as a failure.]
# ########################################################################
# # Example:
# #    user@host:/curr/dir>>  ds-pack /path/mydata
# #
# # Creates the following output:
# #    /curr/dir/mydata.tgz - tarball of contents /path/mydata
# #                           files have relative path:
# #                               mydata/file1
# #                               mydata/file2
# #    /curr/dir/mydata.log - start / stop time info, exit status,
# #                         - output of tar command (list of files & errors)
# ########################################################################

# # In case there is a tarballing process which completes when we tried to break
# # out and removed the tgz & log, do not auto-delete.  See author ctschu for more
# # on reasoning.  ctschu / 2017-09-25
# if [ "$summary" = "PASS"  -a  $autoremoveifpass -gt 0  -a  -e $tarfile  -a  -e $logfile ]; then
