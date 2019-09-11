import logging
from integrations.api.orchestrators.abstract_orchestrator_task import AbstractOrchestratorTask
from integrations.api.orchestrators.orchestrator_data import OrchestratorData
from integrations.api.utils import bigquery_client
from integrations.api.utils import gcp_worker


class GcpCleanerTask(AbstractOrchestratorTask):

    def __init__(self, bucket_name: str, dataset_id: str):
        self.bucket_name = bucket_name
        self.dataset_id = dataset_id
        self.logger = logging.getLogger(__name__)
        self.bq_client = bigquery_client.BigQueryClient()
        self.storage_client = gcp_worker.GcpWorker(self.bucket_name, self.dataset_id)

    def execute(self, orchestrator_data=None) -> OrchestratorData:
        blobs = self.storage_client.list_blobs()
        self.logger.info('Starting to delete all blobs from bucket {}'.format(self.bucket_name))
        for blob in blobs:
            print(blob.name)
            self.logger.info('Deleting {} from gcs'.format(blob.name))
            self.storage_client.delete_blob(blob.name)

        self.logger.info('Starting to delete all tables from dataset {}'.format(self.dataset_id))
        tables = self.bq_client.list_tables(self.dataset_id)
        for table in tables:
            self.logger.info('Deleting {} table from BigQuery'.format(table.table_id))
            self.bq_client.delete_table(self.dataset_id, table.table_id)