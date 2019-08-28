import unittest
from unittest.mock import Mock

from integrations.orchestrators.gcp_storage_to_salesforce_sftp_orchestrator import \
    GcpStorageToSalesforceSftpOrchestrator


class GcpStorageToSalesforceSftpOrchestratorTest(unittest.TestCase):

    def test_mocked_orchestrator(self):
        under_test = GcpStorageToSalesforceSftpOrchestrator('dp2-dev-data-to-salesforce', 'cdp_to_salesforce')
        under_test.orchestrate()


if __name__ == "__main__":
    unittest.main()