def _save_fig_locally(path):
    """
    Saves a figure locally before moving it to a remote computer

    Keyword Arguments:
    path -- the path and filename of the file as it should be on the remote host (with user@blah)

    Paul J. Gierz, Tue Apr  7 09:35:09 2015
    """
    # --------------------------------------------------------------------------------
    # CHANGELOG:
    #
    # Paul J. Gierz, Tue Apr  7 09:36:08 2015:
    #     --| Designed function
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # ROADMAP:
    #
    #    Nothing yet
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # KNOWN ISSUES:
    #
    #    None yet
    # --------------------------------------------------------------------------------
    import matplotlib.pyplot as plt
    fname = path.split('/')[-1]
    plt.savefig(fname)


def _delete_fig_locally(path):
    """
    Deletes the saved file locally

    Keyword Arguments:
    path -- the path and filename of the file as it should be on the remote host (with user@blah)

    Paul J. Gierz, Tue Apr  7 09:38:05 2015
    """
    # --------------------------------------------------------------------------------
    # CHANGELOG:
    #
    # Paul J. Gierz, Tue Apr  7 09:38:43 2015
    #    --| Wrote function
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # ROADMAP:
    #
    #    Nothing yet
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # KNOWN ISSUES:
    #
    #    None yet
    # --------------------------------------------------------------------------------

    import os
    os.remove(path.split('/')[-1])
    return None


def _copy_remote_file(path):
    """
    Copies a remote file from the current working directory to the remote path

    Keyword Arguments:
    path -- the path and filename of the file as it should be on the remote host (with user@blah)

    Paul J. Gierz, Tue Apr  7 09:41:58 2015
    """
    # --------------------------------------------------------------------------------
    # CHANGELOG:
    #
    # Paul J. Gierz, Tue Apr  7 09:42:37 2015
    #    --| Wrote function
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # ROADMAP:
    #
    #    None yet
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # KNOWN ISSUES:
    #
    #    None yet
    # --------------------------------------------------------------------------------
    import os
    import paramiko
    lfile = path.split('/')[-1]
    rfile = path.split(':')[1]
    remote_path = os.path.split(path.rstrip('/'))[0].split(':')[-1]
    user = path.split(':')[0].split('@')[0]
    host = path.split(':')[0].split('@')[1]
    # FIXME: This function only works if .ssh/id_rsa exists and is properly configured
    privatekeyfile = os.path.expanduser('~/.ssh/id_rsa')
    mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=user, pkey=mykey)
    sftp = client.open_sftp()
    try:
        sftp.chdir(remote_path)  # Test if remote_path exists
    except IOError:
        sftp.mkdir(remote_path)  # Create remote_path
    sftp.put(lfile, rfile)
    sftp.close()
    client.close()
    return None


def save_file_remotely(path):
    """
    Wraps the other parts up nicely

    Keyword Arguments:
    path -- the path and filename of the file as it should be on the remote host (with user@blah)

    Paul J. Gierz, Tue Apr  7 09:50:51 2015
    """
    # --------------------------------------------------------------------------------
    # CHANGELOG:
    #
    #
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # ROADMAP:
    #
    #
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # KNOWN ISSUES:
    #
    #
    # --------------------------------------------------------------------------------
    _save_fig_locally(path)
    _copy_remote_file(path)
    _delete_fig_locally(path)
