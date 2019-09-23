from integrations.api.connectors.abstract.connector_push_task import ConnectorPushTask
from integrations.api.orchestrators.orchestrator_data import OrchestratorData


class BigQueryRevenuePushConnector(ConnectorPushTask):
    def connect_push(self, orchestrator_data=None) -> OrchestratorData:
        pass