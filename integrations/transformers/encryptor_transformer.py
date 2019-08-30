from integrations.orchestrators.orchestrator_data import OrchestratorData
from integrations.transformers.abstract.transformer_task import TransformerTask
import logging
import os

from integrations.utils.gcp_worker import GcpWorker
from integrations.utils.gpg_worker import GpgWorker


class EncryptorTransformer(TransformerTask):
    def __init__(self, bucket: str, dataset: str):
        self.public_key_url = 'https://members.exacttarget.com/Content/Subscribers/SubsLists/publickey.txt'
        self.public_key_id = '64C4D5362A88CF19'
        self.encrypted_dir = '/tmp/t'
        self.bucket = bucket
        self.dataset = dataset
        self.logger = logging.getLogger(__name__)

    def transform(self, orchestrator_data: OrchestratorData):
        # gpg_worker = GpgWorker(self.public_key_url, self.public_key_id, self.encrypted_dir, self.bucket)
        # gcp_worker = GcpWorker(self.bucket, self.dataset)
        # prefix = self.dataset
        # for blob in gcp_worker.list_blobs(prefix=prefix):
        #     gpg_worker.encrypt(blob.name)
        return orchestrator_data