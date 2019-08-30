import unittest
import pytest
import google
from google.cloud import bigquery
from integrations.connectors.gcp.bigquery_to_storage_process import BigQueryToStorageProcess
from unittest.mock import Mock, MagicMock, PropertyMock
from unittest import mock

class ClientMock():
    def __init__(self, tables=[]):
        self.tables = tables

    def list_tables(self,dataset : str):
        return self.tables

    def get_dataset(self, dataset_id: str):
        return 'dataset'

    def extract_table(self,bucket_name, project, dataset_id, table_id,file_extension,location):
        pass

class TestBigQueryToStorageProcess(unittest.TestCase):
    @mock.patch('integrations.utils.bigquery_client')
    def test_orchestration_without_tables(self,mocked_instance):
        mocked_instance.BigQueryClient.return_value = Mock(return_value=ClientMock())()
        _test = BigQueryToStorageProcess('bucket1', 'dataset_id1', 'project_id1' , 'csv', 'US')
        _test.orchestrate()

    @mock.patch('integrations.utils.bigquery_client')
    def test_orchestration_with_tables(self, mocked_instance):
        tables = [Mock()]
        mocked_instance.BigQueryClient.return_value = Mock(return_value=ClientMock(tables))()
        _test = BigQueryToStorageProcess('bucket1', 'dataset_id1', 'project_id1', 'csv', 'US')
        _test.orchestrate()


if __name__ == "__main__":
   unittest.main()