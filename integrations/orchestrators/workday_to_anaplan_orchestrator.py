from integrations.connectors.Anaplan.anaplan_api_connector import AnaplanApiConnector
from integrations.connectors.Workday.workday_sftp_connector import WorkdaySftpConnector
from integrations.orchestrators.abstract.abstract_orchestrator import AbstractOrchestrator
from integrations.transformers.workday_to_anaplan_fss import WorkdayToAnaplanFSSTransformer
import bonobo
import logging


class WorkdayToAnaplanOrchestrator(AbstractOrchestrator):

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)

    def get_graph(self):
        graph = bonobo.Graph()
        graph.add_chain(AnaplanApiConnector(), WorkdayToAnaplanFSSTransformer(), WorkdaySftpConnector())
        return graph


    def orchestrate(self):
        bonobo.run(
            self.get_graph(),
            services={})
