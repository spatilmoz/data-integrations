from integrations.connectors.Anaplan.anaplan_api_connector import AnaplanApiConnector
from integrations.connectors.Workday.workday_sftp_connector import WorkdaySftpConnector
from integrations.orchestrators.abstract.abstract_orchestrator import AbstractOrchestrator
from integrations.transformers.workday_to_anaplan_fss_transformer import WorkdayToAnaplanFSSTransformer
import bonobo
import logging


class WorkdayToAnaplanOrchestrator(AbstractOrchestrator):
    def list_of_ordered_orchestrated_tasks(self):
        return [WorkdaySftpConnector(), WorkdayToAnaplanFSSTransformer(), AnaplanApiConnector()]

    def dict_of_services(self):
        return {}

