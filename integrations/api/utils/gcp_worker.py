import subprocess
import logging
import sys
from google.cloud import storage


class GcpWorker:

    def __init__(self, bucket: str, dataset: str):
        self.bucket = bucket
        self.dataset = dataset
        self.storage = storage.Client()
        self.logger = logging.getLogger(__name__)

    def list_blobs(self, prefix=None, delimiter=None):
        """
        Return an iterator used to find blobs in the bucket.
        :param prefix (str) – (Optional) prefix used to filter blobs.
        :param delimiter (str) – (Optional) Delimiter, used with prefix to emulate hierarchy.
        :return: Iterator of all Blob in this bucket matching the arguments.
        """
        blobs = self.storage.list_blobs(self.bucket, prefix=prefix, delimiter=delimiter)
        return blobs

    def execute(self, command):
        try:
            p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p_status = p.wait()
            self.logger.info('Command status: {}'.format(p_status))

        except Exception as e:
            self.logger.info('Exception occurred {}'.format(e))
            self.logger.critical(sys.exc_info()[0])
            raise

    def download(self, bucket, table):
        """
        Concatenate source blobs into this one.
        :param bucket: Name of the bucket from which to compose files.
        :param table: The name of the table from which the files came from when exporting.
        :return: None, composed files written to the configured bucket on gs.
        :raises: Exception in case subprocess exists
        """

        try:

            download = "gsutil -m cp -r gs://{}/{}*.csv /tmp".format(bucket, table)
            # Finish downloading all files for table
            self.execute(download)
            self.logger.info('Done downloading files for table {}'.format(table))
            compose = "awk '(NR == 1) || (FNR > 1)' /tmp/{}*.csv | "\
                      "gzip -9c > /tmp/{}.csv.gz".format(table, table)
            # Compose all local files for table
            self.execute(compose)
            self.logger.info('Done composing files for table {}'.format(table))

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
        bucket = self.storage.get_bucket(self.bucket)
        blob = bucket.blob(blob_name)
        blob.delete()
        self.logger.info('Blob {} deleted.'.format(blob_name))
