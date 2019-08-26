from abc import ABC, abstractmethod


class OrchestratedTask(ABC):
    @abstractmethod
    def execute(self, input_data=None):
        pass  # should return output_data
