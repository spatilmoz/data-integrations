import logging
from abc import ABC, abstractmethod
import bonobo


class AbstractOrchestrator(ABC):
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)

    @abstractmethod
    def list_of_ordered_orchestrated_tasks(self):
        raise NotImplementedError

    @abstractmethod
    def dict_of_services(self):
        raise NotImplementedError

    def get_graph(self):
        graph = bonobo.Graph()
        graph.add_chain(self.list_of_ordered_orchestrated_tasks)
        return graph

    def get_services(self):
        return self.dict_of_services()

    def orchestrate(self, input_args=None):
        bonobo.run(
            self.get_graph(),
            services=self.get_services())