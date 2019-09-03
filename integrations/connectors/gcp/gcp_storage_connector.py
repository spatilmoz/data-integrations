from integrations.connectors.abstract.connector_pull_task import ConnectorPullTask
from integrations.utils.bigquery_client import BigQueryClient
from integrations.utils.gcp_worker import GcpWorker
import logging


class GcpStorageConnector(ConnectorPullTask):
    def __init__(self, bucket: str, dataset: str):
        self.bucket = bucket
        self.dataset = dataset
        self.logger = logging.getLogger(__name__)
        self.bq_client = BigQueryClient()
        self.storage_client = GcpWorker(self.bucket, self.dataset)

    def connect_pull(self, orchestrator_data=None):
        logging.basicConfig(level=logging.INFO)
        self.logger.info("GcpStorageConnector. Top of connect_pull.")
        tables = self.bq_client.list_tables(self.dataset)
        for table in tables:
            blobs = self.storage_client.list_blobs(prefix=table.table_id)
            self.storage_client.compose(blobs, table.table_id)

        return orchestrator_data

