from integrations.orchestrators.orchestrator_data import OrchestratorData
from integrations.transformers.abstract.transformer_task import TransformerTask


class ComsolidateCsvFilesTransformer(TransformerTask):
    def transform(self, orchestrator_data: OrchestratorData):
        return orchestrator_data

