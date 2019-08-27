from abc import abstractmethod, ABC

from integrations.orchestrators.orchestrator_data import OrchestratorData


class TransformerTask(ABC):
    @abstractmethod
    def transform(self, orchestrator_data: OrchestratorData):
        raise NotImplementedError
