from integrations.connectors.Anaplan.anaplan_api_connector import AnaplanApiConnector
from integrations.connectors.Workday.workday_sftp_connector import WorkdaySftpConnector
from integrations.orchestrators.abstract.abstract_orchestrator import AbstractOrchestrator
from integrations.transformers.workday_to_anaplan_fss import WorkdayToAnaplanFSS


class WorkdayToAnaplanOrchestrator(AbstractOrchestrator):
    @property
    def internal_ordered_tasks(self):
        return [
            WorkdaySftpConnector(),
            WorkdayToAnaplanFSS(),
            AnaplanApiConnector()
        ]