from integrations.api.orchestrators.abstract_orchestrator_task import AbstractOrchestratorTask
from integrations.api.orchestrators.orchestrator_data import OrchestratorData
import logging
import integrations.api.utils.bigquery_client
import sys


class BigQueryToStorageProcess(AbstractOrchestratorTask):

    def __init__(self, bucket_name: str, dataset_id: str, file_extension: str, location: str):
        self.bucket_name = bucket_name
        self.dataset_id = dataset_id
        self.file_extension = file_extension
        self.location = location
        self.logger = logging.getLogger(__name__)
        self.bq_client = integrations.api.utils.bigquery_client.BigQueryClient()

    def execute(self, orchestrator_data=None) -> OrchestratorData:
        dataset = self.bq_client.get_dataset(self.dataset_id)
        tables = list(self.bq_client.list_tables(dataset))

        if tables:
            for table in tables:
                self.logger.info("Found table: '{}".format(table.table_id))
                self.logger.info("Exporting '{}' to bucket".format(table.table_id))
                self.bq_client.extract_table(bucket_name=self.bucket_name,
                                             dataset_id=self.dataset_id,
                                             table_id=table.table_id,
                                             file_extension=self.file_extension,
                                             location=self.location)
        else:
            self.logger.error("This dataset does not contain any tables.")  # fix the error message
            self.logger.critical(sys.exc_info()[0])
