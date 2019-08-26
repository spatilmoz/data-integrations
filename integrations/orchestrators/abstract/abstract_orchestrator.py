from abc import ABC, abstractmethod

class AbstractOrchestrator(ABC):

    @abstractmethod
    def orchestrate(self):
        pass
