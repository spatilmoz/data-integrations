from integrations.api.orchestrators.impl.bigquery_to_storage_orchestrator import BigQueryToStorageOrchestrator
from integrations.api.orchestrators.impl.gcp_storage_to_salesforce_sftp_orchestrator import GcpStorageToSalesforceSftpOrchestrator
from integrations.api.orchestrators.impl.workday_to_anaplan_orchestrator import WorkdayToAnaplanOrchestrator
from integrations.api.orchestrators.impl.gcp_cleanup_orchestrator import GcpCleanupOrchestrator
from integrations.api.utils.input_args_worker import InputArgsWorker


class OrchestratorSelector:
    def __init__(self, input_args=None):
        self.worker = InputArgsWorker(input_args)

    def delegate_orchestration(self):
        if 'financial_workday_to_anaplan' == self.worker.get_value('pipeline'):
            WorkdayToAnaplanOrchestrator().orchestrate()

        elif 'marketing_storage_to_salesforce' == self.worker.get_value('pipeline'):
            GcpStorageToSalesforceSftpOrchestrator(self.worker.get_value('bucket'),
                                                   self.worker.get_value('dataset'),
                                                   self.worker.get_value('source_dir'),
                                                   self.worker.get_value('destination_dir')).orchestrate()

        elif 'marketing_bq_to_storage' == self.worker.get_value('pipeline'):
            BigQueryToStorageOrchestrator(self.worker.get_value('bucket'),
                                          self.worker.get_value('dataset'),
                                          self.worker.get_value('file_extension'),
                                          self.worker.get_value('location')).orchestrate()

        elif 'marketing_cleanup' == self.worker.get_value('pipeline'):
            GcpCleanupOrchestrator(self.worker.get_value('bucket'),
                                   self.worker.get_value('dataset')).orchestrate()