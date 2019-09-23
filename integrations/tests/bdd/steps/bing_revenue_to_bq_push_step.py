from behave import *
import unittest

response = None

class BingRevenuePushConnectorStep(unittest.TestCase):

    def __init__(self):
        pass

    @given("this report {report_path}")
    def step_impl(self, report_path: str):
        with open(report_path, 'r') as f:
            for line in f.readlines():
                print(line)


    @then("we write the report data to BQ")
    def step_impl(context):
        pass


