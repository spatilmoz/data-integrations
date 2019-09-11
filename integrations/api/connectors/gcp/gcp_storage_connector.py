from integrations.api.connectors.abstract.connector_pull_task import ConnectorPullTask
from integrations.api.utils.bigquery_client import BigQueryClient
from integrations.api.utils.gcp_worker import GcpWorker
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

        tables = self.bq_client.list_tables(self.dataset)
        for table in tables:
            self.storage_client.download(self.bucket, table.table_id)
            #self.storage_client.compose(self.bucket, table.table_id)



        return orchestrator_data

