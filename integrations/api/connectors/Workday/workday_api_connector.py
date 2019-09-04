from integrations.api.connectors.abstract.connector_pull_task import ConnectorPullTask
from integrations.api.orchestrators.orchestrator_data import OrchestratorData
import requests
import json


class WorkdayAPIConnector(ConnectorPullTask):

    def __init__(self, url: str, report_name: str, url_params: str, username: str, password: str):
        super().__init__()
        self.url = url
        self.report_name = report_name
        self.url_params = url_params
        self.username = username
        self.password = password

    def get_format(self):
        return '{}/{}?{}'

    def get_uri(self):
        return self.get_format().format(self.url, self.report_name, self.url_params)

    def get_auth(self):
        return self.username, self.password

    def connect_pull(self, orchestrator_data=OrchestratorData()):
        response = requests.get(self.get_uri(), auth=self.get_auth())
        orchestrator_data.output = json.loads(response.content)
        return orchestrator_data
