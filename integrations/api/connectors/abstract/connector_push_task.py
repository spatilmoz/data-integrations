from abc import abstractmethod

from integrations.api.orchestrators.abstract_orchestrator_task import AbstractOrchestratorTask
from integrations.api.orchestrators.orchestrator_data import OrchestratorData


class ConnectorPushTask(AbstractOrchestratorTask):
    @abstractmethod
    def connect_push(self, orchestrator_data=None) -> OrchestratorData:
        """
        The intention of this method is to establish a connection with the source; after successfully establishing a
        connection, push the data. Since connect_push is called via execute (through the bonobo etl pipeline)
        this method can:
            - Terminate the sequence, if unsuccessful (return self.terminate()) or return <blank>
            - Use the orchestrator_data.input if necessary and passed through to the Connector
            - Return success with OrchestratorData

        :param orchestrator_data: The orchestrator_data is used a collection that contains: input/output/status
        :return OrchestratorData: Return the provided input with modified output and/or success state
        """
        pass

    def execute(self, orchestrator_data=None) -> OrchestratorData:
        return self.connect_push(orchestrator_data)