from integrations.orchestrators.abstract.orchestrators_enum import Orchestrators


class Orchestration_Selector:
    arg_map = dict()  # Arg map will be used to determine parameter to corresponding action
    selected_orchestrator = None

    def __init__(self, input_args=None):
        self.arg_map = Orchestrators.orchestrator_map()
        if input_args is not None:
            self.select_orchestrator(input_args)

    def select_orchestrator(self, input_args):
        if self.selected_orchestrator is not None:
            return self.selected_orchestrator
        orchestrator_key = self.__extract_orchestrator_key(input_args)
        self.selected_orchestrator = chosen_orchestrator = self.__retrieve_chosen_orchestrator(orchestrator_key)
        return chosen_orchestrator

    def __extract_orchestrator_key(self, input_args):
        # Extract key from passed in parameters
        extracted_key = input_args = "WorkdayToAnaplan_FinancialSystemServices"
        return extracted_key

    def __retrieve_chosen_orchestrator(self, orchestrator_key):
        # Determine correct Orchestrator
        if not self.arg_map:
            raise NotImplementedError
        return self.arg_map[orchestrator_key]

    def delegate_orchestration(self, input_args=None):
        if self.selected_orchestrator is None:
            if input_args is not None:
                self.select_orchestrator(input_args)
            else:
                raise Exception("Delegation attempted without selecting Orchestrator.")

        self.selected_orchestrator.orchestrate()
