from os import environ

from integrations.api.connectors.Anaplan.anaplan_api_connector import AnaplanApiConnector
from integrations.api.connectors.Workday.workday_api_connector import WorkdayAPIConnector
from integrations.api.orchestrators.abstract_orchestrator import AbstractOrchestrator
from integrations.api.orchestrators.orchestrator_executor import OrchestratorExecutor
from integrations.api.transformers.workday_to_anaplan_fss_transformer import WorkdayToAnaplanFSSTransformer


class WorkdayToAnaplanOrchestrator(AbstractOrchestrator):
    def __init__(self):
        self.workday_password = environ['password']  # os
        self.workday_username = environ['username']  # os


    def orchestrate(self):
        nodes = [WorkdayAPIConnector(), WorkdayToAnaplanFSSTransformer(), AnaplanApiConnector()]
        OrchestratorExecutor.execute(nodes)
