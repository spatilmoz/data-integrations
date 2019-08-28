from integrations.orchestrators.gcp_storage_to_salesforce_sftp_orchestrator import \
    GcpStorageToSalesforceSftpOrchestrator
from integrations.orchestrators.workday_to_anaplan_orchestrator import WorkdayToAnaplanOrchestrator


class Orchestrators():
    @staticmethod
    def orchestrator_map():
        '''
        This method will return a dictionary of key->orchestrator map. The key here should be the same as the key
        provided to airflow via the Controller.py call.
        :return:
        '''
        class_orchestrator_map = dict()
        class_orchestrator_map["WorkdayToAnaplan_FinancialSystemServices"] = WorkdayToAnaplanOrchestrator()
        class_orchestrator_map["gcp_storage_to_salesforce_sftp"] = GcpStorageToSalesforceSftpOrchestrator()
        return class_orchestrator_map


