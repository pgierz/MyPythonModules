def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def _check_for_local_file(name, path):
    import os
    """Checks if the file exists locally somewhere first, even if we
    aren't checking in the "copy_to_local" directory.

    Keyword Arguments:
    filepath -- the filepath

    Paul J. Gierz, Sun Jul 19 11:43:35 2015
    """
    # print "Looking for:", name, path
    # print "---------------------------------"
    foundname = False
    for r, d, f in os.walk(path):
        # print r, d, f
        if name in f:
            foundname = os.path.join(r, name)
            break
        else:
            # foundname = False
            pass  # foundname will still be false, not reassigned...
    return foundname


def _refile_local_file_correctly(filepath, from_where):
    import os
    # Check if this directory exists locally:
    if not os.path.exists("/Users/pgierz/Research/" + '/'.join(filepath.split("/")[4:-1])):
        os.makedirs(
            "/Users/pgierz/Research/" + '/'.join(filepath.split("/")[4:-1]))
    # TODO: Check if the run is registered in ~/.all_runs:
    os.rename(from_where + os.path.basename(filepath),
              "/Users/pgierz/Research/" + '/'.join(filepath.split("/")[4:]))
    return "/Users/pgierz/Research/" + '/'.join(filepath.split("/")[4:-1]) + "/", os.path.basename(filepath)


def _copy_remote_file(filepath, remote_dump="/tmp/remote_data/"):
    """
    'Private' function that copies a remote file to /tmp/remote_data
    for use in get remote data

    Keyword Arguments:
    filepath -- the path of the file with username@hostname

    Paul J. Gierz, Sun Feb 15 13:52:38 2015

    """
    # --------------------------------------------------------------------------------
    # CHANGELOG:
    #
    # FEATURE: There is now a progressbar when copying to the local file system! Hooray!
    # Paul J. Gierz, Sat Jun 27 12:58:13 2015
    #
    # FEATURE: Now, we look for the file in multiple local locations
    # based upon a file in ${HOME}/.all_runs.
    # Paul J. Gierz, Sun Jul 19 14:08:28 2015
    #
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # KNOWN ISSUES:
    #
    # BUG: This function copies to /tmp/remote_data by default, which
    # might not be available on all computers, depending on the /tmp/
    # folder settings.  |==> Paul J. Gierz, Sun Feb 15 14:24:39 2015
    # --------------------------------------------------------------------------------
    import os
    import paramiko
    import progressbar
    if not os.path.exists(remote_dump):
        os.makedirs(remote_dump)
    if not os.path.exists(remote_dump + os.path.basename(filepath)):
        for r in [line.strip() for line in open(os.path.expanduser("~/.all_runs.dat")) if "#" not in line]:
            test = _check_for_local_file(os.path.basename(filepath), r)
            if test:
                break
        if not test:
            print "Couldn't find the file in any organized way, copying again..."
            user = filepath.split(':')[0].split('@')[0]
            host = filepath.split(':')[0].split('@')[1]
            rfile = filepath.split(':')[1]
            print "Trying to copy: ", filepath
            # FIXME: This function only works if .ssh/id_rsa exists and is properly
            # configured
            privatekeyfile = os.path.expanduser('~/.ssh/id_rsa')
            mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, username=user, pkey=mykey)
            sftp = client.open_sftp()
            info_rfile = sftp.stat(rfile)
            widgetlist = [rfile.split("/")[-1], ' (' + sizeof_fmt(info_rfile.st_size) + ')', progressbar.Percentage(
            ), ' ', progressbar.FileTransferSpeed(), ' ', progressbar.Bar(), ' ', progressbar.ETA(), ' ', progressbar.Timer()]
            pbar = progressbar.ProgressBar(
                widgets=widgetlist, maxval=info_rfile.st_size)

            def _progress_cb(done, total):
                if pbar.start_time is None:
                    pbar.start()
                pbar.update(done)
            print "starting transfer..."
            sftp.get(
                rfile, remote_dump + os.path.basename(filepath),
                callback=_progress_cb)
            pbar.finish()
            sftp.close()
            client.close()
            pre_s = "Copied " + \
                os.path.basename(filepath) + " to " + remote_dump
            remote_dump, new_filepath = _refile_local_file_correctly(
                filepath, remote_dump)
        else:
            pre_s = "Found " + os.path.basename(filepath) + " in " + test
            remote_dump, new_filepath = "/".join(
                test.split("/")[:-1]) + "/", os.path.basename(test)

    else:
        pre_s = "Loaded from " + remote_dump
        remote_dump, new_filepath = _refile_local_file_correctly(
            filepath, remote_dump)
    return pre_s, remote_dump + new_filepath


