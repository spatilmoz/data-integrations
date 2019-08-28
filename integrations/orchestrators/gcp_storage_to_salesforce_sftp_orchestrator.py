from integrations.connectors.SalesforceFTP.salesforce_sftp_connector import SalesforceSftpConnector
from integrations.connectors.gcp.gcp_storage_connector import GcpStorageConnector
from integrations.orchestrators.abstract.abstract_orchestrator import AbstractOrchestrator
from integrations.orchestrators.orchestrator_data import OrchestratorData
from integrations.transformers.encryptor_transformer import EncryptorTransformer

class GcpStorageToSalesforceSftpOrchestrator(AbstractOrchestrator):
    def __init__(self, bucket : str, dataset : str):
        self.bucket = bucket
        self.dataset = dataset

    def list_of_ordered_orchestrated_tasks(self):
        return [GcpStorageConnector(self.bucket, self.dataset), EncryptorTransformer(), SalesforceSftpConnector()]

    def dict_of_services(self):
        return {}

    def orchestrate(self, input_args=None):
        #GcpStorageConnector(self.bucket, self.dataset).connect_pull()
        #EncryptorTransformer(self.bucket, self.dataset).transform(OrchestratorData())
        SalesforceSftpConnector(self.bucket, self.dataset).connect_push(OrchestratorData())