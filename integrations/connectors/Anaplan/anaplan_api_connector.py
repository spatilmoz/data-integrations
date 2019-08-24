from integrations.connectors.abstract.connector_task import ConnectorTask
from integrations.orchestrators.abstract.orchestrated_task import OrchestratedTask


class AnaplanApiConnector(OrchestratedTask, ConnectorTask):
    connection_params = {}

    def connect(self):
        # abstract method impl
        pass

    def push_data(self, data):
        # abstract method impl
        print("Pushing data to Anaplan API")

    def execute(self, input_data=None):
        # This method should do the necessary steps for the Connector
        if input_data is None:
            print(input_data)
            raise Exception("Expecting input_data for pushing to Anaplan API.")

        self.connect()
        self.push_data(input_data)

        return "success"
