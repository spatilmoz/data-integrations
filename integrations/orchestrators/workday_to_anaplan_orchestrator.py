from integrations.connectors.Anaplan.anaplan_api_connector import AnaplanApiConnector
from integrations.connectors.Workday.workday_sftp_connector import WorkdaySftpConnector
from integrations.orchestrators.abstract.abstract_orchestrator import AbstractOrchestrator
from integrations.transformers.workday_to_anaplan_fss_transformer import WorkdayToAnaplanFSSTransformer
import bonobo
import logging


class WorkdayToAnaplanOrchestrator(AbstractOrchestrator):

    def get_graph(self):
        graph = bonobo.Graph()
        graph.add_chain(WorkdaySftpConnector(), WorkdayToAnaplanFSSTransformer(), AnaplanApiConnector())
        return graph

    def orchestrate(self, input_args=None):
        bonobo.run(
            self.get_graph(),
            services={})
