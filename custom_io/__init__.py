#!/usr/bin/env python
# coding: utf-8

##########################################################################
# get_remote_data (New Implementation/Cleaner version)
#
# Paul J. Gierz, Thu Aug 18 15:08:46 2016
##########################################################################

# Imports
import progressbar
import paramiko
import os
import shutil
import custom_io_constants as constants

# Make sure the remote_dump exists
if not os.path.exists(constants.remote_dump):
    os.makedirs(constants.remote_dump)


# Helper Functions
def _sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def _set_up_client(host, user):
    # FIXME: This function only works if .ssh/id_rsa exists and is
    # properly configured
    mykey = paramiko.RSAKey.from_private_key_file(
        os.path.expanduser('~/.ssh/id_rsa'))
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=user, pkey=mykey)
    return client


def _copy_remote_file(rfile, host, client, tmp=False):
    lfile = rfile.replace(constants.replace_path_dict[
                          host], constants.local_experiment_storehouse)
    if os.path.exists(lfile):
        return lfile
    else:
        sftp = client.open_sftp()
        info_rfile = sftp.stat(rfile)
        widgetlist = [rfile.split("/")[-1], ' (' + _sizeof_fmt(info_rfile.st_size) + ')', progressbar.Percentage(
        ), ' ', progressbar.FileTransferSpeed(), ' ', progressbar.Bar(), ' ', progressbar.ETA(), ' ', progressbar.Timer()]
        pbar = progressbar.ProgressBar(
            widgets=widgetlist, maxval=info_rfile.st_size)

        def _progress_cb(done, total):
            if pbar.start_time is None:
                pbar.start()
            pbar.update(done)

        sftp.get(rfile,
                 constants.remote_dump + os.path.basename(rfile),
                 callback=_progress_cb)
        pbar.finish()
        if not tmp:
            path = os.path.dirname(lfile)
            try:
                os.makedirs(path)
            except OSError:
                if not os.path.isdir(path):
                    raise
            shutil.move(constants.remote_dump + "/" + os.path.basename(rfile),
                        lfile)
            return lfile
        else:
            return constants.remote_dump + "/" + os.path.basename(rfile)


# Main Function
def get_remote_data(filepath, copy_to_local=None):
    copy_to_local = copy_to_local and os.path.exists(constants.local_experiment_storehouse)
    user = filepath.split(':')[0].split('@')[0]
    host = filepath.split(':')[0].split('@')[1]
    rfile = filepath.split(':')[1]
    client = _set_up_client(host, user)
    if copy_to_local:
        lfile = _copy_remote_file(rfile, host, client)
    else:
        lfile = _copy_remote_file(rfile, host, client, tmp=True)
    client.close()
    return lfile
