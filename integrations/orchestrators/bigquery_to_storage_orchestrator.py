from integrations.connectors.SalesforceFTP.salesforce_sftp_connector import SalesforceSftpConnector
from integrations.connectors.gcp.bigquery_to_storage_process import BigQueryToStorageProcess
from integrations.connectors.gcp.gcp_storage_connector import GcpStorageConnector
from integrations.orchestrators.abstract.abstract_orchestrator import AbstractOrchestrator
from integrations.orchestrators.orchestrator_worker import OrchestratorWorker
from integrations.transformers.encryptor_transformer import EncryptorTransformer


class BigQueryToStorageOrchestrator(AbstractOrchestrator):
    def __init__(self, bucket : str, dataset : str):
        self.bucket = bucket
        self.dataset = dataset

    def orchestrate(self):
        nodes = [BigQueryToStorageProcess()]
        OrchestratorWorker.work(nodes)
