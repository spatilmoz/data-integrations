class OrchestratorData:
    input = output = None
    status = False

    def __init__(self, input=None, output=None, success=False):
        """
        Generate an OrchestratorData object from the provided parameters
        :param input: Input to the OrchestratedTask
        :param output: Output from the OrchestratedTask
        :param success: Status from the OrchestratedTask
        """
        self.success = success
        self.input = input
        self.output = output
