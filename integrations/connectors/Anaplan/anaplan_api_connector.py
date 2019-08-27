from bonobo.config import use_context

from integrations.connectors.abstract.connector_task import ConnectorTask
from integrations.orchestrators.abstract.orchestrated_task import OrchestratedTask
from integrations.orchestrators.orchestrator_data import OrchestratorData


class AnaplanApiConnector(OrchestratedTask, ConnectorTask):

    def connect(self):
        print("Connected to Anaplan")

    def push_data(self, orchestrator_data="test"):
        print("Pushing data..." , str(orchestrator_data))

    def execute(self, input_data=None) -> OrchestratorData:
        self.connect()
        output_orchestrator_data = self.passthrough_inspector(orchestrator_data=input_data, key="AnaplanApiConnector")
        self.push_data(output_orchestrator_data)
        return output_orchestrator_data

