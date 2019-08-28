import logging
from abc import ABC, abstractmethod
import bonobo


class AbstractOrchestrator(ABC):
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)

    @abstractmethod
    def list_of_ordered_orchestrated_tasks(self):
        """
        For default orchestration this list of ordered tasks will be used in the order provided through bonobo.
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def dict_of_services(self):
        """
        For default orchestration this dictionary of services will be used to provide services to bonobo.
        :return:
        """
        raise NotImplementedError

    def get_graph(self):
        '''
        Defaulting to a generic graph provided by bonobo, using the list_of_ordered_orchestrated_tasks
        :return:
        '''
        graph = bonobo.Graph()
        graph.add_chain(self.list_of_ordered_orchestrated_tasks)
        return graph

    def get_services(self):
        """
        Helper method for bonobo to access child dictionary of services
        :return: dictionary for bonobo for services
        """
        return self.dict_of_services()

    def orchestrate(self, input_args=None):
        """
        This method is used to initiate the bonobo runs as expected.
        :param input_args:
        :return:
        """
        bonobo.run(
            self.get_graph(),
            services=self.get_services())