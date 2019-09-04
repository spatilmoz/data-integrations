from integrations.api.connectors.abstract.connector_push_task import ConnectorPushTask
from integrations.api.utils.sftp_worker import SftpWorker
import datetime
import os
import logging


class SalesforceSftpConnector(ConnectorPushTask):
    def __init__(self, bucket: str, dataset: str):
        self.bucket = bucket
        self.dataset = dataset
        current_ts = str(datetime.datetime.utcnow().isoformat())
        destination_dir = '-'.join(['etl/salesforce/encrypted', current_ts])
        self.destination_dir = destination_dir
        self.source_dir = '/tmp/'
        self.logger = logging.getLogger(__name__)

    def connect_push(self, orchestrator_data=None):
        print('INSIDE CONNECTOR PUSH')
        sftp = SftpWorker('mozilla.files.com', 'mcovarrubias@mozilla.com', 'Csupomona09!', self.source_dir, self.destination_dir,
                                  self.bucket, self.dataset)

        current_ts = str(datetime.datetime.utcnow().isoformat())
        destination_dir = '-'.join(['etl/salesforce/encrypted', current_ts])
        sftp.mkdir(destination_dir)
        for (dir_path, _, filename) in os.walk('/tmp/'):
            for name in filename:
                if name.endswith('.gpg'):
                    self.logger.info('Uploading {} to sftp server'.format(name))
                    sftp.upload_file(destination_dir=destination_dir,
                                     local_path=os.path.join(dir_path, name),
                                     remote_path=name)
        return orchestrator_data