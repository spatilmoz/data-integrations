from abc import ABC, abstractmethod

from bonobo.config import use_context

from integrations.orchestrators.orchestrator_data import OrchestratorData


class OrchestratedTask(ABC):

    @abstractmethod
    def execute(self, orchestrator_data=None) -> OrchestratorData:
        pass  # should return output_data

    @use_context
    def __call__(self, *args, **kwargs):
        prev_orchestrator_data = self.execute(*args)
        if prev_orchestrator_data.success:
            next_orchestrator_data = OrchestratorData(input=prev_orchestrator_data.output)
            return next_orchestrator_data
        else:
            self.terminate()

    def terminate(self):
        return  # Return nothing to terminate

    def passthrough_inspector(self, orchestrator_data, key="testKey"):
        output_orchestrator_data = OrchestratorData()
        if orchestrator_data is None:
            print("No input data found in ", key)
        else:
            print("Found input data from previous task: ", str(orchestrator_data.input))
            output_orchestrator_data.input = orchestrator_data.input

        output_orchestrator_data.output = key
        output_orchestrator_data.success = True
        return output_orchestrator_data
