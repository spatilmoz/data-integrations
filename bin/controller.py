#!/usr/bin/env python3
from __future__ import division
import argparse

from integrations.orchestrators.orchestrator_selector import OrchestratorSelector


class Controller:
    """
    The Controller class will take input parameter (an Orchestrator key) from provided arguments when called.
    OrchestratorSelector is used to determine the proper Orchestrator that is being triggered. The Orchestrator will use
    the ordered_tasks to determine the OrchestratedTasks that need to be run.
    """
    def __init__(self):
        parser = argparse.ArgumentParser(description="Main Controller to determine pipeline and orchestration")
        parser.add_argument('--pipeline', dest='pipeline', help='the key mapping to the orchestrator')
        parser.add_argument('--bucket', dest='bucket', help='storage for temporary storage')
        parser.add_argument('--dataset', dest='dataset', help='dataset name to be exported')
        parser.add_argument('--file_extension', dest='file_extension', help='file extension of extracted data')
        parser.add_argument('--location', dest='location', help='location of dataset')
        self.args = parser.parse_args()
        self.orchestrator = OrchestratorSelector(self.args)

    def initialize(self):
        self.orchestrator.delegate_orchestration()


if __name__ == "__main__":
    main_controller = Controller()
    main_controller.initialize()
