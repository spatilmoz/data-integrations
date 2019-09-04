from os import environ

from integrations.connectors.Anaplan.anaplan_api_connector import AnaplanApiConnector
from integrations.connectors.Workday.workday_api_connector import WorkdayAPIConnector
from integrations.orchestrators.abstract_orchestrator import AbstractOrchestrator
from integrations.orchestrators.orchestrator_executor import OrchestratorExecutor
from integrations.transformers.workday_to_anaplan_fss_transformer import WorkdayToAnaplanFSSTransformer


class WorkdayToAnaplanOrchestrator(AbstractOrchestrator):
    def __init__(self):
        self.workday_password = environ['password']  # os
        self.workday_username = environ['username']  # os


    def orchestrate(self):
        nodes = [WorkdayAPIConnector(), WorkdayToAnaplanFSSTransformer(), AnaplanApiConnector()]
        OrchestratorExecutor.execute(nodes)
