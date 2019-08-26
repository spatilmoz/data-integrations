import pysftp
import logging
import sys
import os

from integrations.connectors.Storage.secrets_storage import config as _config

logger = logging.getLogger(__name__)


class LocalConfig(object):
    def __init__(self):
        pass

    def __getattr__(self, attr):
        return _config[attr]


config = LocalConfig()


def upload_file(destination_dir, local_path, remote_path):
    """
    Copies a file between the local host and the remote host.
    :param destination_dir: (str|None) – Default: None - remotepath to temporarily make the current directory
    :param local_path (str) – the local path and filename
    :param remote_path (str) – the remote path, else the remote pwd and filename is used.
    :return: (obj) SFTPAttributes containing attributes about the given file
    :raises: IOError – if remote_path doesn’t exist
             OSError – if local_path doesn’t exist
    """
    logger.info('Uploading local file {} to {} on stfp server'.format(
        local_path, remote_path))
    try:

        with pysftp.Connection(host=config.sftp.get('host'),
                               username=config.sftp.get('username'),
                               password=config.sftp.get('password')) as sftp:
            with sftp.cd(destination_dir):
                sftp.put(localpath=local_path, remotepath=remote_path)
        sftp.close()

    except Exception as e:
        logger.info('Exception occurred {}'.format(e))
        logger.critical(sys.exc_info()[0])
        raise


def mkdir(remote_dir):
    """
    Create a directory named remote_dir
    :param remote_dir: (str) – directory to create`
    :return: None
    """
    logger.info('Creating {} directory in sftp server'.format(remote_dir))
    try:
        with pysftp.Connection(host=config.sftp.get('host'),
                               username=config.sftp.get('username'),
                               password=config.sftp.get('password')) as sftp:
            sftp.mkdir(remote_dir)

    except Exception as e:
        logger.info('Exception occurred {}'.format(e))
        logger.critical(sys.exc_info()[0])
        raise
