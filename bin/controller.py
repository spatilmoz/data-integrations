#!/usr/bin/env python3

from __future__ import division

import argparse

# Controller takes parameter to pass to pipeline.
# Orchestrator determines the proper .
# Orchestrator uses proper Connectors and
from integrations.orchestrators.orchestration_selector import Orchestration_Selector


class Controller:
    orchestrator = None
    args = None

    def __init__(self):
        parser = argparse.ArgumentParser(description="Main Controller to determine pipeline and orchestration")
        parser.add_argument('--pipeline-keyword', action='pipeline', help='the date to retrieve')
        self.args = parser.parse_args()
        self.orchestrator = Orchestration_Selector(self.args)
        #self.orchestrator = Orchestration_Selector()

    def initialize(self):
        #self.orchestrator.select_orchestrator(self.args)
        self.orchestrator.delegate_orchestration()


if __name__ == "__main__":
    main_controller = Controller()
    main_controller.initialize()
