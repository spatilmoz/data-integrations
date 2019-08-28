from integrations.orchestrators.orchestrator_data import OrchestratorData
from integrations.transformers.abstract.transformer_task import TransformerTask


class WorkdayToAnaplanFSSTransformer(TransformerTask):
    def __init__(self):
        pass

    def transform(self, orchestrator_data: OrchestratorData):
        print("Transforming Workday Reports to Anaplan syntax")
        orchestrator_data.output = "modified and transformed data"
        return orchestrator_data
