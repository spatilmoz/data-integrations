import gnupg
import logging
import sys
import pandas as pd
import io
import os


class GpgWorker:
    """
    Wrapper for handling interactions with GnuPG, including keyfile import, encryption and decryption.
    Raises: A RuntimeError with explanation message if there is a problem invoking GnuPG.
    """
    def __init__(self, public_key_url: str, encrypted_dir: str):
        self.public_key_url = public_key_url
        self.encrypted_dir = encrypted_dir
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
        self.gpg.recv_keys(self.public_key_url)
        self.keys = self.gpg.list_keys()

    def encrypt(self, blob_name):
        """
        Encrypt data in a file (or file-like object)
        :param blob_name: The name of the blob to be written in output directory
        :return: If encryption succeeded, the returned object's ok attribute is set to True.
        Otherwise, the returned object's ok attribute is set to False and its status attribute
        (a message string) provides more information as to the reason for failure
        (for example, 'invalid recipient' or 'key expired').
        """
        df = pd.read_csv(os.path.join(self.encrypted_dir, blob_name))
        buf = io.StringIO()
        df.to_csv(buf, encoding='utf-8')

        try:
            status = self.gpg.encrypt_file(
                buf,
                self.keys.fingerprints[0],
                armor=True,
                always_trust=True,
                output='/tmp/{}.gpg'.format(blob_name)
            )
            self.logger.info("OK: {}".format(status.ok))
            self.logger.info("STDERR: {}".format(status.stderr))
        except Exception as e:
            self.logger.info('Exception occurred {}'.format(e))
            self.logger.critical(sys.exc_info()[0])
            raise