from integrations.connectors.abstract.connector_task import ConnectorTask
from integrations.orchestrators.abstract.orchestrated_task import OrchestratedTask


class WorkdaySftpConnector(OrchestratedTask, ConnectorTask):
    connection_params = {}

    def connect(self):
        # abstract method impl
        pass

    def fetch_data(self):
        # abstract method impl
        print("Fetching data from Workday")
        data = {"key": "value"}
        return data

    def execute(self, input_data=None):
        # This method should do the necessary steps for the Connector
        if input_data is not None:
            print(input_data)
            raise Exception("Not expecting input_data for pulling from Workday SFTP Connector (at this time).")

        self.connect()
        return self.fetch_data()
