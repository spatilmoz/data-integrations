import json
import unittest
from unittest import mock
import integrations.tests.resources as test_resources
from integrations.api.connectors.Workday.workday_api_connector import WorkdayAPIConnector

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources



class MockResponse:
    def __init__(self, file_path):
        self.file_path = file_path
        self.response_file = pkg_resources.read_text(test_resources, file_path)

    @property
    def content(self):
        data = json.loads(self.response_file)
        return json.dumps(data)


class TestWorkdayAPIConnector(unittest.TestCase):
    workday_url = 'https://services1.myworkday.com/ccx/service/customreport2/vhr_mozilla/hchai%40mozilla.com'
    total_staffing_report_name = 'intg__MoCo_Finance_Tableau_Total_Staffing_Report_-_Masked'
    total_staffing_url_params = 'Effective_as_of_Date_and_Time=2019-08-20T00%3A00%3A00.000-07%3A00&Entry_self.Date_and_Time=2019-08-20T00%3A00%3A00.000-07%3A00&format=json'
    open_positions_report_name = 'intg__MoCo_Finance_Tableau_Open_Positions_Details_Report_-_Masked'
    open_positions_url_params = 'Effective_as_of_Date=2019-08-19-07%3A00&format=json'
    username = ''
    password = ''

    @mock.patch('requests.get')
    def test_connection_established_total_staffing(self, mocked_instance):
        mocked_instance.return_value = MockResponse('workday_report_total_staffing.json')
        api_connector = WorkdayAPIConnector(url=self.workday_url, report_name=self.total_staffing_report_name,
                                            url_params=self.total_staffing_url_params, username=self.username,
                                            password=self.password)
        api_connector.connect_pull()

    @mock.patch('requests.get')
    def test_connection_established_open_positions(self, mocked_instance):
        mocked_instance.return_value = MockResponse('workday_report_open_positions.json')

        api_connector = WorkdayAPIConnector(url=self.workday_url, report_name=self.open_positions_report_name,
                                            url_params=self.open_positions_url_params, username=self.username,
                                            password=self.password)
        api_connector.connect_pull()


if __name__ == '__main__':
    unittest.main()
