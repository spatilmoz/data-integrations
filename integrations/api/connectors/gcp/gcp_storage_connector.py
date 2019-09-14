from integrations.api.connectors.abstract.connector_pull_task import ConnectorPullTask
from integrations.api.utils.bigquery_client import BigQueryClient
from integrations.api.utils.gcp_worker import GcpWorker
import logging
import sys


class GcpStorageConnector(ConnectorPullTask):
    def __init__(self, bucket: str, dataset: str):
        self.bucket = bucket
        self.dataset = dataset
        self.logger = logging.getLogger(__name__)
        self.bq_client = BigQueryClient()
        self.storage_client = GcpWorker(self.bucket, self.dataset)

    def connect_pull(self, orchestrator_data=None):
        logging.basicConfig(level=logging.INFO)

        tables = self.bq_client.list_tables(self.dataset)
        if tables:
            for table in tables:
                self.storage_client.compose(self.bucket, table.table_id)
        else:
            self.logger.error("This bucket does not contain any blobs.")  # fix the error message
            self.logger.critical(sys.exc_info()[0])

        return orchestrator_data
