from bonobo.config import use_context

from integrations.orchestrators.abstract.orchestrated_task import OrchestratedTask
from integrations.orchestrators.orchestrator_data import OrchestratorData


class WorkdayToAnaplanFSSTransformer(OrchestratedTask):


    def execute(self, orchestrator_data=None) -> OrchestratorData:
        output_orchestrator_data = self.passthrough_inspector(orchestrator_data, "WorkdayToAnaplanFSSTransformer")
        return output_orchestrator_data