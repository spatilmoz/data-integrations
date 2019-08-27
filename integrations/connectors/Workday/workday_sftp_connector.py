from bonobo.config import use_context

from integrations.connectors.abstract.connector_task import ConnectorTask
from integrations.orchestrators.abstract.orchestrated_task import OrchestratedTask
from integrations.orchestrators.orchestrator_data import OrchestratorData


class WorkdaySftpConnector(OrchestratedTask, ConnectorTask):

    def connect(self):
        print("Connecting to Workday ...")

    def fetch_data(self):
        return {"Workday": list(range(10))}

    def execute(self, input_data=None) -> OrchestratorData:
        self.connect()
        output_orchestrator_data = self.passthrough_inspector(orchestrator_data=input_data, key="WorkdaySftpConnector")
        output_orchestrator_data.output = self.fetch_data()
        return output_orchestrator_data


