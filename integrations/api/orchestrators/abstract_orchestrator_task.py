from abc import ABC, abstractmethod
import logging

from integrations.api.orchestrators.orchestrator_data import OrchestratorData


class AbstractOrchestratorTask(ABC):
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)

    @abstractmethod
    def execute(self, orchestrator_data=None) -> OrchestratorData:
        """
        This method will be overridden by the children of this class. Please view AbstractOrchestratorTask.__call__ method
        for more background.
        :param orchestrator_data: If provided the OrchestratorData might contain input to use in
        this task step.
        :return OrchestratorData: If success, returns OrchestratorData object with
        OrchestratorData.output, OrchestratorData.success, and OrchestratorData.input (the OrchestratorData.input
        provided); if failure, should be handled gracefully and respond with a False for OrchestratorData.success
        """
        pass  #

    def __call__(self, *args, **kwargs) -> OrchestratorData:
        """
        This is the entry point for bonobo to access the children of this abstract class. After the children classes
        implement the abstract execute method. This will take the provided input args and pass them to the execute
        method, if a child task returns with a success response the data will be passed to the next task. The current
        task then creates a new OrchestrationData with the current task's orchestrator_data.output as the next task's
        orchestrator_data.input. This object is provided to the next task as input.
        :param args:
        :param kwargs:
        :return OrchestratorData: This contains the input to the next task for bonobo or termination of the sequence
        """
        prev_orchestrator_data = self.execute(*args)
        logging.debug("...Received success message from task.")

        if not prev_orchestrator_data:
            prev_orchestrator_data = OrchestratorData()

        next_orchestrator_data = OrchestratorData(input=prev_orchestrator_data.output)
        return next_orchestrator_data

    def terminate(self):
        """
        In bonobo return <blank> is a way to terminate the pipeline
        :return: When called should be returned to trigger pipeline termination.
        """
        return
