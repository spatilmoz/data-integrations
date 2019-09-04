class InputArgsWorker:
    def __init__(self, input_args):
        self.data = vars(input_args)

    def get_value(self, key):
        return self.data[key]