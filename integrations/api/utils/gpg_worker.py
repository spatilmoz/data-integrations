import gnupg
import logging
import sys
import os

import requests


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
        Import keys from a public url and return the fingerprints associated with it.
        :return: fingerprint associated with the key.
        """
        key_data = requests.get(self.public_key_url).text
        import_result = self.gpg.import_keys(key_data)
        self.gpg.trust_keys(import_result.results[0]['fingerprint'], 'TRUST_ULTIMATE')

    def encrypt(self, blob_name):
        """
        Encrypt data in a file (or file-like object)
        :param blob_name: The name of the blob to be written in output directory
        :return: If encryption succeeded, the returned object's ok attribute is set to True.
        Otherwise, the returned object's ok attribute is set to False and its status attribute
        (a message string) provides more information as to the reason for failure
        (for example, 'invalid recipient' or 'key expired').
        """
        stream = open(os.path.join(self.encrypted_dir, blob_name), 'rb')

        try:
            self.logger.info('Starting encryption of file {}'.format(blob_name))
            status = self.gpg.encrypt_file(
                stream,
                ['info@exacttarget.com'],
                output='/tmp/{}.pgp'.format(blob_name)
            )
            self.logger.info("OK: {}".format(status.ok))
            self.logger.info("STDERR: {}".format(status.stderr))

        except Exception as e:
            self.logger.error('Exception occurred {}'.format(e))
            self.logger.critical(sys.exc_info()[0])
            raise
