from enum import Enum
from collections import namedtuple

from integrations.orchestrators.workday_to_anaplan_orchestrator import WorkdayToAnaplanOrchestrator

Orchestrator = namedtuple('__Orchestrator', ['key_orchestrator', 'entity_orchestrator'])


class Orchestrators(Enum):
    @property
    def entity_orchestrator(self):
        return self.value.entity_orchestrator

    @property
    def key_orchestrator(self):
        return self.value.key_orchestrator

    @staticmethod
    def orchestrator_map():
        class_orchestrator_map = {}
        for key_orchestrator, entity_orchestrator in Orchestrators.__members__.items():
            class_orchestrator_map[key_orchestrator] = entity_orchestrator
        return class_orchestrator_map

    WorkdayToAnaplan_FinancialSystemServices = Orchestrator("WorkdayToAnaplan_FinancialSystemServices",
                                                            WorkdayToAnaplanOrchestrator())
