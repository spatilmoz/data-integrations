import logging
from abc import ABC, abstractmethod

class AbstractOrchestrator(ABC):
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)

    @abstractmethod
    def orchestrate(self, input_args=None):
        pass
