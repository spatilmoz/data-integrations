from integrations.api.connectors.abstract.connector_pull_task import ConnectorPullTask
from integrations.api.orchestrators.orchestrator_data import OrchestratorData
import requests
import json
from integrations.api.config.app_configuration import *
import time
import urllib.request
import base64

class BingRevenuePullConnector(ConnectorPullTask):
    def __init__(self, job_id_url: str, report_id_url: str, start_date: str, end_date: str, report_name: str, report_type: str, granularity: str, columns: []):
        self.job_id_url = job_id_url
        self.report_id_url = report_id_url
        self.start_date = start_date
        self.end_date = end_date
        self.report_name = report_name
        self.report_type = report_type
        self.granularity = granularity
        self.columns = columns

    def connect_pull(self, orchestrator_data=None) -> OrchestratorData:
        headers = dict()
        headers['Content-Type'] = bing_revenue_content_type
        headers['Username'] = bing_revenue_username
        headers['Password'] = bing_revenue_password
        headers['DeveloperToken'] = bing_revenue_developer_token

        payload = dict()
        payload['startDate'] = self.start_date
        payload['endDate'] = self.end_date
        payload['reportName'] = self.report_name
        payload['reportType'] = self.report_type
        payload['granularity'] = self.granularity
        payload['columns'] = self.columns

        response = requests.request("POST", self.job_id_url, data=json.dumps(payload), headers=headers)
        loads = json.loads(response.content.decode('utf-8'))
        job_id_string = loads['jobIdString']
        status_code = None

        while status_code != 200:
            report = requests.get(self.report_id_url + job_id_string, headers=headers)
            if report.status_code == 200:
                download_url = json.loads(report.content)['downloadUrl']
                response = urllib.request.urlopen(download_url)
                data = response.read()
                text = data.decode('utf-8')
                status_code = report.status_code
            else:
                time.sleep(1)


