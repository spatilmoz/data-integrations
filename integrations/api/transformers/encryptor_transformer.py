from integrations.api.orchestrators.orchestrator_data import OrchestratorData
from integrations.api.transformers.abstract.transformer_task import TransformerTask
import logging
import os
import json
from integrations.api.utils.gpg_worker import GpgWorker


class EncryptorTransformer(TransformerTask):
    
    def __init__(self, encrypted_dir: str):
        self.public_key_url = json.load(open(os.environ.get('CONFIG'))).get('gpg_public_key_url')
        self.encrypted_dir = encrypted_dir
        self.logger = logging.getLogger(__name__)
        self.gpg_worker = GpgWorker(self.public_key_url, self.encrypted_dir)

    def transform(self, orchestrator_data: OrchestratorData):
        for (root, dirs, files) in os.walk(self.encrypted_dir):
            for filename in files:
                if filename.endswith('.gz'):
                    self.gpg_worker.encrypt(filename)
        return orchestrator_data
