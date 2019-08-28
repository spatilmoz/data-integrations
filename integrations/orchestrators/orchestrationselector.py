from integrations.orchestrators.abstract.abstract_orchestrator import AbstractOrchestrator
from integrations.orchestrators.abstract.orchestrators_enum import Orchestrators


class OrchestrationSelector:
    """
    This class is used to provide the Controller with the expected Orchestrator
    """
    def __init__(self, input_args=None):
        self.argument_to_orchestrator_map = Orchestrators.orchestrator_map()
        self.selected_orchestrator = None
        if input_args is not None:
            self.select_orchestrator(input_args)

    def delegate_orchestration(self, input_args=None):
        '''
        This method runs the orchestrator's pipeline of OrchestratedTasks
        :param input_args: Optional, if not filled in on construction
        :return:
        '''
        if self.selected_orchestrator is None:
            if input_args is not None:
                self.select_orchestrator(input_args)
            else:
                raise Exception("Delegation attempted without selecting Orchestrator.")

        self.selected_orchestrator.orchestrate()

    def select_orchestrator(self, input_args):
        '''
        Determine the Orchestrator based on the input_args
        :param input_args: Expected key that maps to corresponding Orchestrator
        :return: Orchestrator to be run downstream
        '''
        if self.selected_orchestrator is not None:
            return self.selected_orchestrator
        orchestrator_key = self.__extract_orchestrator_key(input_args)
        self.selected_orchestrator = self.__retrieve_chosen_orchestrator(orchestrator_key)
        return self.selected_orchestrator

    def __extract_orchestrator_key(self, input_args):
        """
        The input_args is expected to come with orchestrator_key, otherwise we are unable to determine the correct
        Orchestrator.
        :param input_args:
        :return:
        """
        if None is input_args.orchestrator_key:
            raise Exception("Cannot extract key from provided input")
        extracted_key = input_args.orchestrator_key
        return extracted_key

    def __retrieve_chosen_orchestrator(self, orchestrator_key) -> AbstractOrchestrator:
        """
        Using argument_to_orchestrator_map and provided key to return Orchestrator
        :param orchestrator_key: key provided for map
        :return AbstractOrchestrator: a child class that implements the AbstractOrchestrator
        """
        if not self.argument_to_orchestrator_map:
            raise NotImplementedError
        return self.argument_to_orchestrator_map[orchestrator_key]
