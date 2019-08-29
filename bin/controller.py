#!/usr/bin/env python3
from __future__ import division
import argparse

from integrations.orchestrators.orchestrationselector import OrchestrationSelector


class Controller:
    """
    The Controller class will take input parameter (an Orchestrator key) from provided arguments when called.
    OrchestratorSelector is used to determine the proper Orchestrator that is being triggered. The Orchestrator will use
    the ordered_tasks to determine the OrchestratedTasks that need to be run.
    """
    def __init__(self):
        parser = argparse.ArgumentParser(description="Main Controller to determine pipeline and orchestration")
        parser.add_argument('--orchestrator-key', dest='orchestrator_key', help='the key mapping to the orchestrator')
        self.args = parser.parse_args()
        self.orchestrator = OrchestrationSelector(self.args)

    def initialize(self):
        self.orchestrator.delegate_orchestration()


if __name__ == "__main__":
    main_controller = Controller()
    main_controller.initialize()
