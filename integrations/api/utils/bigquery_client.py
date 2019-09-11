import logging
from google.cloud import bigquery


class BigQueryClient:
    def __init__(self):
        self.client = bigquery.Client()
        self.logger = logging.getLogger(__name__)

    def list_tables(self, dataset: str):
        tables = list(self.client.list_tables(dataset))
        return tables

    def extract_table(self, bucket_name: str, dataset_id: str, table_id: str, file_extension: str, location: str):
        filename = table_id + '*.' + file_extension
        destination_uri = "gs://{}/{}".format(bucket_name, filename)
        dataset_ref = self.client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)

        extract_job = self.client.extract_table(
            table_ref,
            destination_uri,
            # Location must match that of the source table.
            location=location,
        )  # API request
        extract_job.result()  # Waits for job to complete.

        self.logger.info("Exported {}.{} to {}".format(dataset_id, table_id, destination_uri))

    def get_dataset(self, dataset_id: str):
        return self.client.get_dataset(dataset_id)

    def delete_table(self, dataset, table_id):
        dataset_ref = self.get_dataset(dataset)
        self.client.delete_table('.'.join([dataset_ref.project,
                                           dataset_ref.dataset_id,
                                           table_id]),
                                 not_found_ok=True)
        self.logger.info('Deleted table {}'.format(table_id))