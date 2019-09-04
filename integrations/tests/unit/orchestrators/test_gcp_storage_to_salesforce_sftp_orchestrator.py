import unittest
from unittest.mock import Mock
from unittest import mock

from integrations.api.orchestrators.impl.gcp_storage_to_salesforce_sftp_orchestrator import \
    GcpStorageToSalesforceSftpOrchestrator


class GcpStorageConnectorMock():
    pass

class EncryptorTransformerMock():
    pass

class SalesforceSftpConnectorMock():
    pass


class GcpStorageToSalesforceSftpOrchestratorTest(unittest.TestCase):
    pass

    # @mock.patch('integrations.api.connectors.gcp.gcp_storage_connector')
    # @mock.patch('integrations.api.transformers.encryptor_transformer')
    # @mock.patch('integrations.api.connectors.SalesforceFTP.salesforce_sftp_connector')
    # def test_mocked_orchestrator(self, mocked_storage, mocked_transformer, mocked_sftp):
    #     mocked_storage.GcpStorageConnector.return_value = Mock(return_value=GcpStorageConnectorMock())()
    #     mocked_transformer.EncryptorTransformer.return_value = Mock(return_value=EncryptorTransformerMock())
    #     mocked_sftp.SalesforceSftpConnector.return_value = Mock(return_value=SalesforceSftpConnectorMock())()
    #     under_test = GcpStorageToSalesforceSftpOrchestrator('dp2-dev-data-to-salesforce', 'cdp_to_salesforce')
    #     under_test.orchestrate()


if __name__ == "__main__":
    unittest.main()