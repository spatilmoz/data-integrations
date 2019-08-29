from integrations.orchestrators.gcp_storage_to_salesforce_sftp_orchestrator import GcpStorageToSalesforceSftpOrchestrator
from integrations.orchestrators.workday_to_anaplan_orchestrator import WorkdayToAnaplanOrchestrator
from integrations.utils.input_args_worker import InputArgsWorker


class OrchestrationSelector:
    def __init__(self, input_args=None):
        self.worker = InputArgsWorker(input_args)

    def delegate_orchestration(self):
        if 'financial_workday_to_anaplan' == self.worker.get_value('pipeline'):
            WorkdayToAnaplanOrchestrator().orchestrate()
        elif 'marketing_bq_to_salesforce' == self.worker.get_value('pipeline'):
            GcpStorageToSalesforceSftpOrchestrator(self.worker.get_value('bucket'), self.worker.get_value('dataset')).orchestrate()
