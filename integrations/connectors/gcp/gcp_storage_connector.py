from integrations.connectors.abstract.connector_pull_task import ConnectorPullTask


class GcpStorageConnector(ConnectorPullTask):
    def connect_pull(self, orchestrator_data=None):
        return orchestrator_data

