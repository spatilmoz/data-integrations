from integrations.api.orchestrators.orchestrator_data import OrchestratorData
from integrations.api.transformers.abstract.transformer_task import TransformerTask
from integrations.api.config.app_configuration import config
import logging
import os
from integrations.api.utils.gpg_worker import GpgWorker


class EncryptorTransformer(TransformerTask):
    
    def __init__(self, encrypted_dir: str):
        self.public_key_url = config['gpg'].get('gpg_public_key_url')
        self.encrypted_dir = encrypted_dir
        self.logger = logging.getLogger(__name__)
        self.gpg_worker = GpgWorker(self.public_key_url, self.encrypted_dir)

    def transform(self, orchestrator_data: OrchestratorData):
        for (root, dirs, files) in os.walk(self.encrypted_dir):
            for filename in files:
                if filename.endswith('.csv'):
                    print(filename)
                    self.gpg_worker.encrypt(filename)
        return orchestrator_data