import gnupg
import logging
import sys
import pandas as pd
import io
import os

from integrations.utils.gcp_worker import GcpWorker


class GpgWorker(object):
    public_key_url = None
    key_id = None
    encrypted_dir = None
    bucket = None

    """
    Wrapper for handling interactions with GnuPG, including keyfile import, encryption and decryption.
    Raises: A RuntimeError with explanation message if there is a problem invoking GnuPG.
    """
    def __init__(self, public_key_url : str, key_id : str, encrypted_dir : str, bucket : str):
        self.public_key_url = public_key_url
        self.key_id = key_id
        self.encrypted_dir = encrypted_dir
        self.bucket = bucket
        self.gpg = gnupg.GPG()
        self.keys = None
        self.logger = logging.getLogger(__name__)
        self.import_keys()

    def import_keys(self):
        """
        Import keys from a keyserver. List the keys currently in the keyring.
        Fetch keyids (str) - Each keyids argument should be a string containing a keyid to request
        Fetch keyserver (str) - The keyserver to request the keyids from.
        :return: None
        """
        self.logger.info('Importing keys')
        self.gpg.recv_keys(self.public_key_url,
                           self.key_id)
        self.keys = self.gpg.list_keys()

    def encrypt(self, blob_name):
        """
        Encrypt data in a file (or file-like object)
        :param blob_name: The name of the blob to be written in output directory
        :return: If encryption succeeded, the returned object’s ok attribute is set to True.
        Otherwise, the returned object’s ok attribute is set to False and its status attribute
        (a message string) provides more information as to the reason for failure
        (for example, 'invalid recipient' or 'key expired').
        """
        #df = pd.read_csv('gs://{}/{}'.format(self.bucket, blob_name))
        df = pd.read_csv('/tmp/{}'.format(blob_name))
        buf = io.StringIO()
        df.to_csv(buf, encoding='utf-8')

        try:
            status = self.gpg.encrypt_file(
                buf,
                self.keys.fingerprints[0],
                armor=True,
                always_trust=True,
                output='/tmp/{}.gpg'.format(blob_name)
                #output='{}/{}.gpg'.format(self.encrypted_dir, blob_name)
            )
            self.logger.info("OK: {}".format(status.ok))
            self.logger.info("STDERR: {}".format(status.stderr))
        except Exception as e:
            self.logger.info('Exception occurred {}'.format(e))
            self.logger.critical(sys.exc_info()[0])
            raise

    def encrypt_all(self, prefix : str):
        storage_client = GcpWorker()
        self.import_keys()
        for blob in storage_client.list_blobs(prefix=prefix):
            self.encrypt(blob.name)