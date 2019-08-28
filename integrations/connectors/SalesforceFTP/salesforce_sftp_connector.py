from integrations.connectors.abstract.connector_push_task import ConnectorPushTask


class SalesforceSftpConnector(ConnectorPushTask):
    def connect_push(self, orchestrator_data=None):
        return orchestrator_data