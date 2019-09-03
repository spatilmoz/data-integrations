from integrations.connectors.gcp.bigquery_to_storage_process import BigQueryToStorageProcess
from integrations.orchestrators.abstract_orchestrator import AbstractOrchestrator
from integrations.orchestrators.orchestrator_executor import OrchestratorExecutor


class BigQueryToStorageOrchestrator(AbstractOrchestrator):
    def __init__(self, bucket: str, dataset: str, file_extension: str, location: str):
        self.bucket = bucket
        self.dataset = dataset
        self.file_extension = file_extension
        self.location = location

    def orchestrate(self):
        nodes = [BigQueryToStorageProcess(self.bucket,
                                          self.dataset,
                                          self.file_extension,
                                          self.location)]
        OrchestratorExecutor.execute(nodes)
