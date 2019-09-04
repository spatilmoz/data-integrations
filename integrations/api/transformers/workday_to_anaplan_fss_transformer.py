from integrations.api.orchestrators.orchestrator_data import OrchestratorData
from integrations.api.transformers.abstract.transformer_task import TransformerTask


class WorkdayToAnaplanFSSTransformer(TransformerTask):
    benefit_map = {0: "no", 1: "yes"}

    def transform(self, orchestrator_data: OrchestratorData):
        print("Transforming Workday Reports to Anaplan syntax")
        orchestrator_data.output = "modified and transformed data"
        return orchestrator_data

    def get_benefits(self, workday_data=None):
        wd_benefits = workday_data["benefits"]
        return self.benefit_map[wd_benefits]


