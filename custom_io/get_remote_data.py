def get_remote_data(filepath):
    """
    A paramiko wrapper that gets file from a remote computer. Parses
    hostname from filepath. Works only for netcdf files!

    Arguments:
        filepath -- the path with hostname.

    Example:
        get_remote_data('pgierz@sx8:/sx8/user1/pgierz/testfile.nc')

    Paul J. Gierz
    """
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
    import paramiko
    import os
    from scipy.io import netcdf
    # We wish to split the filepath to get the username, hostname, and
    # path on the remote machine.
    user = filepath.split(':')[0].split('@')[0]
    host = filepath.split(':')[0].split('@')[1]
    rfile = filepath.split(':')[1]
    privatekeyfile = os.path.expanduser('~/.ssh/id_rsa')
    mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=user, pkey=mykey)
    sftp = client.open_sftp()
    fileObject = sftp.file(rfile)
    file = netcdf.netcdf_file(fileObject)
    return file
