from abc import ABC, abstractmethod

from bonobo.config import use_context

from integrations.orchestrators.orchestrator_data import OrchestratorData


class OrchestratedTask(ABC):

    @abstractmethod
    def execute(self, input_data=None) -> OrchestratorData:
        pass  # should return output_data

    @use_context
    def __call__(self, *args, **kwargs):
        return self.execute(args)