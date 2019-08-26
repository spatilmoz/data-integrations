import gnupg
import logging
import sys
import pandas as pd
import io
import os

from integrations.connectors.Storage.secrets_storage import config as _config


class LocalConfig(object):
    def __init__(self):
        pass

    def __getattr__(self, attr):
        return _config[attr]


class GPG(object):
    """
    Wrapper for handling interactions with GnuPG, including keyfile import, encryption and decryption.
    Raises: A RuntimeError with explanation message if there is a problem invoking GnuPG.
    """
    def __init__(self):
        self.gpg = gnupg.GPG()
        self.config = LocalConfig()
        self.keys = None
        self.logger = logging.getLogger(__name__)

    def import_keys(self):
        """
        Import keys from a keyserver. List the keys currently in the keyring.
        Fetch keyids (str) - Each keyids argument should be a string containing a keyid to request
        Fetch keyserver (str) - The keyserver to request the keyids from.
        :return: None
        """
        self.logger.info('Importing keys')
        self.gpg.recv_keys(self.config.gpg.get('public_key'),
                           self.config.gpg.get('key_id'))
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
        df = pd.read_csv('gs://{}/{}'.format(self.config.storage.get('bucket'), blob_name))
        buf = io.StringIO()
        df.to_csv(buf, encoding='utf-8')
        directory = self.config.gpg.get('encrypted_dir')
        try:
            if not os.path.exists(directory):
                os.makedirs(directory, mode=777)
                os.chmod(directory, 777)
            status = self.gpg.encrypt_file(
                buf,
                self.keys.fingerprints[0],
                armor=True,
                always_trust=True,
                output='{}/{}.gpg'.format(directory, blob_name)
            )
            self.logger.info("OK: {}".format(status.ok))
            self.logger.info("STDERR: {}".format(status.stderr))
        except Exception as e:
            self.logger.info('Exception occurred {}'.format(e))
            self.logger.critical(sys.exc_info()[0])
            raise
