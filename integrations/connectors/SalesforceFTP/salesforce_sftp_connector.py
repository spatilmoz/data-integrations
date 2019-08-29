from integrations.connectors.abstract.connector_push_task import ConnectorPushTask
from integrations.utils.sftp_worker import SftpWorker
import datetime


class SalesforceSftpConnector(ConnectorPushTask):
    def __init__(self, bucket: str, dataset: str):
        self.bucket = bucket
        self.dataset = dataset
        current_ts = str(datetime.datetime.utcnow().isoformat())
        destination_dir = '-'.join(['etl/salesforce/encrypted', current_ts])
        self.destination_dir = destination_dir
        self.source_dir = '/tmp/t/'

    def connect_push(self, orchestrator_data=None):
        sftp_worker = SftpWorker('mozilla.files.com', 'mcovarrubias@mozilla.com', 'Csupomona09!', self.source_dir, self.destination_dir,
                                 self.bucket, self.dataset)
        sftp_worker.transfer()
        return orchestrator_data