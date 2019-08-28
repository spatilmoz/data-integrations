class OrchestratorData:
    input = output = None
    status = False

    def __init__(self, input=None, output=None, success=False):
        self.success = success
        self.input = input
        self.output = output
