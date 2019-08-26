from bonobo.config import use_context

from integrations.connectors.abstract.connector_task import ConnectorTask
from integrations.orchestrators.abstract.orchestrated_task import OrchestratedTask
from integrations.orchestrators.orchestrator_data import OrchestratorData


class AnaplanApiConnector(OrchestratedTask):

    def execute(self, orchestrator_data=None) -> OrchestratorData:
        output_orchestrator_data = self.passthrough_inspector(orchestrator_data, "AnaplanApiConnector")
        return output_orchestrator_data

