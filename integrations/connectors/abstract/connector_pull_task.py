from abc import abstractmethod

from integrations.orchestrators.abstract.orchestrated_task import OrchestratedTask
from integrations.orchestrators.orchestrator_data import OrchestratorData


class ConnectorPullTask(OrchestratedTask):
    @abstractmethod
    def connect_pull(self, orchestrator_data=None):
        ### Establish connection
        pass

    def execute(self, orchestrator_data=None) -> OrchestratorData:
        return self.connect_pull(orchestrator_data)
