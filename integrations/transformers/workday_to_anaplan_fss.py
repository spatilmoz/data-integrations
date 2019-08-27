from bonobo.config import use_context

from integrations.orchestrators import orchestrator_data
from integrations.orchestrators.abstract.orchestrated_task import OrchestratedTask
from integrations.orchestrators.orchestrator_data import OrchestratorData


class WorkdayToAnaplanFSSTransformer(OrchestratedTask):
    def transform(self, orchestrator_data: OrchestratorData):
        print("Transforming Workday Reports to Anaplan syntax")
        orchestrator_data.output = "modified and transformed data"
        return orchestrator_data

    def execute(self, input_data=None) -> OrchestratorData:
        output_orchestrator_data = self.passthrough_inspector(orchestrator_data=input_data, key="WorkdayToAnaplanFSSTransformer")
        return self.transform(output_orchestrator_data)