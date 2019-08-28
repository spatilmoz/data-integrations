from abc import abstractmethod

from integrations.orchestrators.abstract.orchestrated_task import OrchestratedTask
from integrations.orchestrators.orchestrator_data import OrchestratorData


class ConnectorPushTask(OrchestratedTask):
    @abstractmethod
    def connect_push(self, orchestrator_data=None):
        pass

    def execute(self, orchestrator_data=None) -> OrchestratorData:
        return self.connect_push(orchestrator_data)
