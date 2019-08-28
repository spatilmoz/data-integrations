from abc import abstractmethod

from integrations.orchestrators.abstract.orchestrated_task import OrchestratedTask
from integrations.orchestrators.orchestrator_data import OrchestratorData


class TransformerTask(OrchestratedTask):
    def execute(self, orchestrator_data=None) -> OrchestratorData:
        return self.transform(orchestrator_data)

    @abstractmethod
    def transform(self, orchestrator_data: OrchestratorData):
        raise NotImplementedError
