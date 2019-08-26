class OrchestratorData:
    input = output = status = None

    def __init__(self, input=None, output=None, success=False):
        self.success = success
        self.input = input
        self.output = output
