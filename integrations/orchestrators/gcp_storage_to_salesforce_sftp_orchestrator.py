import bonobo

from integrations.connectors.SalesforceFTP.salesforce_sftp_connector import SalesforceSftpConnector
from integrations.connectors.gcp.gcp_storage_connector import GcpStorageConnector
from integrations.orchestrators.abstract.abstract_orchestrator import AbstractOrchestrator
from integrations.transformers.comsolidate_csv_files_transformer import ComsolidateCsvFilesTransformer


class GcpStorageToSalesforceSftpOrchestrator(AbstractOrchestrator):
    def list_of_ordered_orchestrated_tasks(self):
        return [GcpStorageConnector(), ComsolidateCsvFilesTransformer(), SalesforceSftpConnector()]

    def dict_of_services(self):
        return {}
