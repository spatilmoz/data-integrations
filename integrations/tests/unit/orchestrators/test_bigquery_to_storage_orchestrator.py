import unittest
from unittest.mock import Mock
from unittest import mock
from integrations.api.orchestrators.impl.bigquery_to_storage_orchestrator import BigQueryToStorageOrchestrator
from integrations.tests.unit.mocks.bigquery_client_mock import BigqueryClientMock


class TestBigQueryToStorageOrchestrator(unittest.TestCase):

    @mock.patch('integrations.api.utils.bigquery_client')
    def test_orchestration_without_tables(self, mocked_instance):
        mocked_instance.BigQueryClient.return_value = Mock(return_value=BigqueryClientMock())()
        under_test = BigQueryToStorageOrchestrator(bucket='dp2-dev-data-to-salesforce', dataset='cdp_to_salesforce',
                                      file_extension='csv', location='US')

        under_test.orchestrate()


    @mock.patch('integrations.api.utils.bigquery_client')
    def test_orchestration_with_tables(self, mocked_instance):
        tables = [Mock()]
        mocked_instance.BigQueryClient.return_value = Mock(return_value=BigqueryClientMock(tables))()
        under_test = BigQueryToStorageOrchestrator(bucket='dp2-dev-data-to-salesforce', dataset='cdp_to_salesforce',
                                      file_extension='csv', location='US')

        under_test.orchestrate()



