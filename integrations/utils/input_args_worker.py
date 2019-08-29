
class InputArgsWorker:
    def __init__(self, input_args):
        self.input_args = input_args
        self.data = {}

    def get_value(self, key):
        return self.data[key]