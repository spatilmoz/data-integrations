import bonobo

from integrations.connectors.SalesforceFTP.salesforce_sftp_connector import SalesforceSftpConnector
from integrations.connectors.gcp.gcp_storage_connector import GcpStorageConnector
from integrations.orchestrators.abstract.abstract_orchestrator import AbstractOrchestrator
from integrations.transformers.comsolidate_csv_files_transformer import ComsolidateCsvFilesTransformer


class GcpStorageToSalesforceSftpOrchestrator(AbstractOrchestrator):
    def get_graph(self):
        graph = bonobo.Graph()
        graph.add_chain(GcpStorageConnector(), ComsolidateCsvFilesTransformer(), SalesforceSftpConnector())
        return graph

    def orchestrate(self, input_args=None):
        bonobo.run(
            self.get_graph(),
            services={})
