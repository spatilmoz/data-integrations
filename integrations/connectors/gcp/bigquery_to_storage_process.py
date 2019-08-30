from integrations.orchestrators.abstract.abstract_orchestrator import AbstractOrchestrator
from integrations.orchestrators.orchestrator_data import OrchestratorData
import logging

import integrations.utils.bigquery_client

class BigQueryToStorageProcess(AbstractOrchestrator):

    def __init__(self, bucket: str, dataset_id: str, project_id : str, file_extension : str, location : str):
        self.bucket = bucket
        self.dataset_id = dataset_id
        self.project_id = project_id
        self.file_extension = file_extension
        self.location = location
        self.logger = logging.getLogger(__name__)
        self.bq_client = integrations.utils.bigquery_client.BigQueryClient()

    def orchestrate(self, orchestrator_data=None) -> OrchestratorData:
        dataset = self.bq_client.get_dataset(self.dataset_id)
        tables = list(self.bq_client.list_tables(dataset))

        if tables:
            for table in tables:
                self.logger.info("Found table: '{}".format(table.table_id))
                self.logger.info("Exporting '{}' to bucket".format(table.table_id))
                self.bq_client.extract_table(bucket_name=self.bucket, project=self.project_id,
                                       dataset_id=dataset, table_id=table.table_id,file_extension=self.file_extension, location=self.location)
        else:
            self.logger.info("This dataset does not contain any tables.")  # fix the error message




