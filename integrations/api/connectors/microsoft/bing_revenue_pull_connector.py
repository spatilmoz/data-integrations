from integrations.api.connectors.abstract.connector_pull_task import ConnectorPullTask
from integrations.api.orchestrators.orchestrator_data import OrchestratorData
import requests
import json
from integrations.api.config.app_configuration import *
import time
import urllib.request
import base64
import zipfile
import io

from integrations.api.utils.local_config import LocalConfig

local_config = LocalConfig()

class BingRevenuePullConnector(ConnectorPullTask):
    base_url = 'https://searchapi.pubcenter.microsoft.com/api/{}'
    report_url = base_url.format('v3/report')
    report_job_url = base_url.format('v1/reportjobs/{}')

    def __init__(self, start_date: str, end_date: str, report_name: str, report_type: str,granularity: str, columns: [] ):
        self.start_date = start_date
        self.end_date = end_date
        self.report_name = report_name
        self.report_type = report_type
        self.granularity = granularity
        self.columns = columns
        self.http_headers()

    def create_post_request(self):
        return self.base_url

    def http_headers(self):
        self.headers = dict()
        bing_creds = local_config['revenue']['bing']['creds']
        # return OrchestratorData(output=headers)
        self.headers['Content-Type'] = bing_creds['content_type']
        self.headers['Username'] = bing_creds['username']
        self.headers['Password'] = bing_creds['password']
        self.headers['DeveloperToken'] = bing_creds['developer_token']

    def connect_pull(self, orchestrator_data=None) -> OrchestratorData:

        payload = dict()
        payload['startDate'] = self.start_date
        payload['endDate'] = self.end_date
        payload['reportName'] = self.report_name
        payload['reportType'] = self.report_type
        payload['granularity'] = self.granularity
        payload['columns'] = self.columns

        response = requests.request("POST", self.report_url, data=json.dumps(payload), headers=self.headers)
        loads = json.loads(response.content.decode('utf-8'))
        job_id_string = loads['jobIdString']
        status_code = None

        while status_code != 200:
            report = requests.get(self.report_job_url.format(job_id_string), headers=self.headers)
            if report.status_code == 200:
                download_url = json.loads(report.content)['downloadUrl']
                response = urllib.request.urlopen(download_url)
                zip_content = io.BytesIO(response.read())
                zip_file = zipfile.ZipFile(zip_content, "r")
                for zipinfo in zip_file.infolist():
                    with zip_file.open(zipinfo) as csv:
                        with open('report.csv', 'wb') as f:
                            f.write(csv.read())



                #data = response.read()
                #text = data.decode('utf-8')
                #with open('report.out', 'wb') as f:
                    #f.write(response.read())
                status_code = report.status_code
            else:
                time.sleep(1)


