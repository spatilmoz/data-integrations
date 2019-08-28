from integrations.orchestrators.orchestration_selector import Orchestration_Selector
import unittest
from unittest.mock import Mock, MagicMock, PropertyMock
import logging
from integrations.orchestrators.workday_to_anaplan_orchestrator import WorkdayToAnaplanOrchestrator

class MockOrchestrator():
    def orchestrate(self):
        raise Exception


class Tester(unittest.TestCase):
    def test_mocked_orchestrator(self):
        input_args = ""
        orchestrator = Orchestration_Selector()
        orchestrator.arg_map["WorkdayToAnaplan_FinancialSystemServices"] = Mock(return_value=MockOrchestrator())
        orchestrator.select_orchestrator(input_args)

    def test_no_orchestrator_found(self):
        input_args = ""
        orchestrator = Orchestration_Selector()
        orchestrator.arg_map = None
        with self.assertRaises(NotImplementedError):
            orchestrator.select_orchestrator(input_args)

    def test_no_orchestrator_selected(self):
        input_args = ""
        orchestrator = Orchestration_Selector()
        orchestrator.arg_map = None
        with self.assertRaises(Exception):
            orchestrator.delegate_orchestration(input_args)

    def test_no_orchestrator_selected_passed_input(self):
        input_args = "WorkdayToAnaplan-FinancialSystemServices"
        orchestrator = Orchestration_Selector()
        orchestrator.delegate_orchestration(input_args)


if __name__ =="__main__":
    unittest.main()