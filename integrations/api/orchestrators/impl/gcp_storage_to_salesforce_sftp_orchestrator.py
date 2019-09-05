import integrations.api.connectors.SalesforceFTP.salesforce_sftp_connector
import integrations.api.connectors.gcp.gcp_storage_connector
from integrations.api.orchestrators.abstract_orchestrator import AbstractOrchestrator
from integrations.api.orchestrators.orchestrator_executor import OrchestratorExecutor
import integrations.api.transformers.encryptor_transformer


class GcpStorageToSalesforceSftpOrchestrator(AbstractOrchestrator):

    def __init__(self, bucket: str, dataset: str, source_dir: str, destination_dir: str):
        self.bucket = bucket
        self.dataset = dataset
        self.source_dir = source_dir
        self.destination_dir = destination_dir

    def orchestrate(self):
        storage_connector = integrations.api.connectors.gcp.gcp_storage_connector.GcpStorageConnector(self.bucket, self.dataset)
        transformer = integrations.api.transformers.encryptor_transformer.EncryptorTransformer(self.source_dir)
        sftp_connector = integrations.api.connectors.SalesforceFTP.salesforce_sftp_connector.SalesforceSftpConnector(self.source_dir, self.destination_dir)

        nodes = [storage_connector, transformer, sftp_connector]
        OrchestratorExecutor.execute(nodes)