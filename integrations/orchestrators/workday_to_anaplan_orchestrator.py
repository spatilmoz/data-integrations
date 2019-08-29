from integrations.connectors.Anaplan.anaplan_api_connector import AnaplanApiConnector
from integrations.connectors.Workday.workday_sftp_connector import WorkdaySftpConnector
from integrations.orchestrators.abstract.abstract_orchestrator import AbstractOrchestrator
from integrations.orchestrators.orchestrator_worker import OrchestratorWorker
from integrations.transformers.workday_to_anaplan_fss_transformer import WorkdayToAnaplanFSSTransformer


class WorkdayToAnaplanOrchestrator(AbstractOrchestrator):
    def orchestrate(self):
        nodes = [WorkdaySftpConnector(), WorkdayToAnaplanFSSTransformer(), AnaplanApiConnector()]
        OrchestratorWorker.work(nodes)
