import unittest
from unittest.mock import Mock

from integrations.orchestrators.orchestrationselector import OrchestrationSelector


class MockOrchestrator():
    def orchestrate(self):
        raise c


class MockArgParsed():
    @property
    def orchestrator_key(self):
        raise Exception


class Tester(unittest.TestCase):
    input_args = Mock(return_value=MockArgParsed())
    input_args.orchestrator_key = "WorkdayToAnaplan_FinancialSystemServices"

    def test_mocked_orchestrator(self):
        orchestrator = OrchestrationSelector()
        orchestrator.argument_to_orchestrator_map["WorkdayToAnaplan_FinancialSystemServices"] = Mock(return_value=MockOrchestrator())()
        with self.assertRaises(Exception):
            orchestrator.delegate_orchestration(self.input_args)

    def test_no_orchestrator_found(self):
        orchestrator = OrchestrationSelector()
        orchestrator.argument_to_orchestrator_map = None
        with self.assertRaises(NotImplementedError):
            orchestrator.select_orchestrator(self.input_args)

    def test_no_orchestrator_selected(self):
        orchestrator = OrchestrationSelector()
        orchestrator.argument_to_orchestrator_map = None
        with self.assertRaises(Exception):
            orchestrator.delegate_orchestration(self.input_args)

    def test_no_orchestrator_selected_passed_input(self):
        orchestrator = OrchestrationSelector()
        orchestrator.delegate_orchestration(self.input_args)

    def test_orchestrator_selected_passed_input(self):
        orchestrator = OrchestrationSelector(self.input_args)
        orchestrator.delegate_orchestration()


if __name__ == "__main__":
    unittest.main()
