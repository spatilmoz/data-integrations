from integrations.connectors.abstract.connector_pull_task import ConnectorPullTask
from integrations.orchestrators.orchestrator_data import OrchestratorData


class WorkdaySftpConnector(ConnectorPullTask):
    def connect_pull(self, orchestrator_data=None):
        return {"Workday": list(range(10))}



