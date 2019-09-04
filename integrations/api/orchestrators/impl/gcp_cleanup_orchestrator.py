from integrations.api.orchestrators.abstract_orchestrator import AbstractOrchestrator
from integrations.api.orchestrators.orchestrator_executor import OrchestratorExecutor
from integrations.api.tasks.gcp_cleaner_task import GcpCleanerTask


class GcpCleanupOrchestrator(AbstractOrchestrator):

    def __init__(self, bucket: str, dataset: str):
        self.bucket = bucket
        self.dataset = dataset

    def orchestrate(self):
        nodes = [GcpCleanerTask(self.bucket, self.dataset)]
        OrchestratorExecutor.execute(nodes)