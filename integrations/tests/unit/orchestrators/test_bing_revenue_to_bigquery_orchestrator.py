import unittest
from unittest.mock import Mock
from unittest import mock
from integrations.api.orchestrators.impl.bing_revenue_to_bigquery_orchestrator import BingRevenueToBigQueryOrchestrator
from integrations.api.utils.input_args_worker import InputArgsWorker
from datetime import datetime


class MockInputArgsWorker(InputArgsWorker):
    def __init__(self):
        pass

    def get_value(self, key):
        return datetime.now()

class TestBingRevenueToBigQueryOrchestrator(unittest.TestCase):

    def test_mocked_orchestrator(self):
        under_test = BingRevenueToBigQueryOrchestrator(worker= MockInputArgsWorker())
        under_test.orchestrate()

    def test_is_pipeline_key(self):
        static_under_test = BingRevenueToBigQueryOrchestrator
        pipeline_key = static_under_test.get_pipeline_key()
        result = static_under_test.is_pipeline_key(pipeline_key)
        self.assertTrue(result)

    def test_is_not_pipeline_key(self):
        static_under_test = BingRevenueToBigQueryOrchestrator
        result = static_under_test.is_pipeline_key('test')
        self.assertFalse(result)

    def test_pipeline_key_not_changed(self):
        static_under_test = BingRevenueToBigQueryOrchestrator
        current_pipeline_key = 'bing_revenue_to_big_query'
        pipeline_key = static_under_test.get_pipeline_key()
        self.assertEqual(current_pipeline_key,pipeline_key)
        result = static_under_test.is_pipeline_key(current_pipeline_key)
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()