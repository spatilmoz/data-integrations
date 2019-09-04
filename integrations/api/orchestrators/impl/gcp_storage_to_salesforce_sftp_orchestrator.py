from integrations.api.connectors.SalesforceFTP.salesforce_sftp_connector import SalesforceSftpConnector
from integrations.api.connectors.gcp.gcp_storage_connector import GcpStorageConnector
from integrations.api.orchestrators.abstract_orchestrator import AbstractOrchestrator
from integrations.api.orchestrators.orchestrator_executor import OrchestratorExecutor
from integrations.api.transformers.encryptor_transformer import EncryptorTransformer


class GcpStorageToSalesforceSftpOrchestrator(AbstractOrchestrator):

    def __init__(self, bucket: str, dataset: str, source_dir: str, destination_dir: str):
        self.bucket = bucket
        self.dataset = dataset
        self.source_dir = source_dir
        self.destination_dir = destination_dir

    def orchestrate(self):
        nodes = [GcpStorageConnector(self.bucket, self.dataset), EncryptorTransformer(self.source_dir), SalesforceSftpConnector(self.source_dir, self.destination_dir)]
        OrchestratorExecutor.execute(nodes)