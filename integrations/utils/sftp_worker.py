import pysftp
import logging
import sys
import datetime
import os

from integrations.utils.gcp_worker import GcpWorker


class SftpWorker:
    def __init__(self, host : str, username : str, password : str):
        self.host = host
        self.username = username
        self.password = password

    def upload_file(self, destination_dir, local_path, remote_path):
        """
        Copies a file between the local host and the remote host.
        :param destination_dir: (str|None) – Default: None - remotepath to temporarily make the current directory
        :param local_path (str) – the local path and filename
        :param remote_path (str) – the remote path, else the remote pwd and filename is used.
        :return: (obj) SFTPAttributes containing attributes about the given file
        :raises: IOError – if remote_path doesn’t exist
                 OSError – if local_path doesn’t exist
        """
        logging.info('Uploading local file {} to {} on stfp server'.format(
            local_path, remote_path))
        try:

            with pysftp.Connection(host=self.host,
                                   username=self.username,
                                   password=self.password) as sftp:
                with sftp.cd(destination_dir):
                    sftp.put(localpath=local_path, remotepath=remote_path)
            sftp.close()

        except Exception as e:
            logging.info('Exception occurred {}'.format(e))
            logging.critical(sys.exc_info()[0])
            raise

    def mkdir(self, remote_dir):
        """
        Create a directory named remote_dir
        :param remote_dir: (str) – directory to create`
        :return: None
        """
        logging.info('Creating {} directory in sftp server'.format(remote_dir))
        try:
            with pysftp.Connection(host=self.host,
                                   username=self.username,
                                   password=self.password) as sftp:
                sftp.mkdir(remote_dir)

        except Exception as e:
            logging.info('Exception occurred {}'.format(e))
            logging.critical(sys.exc_info()[0])
            raise

    def transfer(self, destination_path : str):
        logging.info('Starting transfer stage')
        gcp_worker = GcpWorker()
        current_ts = str(datetime.datetime.utcnow().isoformat())
        destination_dir = '-'.join(['etl/salesforce/encrypted', current_ts])
        self.mkdir(destination_dir)
        for (dir_path, _, filename) in os.walk('/tmp/encrypted/'):
            for name in filename:
                if name.endswith('.gpg'):
                    logging.info('Uploading {} to sftp server'.format(name))
                    self.upload_file(destination_dir=destination_dir,
                                     local_path=os.path.join(dir_path, name),
                                     remote_path=name)
                    gcp_worker.upload_blob(source_file_name=os.path.join(dir_path, name),
                                               destination_blob_name=name)