def _check_for_local(name, path):
    import os
    """Checks if the file exists locally somewhere first, even if we
    aren't checking in the "copy_to_local" directory.

    Keyword Arguments:
    filepath -- the filepath

    Paul J. Gierz, Sun Jul 19 11:43:35 2015
    """
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
        else:
            return False


def get_remote_data(filepath, time=False, info=False, copy_to_local=False):
    """
    A paramiko wrapper that gets file from a remote computer. Parses
    hostname from filepath. Works only for netcdf files!

    Keyword Arguments:
    filepath         -- the path of the file with hosname.
    time             -- print time required for loading(default False)
    info             -- print some information about the file after loading
                        (default False)
    copy_to_local    -- copies file to local /tmp/remote_data/ and checks
                        if this file already exists there (default False)

    Example:
    >>> get_remote_data('pgierz@rayo3:/csys/paleo2/pgierz/GR30s.nc')

    Paul J. Gierz, Sat Feb 14 14:20:43 2015
    """

    # --------------------------------------------------------------------------------
    # CHANGELOG:
    #
    # First port of this function to the repository that will be
    # shared with the AWI Paleodyn group later. I have also added
    # options to print out some file information and the amount of
    # time required during transfer
    #
    # Paul J. Gierz, Sat Feb 14 14:21:19 2015
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # ROADMAP:
    #
    # A couple of things could be added:
    # 1) option to copy to some local folder to avoid long load times
    # due to ssh transfers -- DONE!
    # 2) Support for non nc files
    # 3) Checking a local datasystem first to see if this file already
    # exists somewhere to prevent needless copying
    # 4) The info statement printing could be cleaner
    # 5) hostname check...
    #
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # KNOWN ISSUES:
    #
    # BUG: For some reason, this function breaks horribly when I do
    # not directly return the netcdf file. I suspect that it has
    # something to do with the namespaces/scopes: The main program
    # probably doesn't know about the ssh-socket. Or something...I'm
    # not even remotely close to what you would call a network
    # protocol expert; so that's an "educated guess" Since we
    # generally work with netcdf data exclusively, I will simply use
    # this note as a caution for anyone trying to open other data
    # files with this function. I'll also probably post something on
    # an online forum later on, maybe someone can help!
    #
    # BUG: This function currently depends on the ~/.ssh/id_rsa
    # file. It would be elegant if the user did not necessearily have
    # to have this file in place (some people prefer to type their
    # password often, I guess). By not having this file in place, the
    # entire function breaks needlessly
    #     |==> Paul J. Gierz, Sat Feb 14 15:12:24 2015
    # --------------------------------------------------------------------------------

    # Import stuff from your own library:
    from UI_Stuff import print_colors
    if time:
        import time
    import paramiko
    import os
    from scipy.io import netcdf
    if time:
        now = time.time()
        print "Trying to load ".ljust(40) \
            + \
            print_colors.WARNING("{f}").format(
                f=os.path.basename(filepath)).ljust(100)

    if ":" not in filepath:
        # local file
        file = netcdf.netcdf_file(filepath)
    else:
        if not copy_to_local:
            # We wish to split the filepath to get the username, hostname, and
            # path on the remote machine.
            user = filepath.split(':')[0].split('@')[0]
            host = filepath.split(':')[0].split('@')[1]
            rfile = filepath.split(':')[1]
            # FIXME: This function only works if .ssh/id_rsa exists and is
            # properly configured
            privatekeyfile = os.path.expanduser('~/.ssh/id_rsa')
            mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, username=user, pkey=mykey)
            sftp = client.open_sftp()
            fileObject = sftp.file(rfile)
            file = netcdf.netcdf_file(fileObject)
            pre_s = "Loaded from " + host
        else:
            if type(copy_to_local) is str:
                pre_s, fileObject = _copy_remote_file(
                    filepath, remote_dump=copy_to_local)
            else:
                pre_s, fileObject = _copy_remote_file(filepath)
            file = netcdf.netcdf_file(fileObject)
    if time:
        print pre_s.ljust(40) \
            + print_colors.OKGREEN("{filepath}").format(filepath=os.path.basename(filepath)).ljust(100) \
            + " in ".rjust(0) \
            + print_colors.OKBLUE("{time}").format(time=round(time.time() - now)) \
            + " seconds"
    if info:
        s = print_colors.HEADER(
            "#" * 30 + " INFO of " + os.path.basename(filepath) + " " + "#" * 30)
        print s
        print "Variables: \n"
        for k, v in file.variables.iteritems():
            print k, ":  dimensions -" + str(v.dimensions) + " shape - " + str(v.shape)
        print "Dimensions: \n"
        print file.dimensions
        print print_colors.HEADER("#" * len(s))
    return file
