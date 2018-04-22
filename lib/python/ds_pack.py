########################################################################
# ds_pack.py
########################################################################
import sys, os, re
import socket
import subprocess
import ds_summary
import ds_util



def execute_pack(targets, *, verbose=0):
    def _now():
        return ds_util.now_timestamp_pretty()


    def _remove(loc):
        if (verbose > 0):
            print("deleting {}".format(loc))
        temploc = "{0}-DELETEME-{1}".format(loc, _now())
        os.rename(loc, temploc)
        subprocess.call(["/bin/rm", "-fr", temploc])


    def _packit(ds):
        ret1=-1
        ret2=-1
        def _pack_step1(dsdict):
            "generate header info"
            print("[{0}]  Dataset:  {1}".format(_now(), dsdict['ds']))
            if (not os.path.isabs(dsdict['ds'])):
                print("[{0}]  AbsPath:  {1}".format(_now(), dsdict['absds']))
            print("[{0}]  Server:   {1}".format(_now(), socket.gethostname()))

            print("[{0}]  File system info:".format(_now()))
            (ret,output) = subprocess.getstatusoutput("df -hP {}".format(dsdict['ds']))
            ds_util.show_output(output.splitlines())

            print("[{0}]  Dataset summary:".format(_now()))
            sys.stdout.write("    ")
            ds_summary.single_summary(dsdict['ds'])

        def _pack_step2(dsdict):
            "generate tarball"
            print("[{0}]  Generating tarball:  {1}".format(_now(), dsdict['tarfile']))
            savedir = os.getcwd()
            tarfilewpath = os.path.abspath("{}/{}".format(savedir, dsdict['tarfile']))
            dir  = os.path.dirname(dsdict['absds'])
            base = os.path.basename(dsdict['absds'])
            os.chdir(dir)
            cmd = [ "tar", "cvfz", tarfilewpath, "--exclude-backups", "--exclude=.snapshot", base]
            ret1 = ds_util.run_command(cmd)
            #BUG: save stdout to logfile!
            os.chdir(savedir)
            status_string = 'success' if (ret1 == 0) else 'failure'
            print("[{0}]  Tarball completion:  {1}".format(_now(), status_string))

        def _pack_step3(dsdict):
            "show tarball contents"
            print("[{0}]  Generating file list".format(_now()))
            # tar tvfz $tarfile 2>&1 >> $logfile
            ret2=0
            status_string = 'success' if (ret2 == 0) else 'failure'
            print("[{0}]  Tarball listing:  {1}".format(_now(), status_string))

        def _pack_step4(dsdict):
            "contruct checksum & closing info"
            print("[{0}]  Generating checksum:".format(_now()))
            # md5=`md5sum $tarfile | awk '{print $1}'`
            size      = os.path.getsize(dsdict['tarfile'])
            pf_string = 'PASS' if (ret1 == 0  and  ret2 == 0  and  size > 0) else 'FAIL'
            # echo "[`date +'%F %T'`]  Generating checksum/summary info" | tee -a $logfile
            # echo "[`date +'%F %T'`]  MD5:    ${md5}" | tee -a $logfile

            print("[{0}]  Size:   {1} bytes".format(_now(), -1))
            print("[{0}]  Summary {1} - {2}".format(_now(), dsdict['tarfile'], pf_string))

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


    if (len(targets) != 0):
        for loc in targets:
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
