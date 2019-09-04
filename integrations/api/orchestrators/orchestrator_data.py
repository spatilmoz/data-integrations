class OrchestratorData:
    def __init__(self, input=None, output=None, success=True):
        """
        Generate an OrchestratorData object from the provided parameters
        :param input: Input to the AbstractOrchestratorTask
        :param output: Output from the AbstractOrchestratorTask
        :param success: Status from the AbstractOrchestratorTask
        """
        self.success = success
        self.input = input
        self.output = output
