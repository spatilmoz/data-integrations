from integrations.connectors.abstract.connector_push_task import ConnectorPushTask


class AnaplanApiConnector(ConnectorPushTask):
    def connect_push(self, orchestrator_data=None):
        print("Pushing data..." , str(orchestrator_data))
        return orchestrator_data

