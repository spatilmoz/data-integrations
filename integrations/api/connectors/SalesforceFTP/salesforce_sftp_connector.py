from integrations.api.connectors.abstract.connector_push_task import ConnectorPushTask
from integrations.api.utils.sftp_worker import SftpWorker
from integrations.api.config.app_configuration import config
import datetime
import os
import logging


class SalesforceSftpConnector(ConnectorPushTask):

    def __init__(self, source_dir: str, destination_dir: str):
        self.host = config['sftp'].get('sftp_host')
        self.username = config['sftp'].get('sftp_username')
        self.password = config['sftp'].get('sftp_password')
        self.source_dir = source_dir
        self.destination_dir = destination_dir
        self.logger = logging.getLogger(__name__)

    def connect_push(self, orchestrator_data=None):
        sftp = SftpWorker(host=self.host,
                          username=self.username,
                          password=self.password,
                          source_dir=self.source_dir,
                          destination_dir=self.destination_dir)

        current_ts = str(datetime.datetime.utcnow().isoformat())
        destination_dir = '-'.join([self.destination_dir, current_ts])
        sftp.mkdir(destination_dir)
        for (dir_path, _, filename) in os.walk(self.source_dir):
            for name in filename:
                if name.endswith('.enc'):
                    self.logger.info('Uploading {} to sftp server'.format(name))
                    sftp.upload_file(destination_dir=destination_dir,
                                     local_path=os.path.join(dir_path, name),
                                     remote_path=name)
        return orchestrator_data