import pandas as pd
import logging
import sys

from google.cloud import storage
from integrations.connectors.Storage.secrets_storage import config as _config


class LocalConfig(object):

    def __init__(self):
        pass

    def __getattr__(self, attr):
        return _config[attr]


class StorageClient(object):

    def __init__(self):
        """
        Client for interacting with the Google Cloud Storage API.
           Bases: google.cloud.client.ClientWithProject
           Client to bundle configuration needed for API requests.
           If you don't specify credentials when constructing the client, the
           client library will look for credentials in the environment.
        """

        self.storage = storage.Client()
        self.config = LocalConfig()
        self.logger = logging.getLogger(__name__)

    def list_blobs(self, prefix=None, delimiter=None):
        """
        Return an iterator used to find blobs in the bucket.
        :param prefix (str) – (Optional) prefix used to filter blobs.
        :param delimiter (str) – (Optional) Delimiter, used with prefix to emulate hierarchy.
        :return: Iterator of all Blob in this bucket matching the arguments.
        """
        blobs = self.storage.list_blobs(self.config.storage.get('bucket'), prefix=prefix, delimiter=delimiter)
        return blobs

    def download_blob(self, blob_name):
        """
        Download the contents of this blob into a file-like object.
        :param blob_name - A file name to which to write the blob's data.
        :return: Local path to where the blob has been written to.
        """
        bucket = self.storage.get_bucket(self.config.storage.get('bucket'))
        blob = bucket.get_blob(blob_name)
        with open('/tmp/{}'.format(blob_name), 'wb') as file_obj:
            blob.download_to_file(file_obj)
        return '/tmp/{}'.format(blob_name)

    def upload_blob(self, source_file_name, destination_blob_name):
        """
        Upload this blob’s contents from the content of a named file.
        :param source_file_name: (str) – The path to the file.
        :param destination_blob_name: Location in the bucket where to upload.
        :return: None
        """
        bucket = self.storage.get_bucket(self.config.storage.get('bucket'))
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        self.logger.info('File {} uploaded to {}.'.format(
            source_file_name,
            destination_blob_name))

    def compose(self, sources, table):
        """
        Concatenate source blobs into this one.
        :param sources (list of filenames) – filenames whose contents will be composed into this blob.
        :param table: The name of the table from which the files came from when exporting.
        :return: None, composed files written to the configured bucket on gs.
        """

        try:
            combined_csv = pd.concat([pd.read_csv('gs://{}/{}'.format(self.config.storage.get('bucket'), f),
                                                  header=0) for f in sources])
            combined_csv.to_csv("gs://{}/{}_composed_{}.csv".format(
                self.config.storage.get('bucket'),
                self.config.storage.get('dataset'),
                table),
                index=False,
                encoding='utf-8-sig')
        except Exception as e:
            self.logger.info('Exception occurred {}'.format(e))
            self.logger.critical(sys.exc_info()[0])
            raise

    def delete_blob(self, blob_name):
        """
        Deletes a blob from the current bucket.
        :param blob_name: (str) – A blob name to delete.
        :return: None
        :raises: google.cloud.exceptions.NotFound (to suppress the exception, call delete_blobs,
        passing a no-op on_error callback, e.g.:
        """
        bucket = self.storage.get_bucket(self.config.storage.get('bucket'))
        blob = bucket.blob(blob_name)
        blob.delete()
        self.logger.info('Blob {} deleted.'.format(blob_name))
