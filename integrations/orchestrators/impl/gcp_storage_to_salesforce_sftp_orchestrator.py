from integrations.connectors.SalesforceFTP.salesforce_sftp_connector import SalesforceSftpConnector
from integrations.connectors.gcp.gcp_storage_connector import GcpStorageConnector
from integrations.orchestrators.abstract_orchestrator import AbstractOrchestrator
from integrations.orchestrators.orchestrator_executor import OrchestratorExecutor
from integrations.transformers.encryptor_transformer import EncryptorTransformer


class GcpStorageToSalesforceSftpOrchestrator(AbstractOrchestrator):

    def __init__(self, bucket: str, dataset: str):
        self.bucket = bucket
        self.dataset = dataset

    def orchestrate(self):
        nodes = [GcpStorageConnector(self.bucket, self.dataset), EncryptorTransformer(self.bucket, self.dataset), SalesforceSftpConnector(self.bucket, self.dataset)]
        OrchestratorExecutor.execute(nodes)
