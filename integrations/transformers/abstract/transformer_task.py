from abc import abstractmethod

from integrations.orchestrators.abstract_orchestrator_task import AbstractOrchestratorTask
from integrations.orchestrators.orchestrator_data import OrchestratorData


class TransformerTask(AbstractOrchestratorTask):
    def execute(self, orchestrator_data=None) -> OrchestratorData:
        """
        Please view AbstractOrchestratorTask.execute(). For children of TransformerTask, the transform method should be implemented
        :param orchestrator_data: If provided the OrchestratorData might contain input to use in
        this task step to convert to another format.
        :return OrchestratorData: Transformed, formatted, processed data.
        """
        return self.transform(orchestrator_data)

    @abstractmethod
    def transform(self, orchestrator_data: OrchestratorData) -> OrchestratorData:
        """
        Children of TransformerTask will implement this method. Converting the OrchestratorData.input via the
        transformation and returning the new processed data as the OrchestratorData.output
        :param orchestrator_data:  If provided the OrchestratorData might contain input to use in
        this task step to convert to another format.
        :return OrchestratorData: If successful transformed, formatted, processed data, otherwise False success state
        """
        pass
