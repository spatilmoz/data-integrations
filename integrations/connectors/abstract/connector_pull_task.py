from abc import abstractmethod

from integrations.orchestrators.abstract.orchestrated_task import OrchestratedTask
from integrations.orchestrators.orchestrator_data import OrchestratorData


class ConnectorPullTask(OrchestratedTask):
    @abstractmethod
    def connect_pull(self, orchestrator_data=None):
        '''
        The intention of this method is to establish a connection with the source; after successfully establishing a
        connection, pull/fetch the data. Since connect_pull is called via execute (through the bonobo etl pipeline)
        this method can:
            - Terminate the sequence, if unsuccessful (return self.terminate()) or return <blank>
            - Use the orchestrator_data.input if necessary and passed through to the Connector

        :param orchestrator_data: The orchestrator_data is used a collection that contains: input/output/status
        :return: integrations.orchestrators.orchestrator_data.OrchestratorData
        '''
        pass

    def execute(self, orchestrator_data=None) -> OrchestratorData:
        return self.connect_pull(orchestrator_data)
