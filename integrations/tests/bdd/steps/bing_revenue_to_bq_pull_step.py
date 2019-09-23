from behave import *
import unittest
from integrations.api.connectors.microsoft.bing_revenue_pull_connector import BingRevenuePullConnector

response = None

class BingRevenuePullConnectorStep(unittest.TestCase):

    def __init__(self):
        self.start_date = None
        self.end_date = None
        self.report_name = None
        self.report_type = None
        self.granularity = None
        self.columns = None

    @given("the report name is {report_name}")
    def step_impl(self, report_name: str):
        self.report_name = report_name

    @step("the date range is from {start_date} to {end_date}")
    def step_impl(self, start_date: str, end_date:str):
        self.start_date = start_date
        self.end_date = end_date

    @step("the report type is {report_type}")
    def step_impl(self, report_type: str):
        self.report_type = report_type

    @step("the report granularity is {granularity}")
    def step_impl(self, granularity: str):
        self.granularity = granularity

    @step("the report columns are {columns}")
    def step_impl(self, columns: str):
        result = columns.split(',')
        self.columns = result

    @when("we hit the endpoint")
    def step_impl(self):
        global response
        response = BingRevenuePullConnector(self.start_date, self.end_date, self.report_name, self.report_type,
                                            self.granularity, self.columns).connect_pull()

    @then("we get a response")
    def step_impl(context):
        global response
        assert response != None
