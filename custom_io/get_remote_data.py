def _copy_remote_file(filepath):
    """
    'Private' function that copies a remote file to /tmp/remote_data
    for use in get remote data

    Keyword Arguments:
    filepath -- the path of the file with username@hostname

    Paul J. Gierz, Sun Feb 15 13:52:38 2015

    """
    # --------------------------------------------------------------------------------
    # KNOWN ISSUES:
    #
    # BUG: This function copies to /tmp/remote_data, which might not
    # be available on all computers, depending on the /tmp/ folder
    # settings.
    #     |==> Paul J. Gierz, Sun Feb 15 14:24:39 2015
    # --------------------------------------------------------------------------------

    import os
    import sys
    import paramiko
    if not os.path.exists('/tmp/remote_data'):
        os.makedirs('/tmp/remote_data')
    if not os.path.exists('/tmp/remote_data/'+os.path.basename(filepath)):
        user = filepath.split(':')[0].split('@')[0]
        host = filepath.split(':')[0].split('@')[1]
        rfile = filepath.split(':')[1]
        # FIXME: This function only works if .ssh/id_rsa exists and is properly configured                
        privatekeyfile = os.path.expanduser('~/.ssh/id_rsa')
        mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, pkey=mykey)
        sftp = client.open_sftp()
        sftp.get(rfile, '/tmp/remote_data/'+os.path.basename(filepath))
        sftp.close()
        client.close()
        pre_s = "Copied"
    else:
        pre_s = "Loaded from /tmp/remote_data/"
    return pre_s, '/tmp/remote_data/'+os.path.basename(filepath)


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

    #--------------------------------------------------------------------------------
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
    # due to ssh transfers
    # 2) Support for non nc files
    # 3) Checking a local datasystem first to see if this file already
    # exists somewhere to prevent needless copying
    # 4) The info statement printing could be cleaner
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
    import os, sys
    from scipy.io import netcdf
    if time:
        now = time.time()
    print "Trying to load ".ljust(40) \
          +print_colors.WARNING("{f}").format(f=os.path.basename(filepath)).ljust(100)
    if not copy_to_local:
        # We wish to split the filepath to get the username, hostname, and
        # path on the remote machine.
        user = filepath.split(':')[0].split('@')[0]
        host = filepath.split(':')[0].split('@')[1]
        rfile = filepath.split(':')[1]
        # FIXME: This function only works if .ssh/id_rsa exists and is properly configured                
        privatekeyfile = os.path.expanduser('~/.ssh/id_rsa')
        mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, pkey=mykey)
        sftp = client.open_sftp()
        fileObject = sftp.file(rfile)
        file = netcdf.netcdf_file(fileObject)
        pre_s = "Loaded from "+host
    else:
        pre_s, fileObject = _copy_remote_file(filepath)
        file = netcdf.netcdf_file(fileObject)        
    if time:
        print pre_s.ljust(40) \
        +print_colors.OKGREEN("{filepath}").format(filepath=os.path.basename(filepath)).ljust(100) \
        +" in ".rjust(0) \
        +print_colors.OKBLUE("{time}").format(time=round(time.time()-now)) \
        +" seconds"
    if info:
        s = print_colors.HEADER("#"*30+" INFO of "+os.path.basename(filepath)+" "+"#"*30)
        print s
        print "Variables: \n"
        for k, v in file.variables.iteritems():
            print k, ":  dimensions -"+str(v.dimensions)+" shape - "+str(v.shape)
        print "Dimensions: \n"
        print file.dimensions
        print print_colors.HEADER("#"*len(s))
        
    return file
