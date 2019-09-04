import unittest
from integrations.api.connectors.gcp.bigquery_to_storage_process import BigQueryToStorageProcess
from unittest.mock import Mock
from unittest import mock

from integrations.tests.unit.mocks.bigquery_client_mock import BigqueryClientMock


class TestBigQueryToStorageProcess(unittest.TestCase):
    @mock.patch('integrations.api.utils.bigquery_client')
    def test_orchestration_without_tables(self, mocked_instance):
        mocked_instance.BigQueryClient.return_value = Mock(return_value=BigqueryClientMock())()
        _test = BigQueryToStorageProcess('bucket1', 'dataset_id1' , 'csv', 'US')
        _test.execute()

    @mock.patch('integrations.api.utils.bigquery_client')
    def test_orchestration_with_tables(self, mocked_instance):
        tables = [Mock()]
        mocked_instance.BigQueryClient.return_value = Mock(return_value=BigqueryClientMock(tables))()
        _test = BigQueryToStorageProcess('bucket1', 'dataset_id1', 'csv', 'US')
        _test.execute()


if __name__ == "__main__":
   unittest.main()