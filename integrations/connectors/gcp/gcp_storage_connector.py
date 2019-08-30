from integrations.connectors.abstract.connector_pull_task import ConnectorPullTask
from integrations.orchestrators.orchestrator_data import OrchestratorData
from integrations.utils.gcp_worker import GcpWorker
import logging
from google.cloud import bigquery


class GcpStorageConnector(ConnectorPullTask):
    def __init__(self, bucket: str, dataset: str):
        self.bucket = bucket
        self.dataset = dataset
        self.logger = logging.getLogger(__name__)

    def connect_pull(self, orchestrator_data=None):
        logging.basicConfig(level=logging.INFO)
        # try:
        #     gcp_worker = GcpWorker(self.bucket, self.dataset)
        #
        #     self.logger.info('Starting Compose stage')
        #     bq_client = bigquery.Client()
        #     tables = bq_client.list_tables(dataset=self.dataset)
        #
        #     for table in tables:
        #         self.logger.info('Fetching files for {}'.format(table.table_id))
        #         blobs = gcp_worker.list_blobs(prefix=table.table_id)
        #         gcp_worker.compose([blob.name for blob in blobs], table.table_id)
        # except:
        #     self.logger.error('GcpStorageConnector ERROR')

        self.logger.info("GcpStorageConnector")

        return orchestrator_data

