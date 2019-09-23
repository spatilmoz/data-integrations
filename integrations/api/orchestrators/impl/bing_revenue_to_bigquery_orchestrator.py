from integrations.api.connectors.microsoft.bing_revenue_pull_connector import BingRevenuePullConnector
from integrations.api.orchestrators.abstract_orchestrator import AbstractOrchestrator
from integrations.api.orchestrators.orchestrator_executor import OrchestratorExecutor
from integrations.api.utils.input_args_worker import InputArgsWorker
from datetime import datetime, timedelta
from integrations.api.utils.local_config import LocalConfig

local_config = LocalConfig()

class BingRevenueToBigQueryOrchestrator(AbstractOrchestrator):

    def __init__(self, worker : InputArgsWorker):
        self.nodes = []
        self.__init_nodes()

    def __init_nodes(self):
        report_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
        bing_config = local_config['revenue']['bing']['config']['distribution']
        report_name = bing_config['report_name']
        report_type = bing_config['report_type']
        granularity = bing_config['granularity']
        columns = bing_config['columns']
        self.nodes.append(BingRevenuePullConnector(start_date = report_date, end_date = report_date, report_name =report_name,
                                                   report_type= report_type, granularity= granularity, columns = columns))

    def orchestrate(self):
        OrchestratorExecutor.execute(self.nodes)

    @staticmethod
    def get_pipeline_key() -> str:
        return 'bing_revenue_to_big_query'

    @staticmethod
    def is_pipeline_key(pipeline_key: str):
        return pipeline_key == BingRevenueToBigQueryOrchestrator.get_pipeline_key()