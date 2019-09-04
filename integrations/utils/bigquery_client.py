import google.cloud
import logging


class BigQueryClient():
    def __init__(self):
        self.client = google.cloud.bigquery.Client()
        self.logger = logging.getLogger(__name__)

    def list_tables(self,dataset: str):
        tables = list(self.client.list_tables(dataset))
        return tables

    def extract_table(self, bucket_name: str, project_id: str, dataset_id: str, table_id: str, file_extension: str, location: str):
        filename = table_id + '.' + file_extension
        destination_uri = "gs://{}/{}".format(bucket_name, filename)
        dataset_ref = self.client.dataset(dataset_id, project=project_id)
        table_ref = dataset_ref.table(table_id)

        extract_job = self.client.extract_table(
            table_ref,
            destination_uri,
            # Location must match that of the source table.
            location= location,
        )  # API request
        extract_job.result()  # Waits for job to complete.

        self.logger.info("Exported {}:{}.{} to {}".format(project_id, dataset_id, table_id, destination_uri))

    def get_dataset(self,dataset_id : str):
        return self.client.get_dataset(dataset_id)
