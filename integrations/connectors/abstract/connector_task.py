from abc import ABC, abstractmethod


class ConnectorTask(ABC):
    connection_params = {}

    def __init__(self):
        pass

    @abstractmethod
    def connect(self):
        ### Establish connection
        pass

    def fetch_data(self):
        ### Pull data from established connection
        print("Ability to fetch data, not yet implemented.")
        return None

    def push_data(self, orchestrator_data=None):
        ### Push data to established connection
        print("Ability to push data, not yet implemented.")
        return None

