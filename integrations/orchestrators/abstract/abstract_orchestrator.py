from abc import ABC, abstractmethod


class AbstractOrchestrator(ABC):
    @property
    @abstractmethod
    def internal_ordered_tasks(self):
        return []

    @property
    def ordered_tasks(self):
        if not self.internal_ordered_tasks:
            raise NotImplementedError
        return self.internal_ordered_tasks

    def orchestrate(self):
        # After OrchestratedTasks are added to the internal_ordered_tasks
        # calling the orchestrate method will cycle between the constructed tasks.
        # Connectors, Transformers, etc can inherit from OrchestratedTask and then
        # be called through here after implementing the execute method.
        # The data will be passed through the tasks.
        task_data = None
        for task in self.ordered_tasks:
            task_data = task.execute(task_data)

        return task_data