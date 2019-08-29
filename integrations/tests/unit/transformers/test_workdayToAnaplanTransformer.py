from integrations.orchestrators.orchestrationselector import OrchestrationSelector
import unittest
from unittest.mock import Mock, MagicMock, PropertyMock
import logging

from integrations.orchestrators.orchestrator_data import OrchestratorData
from integrations.transformers.abstract.transformer_task import TransformerTask
from integrations.transformers.workday_to_anaplan_fss_transformer import WorkdayToAnaplanFSSTransformer


class MockTransformer(TransformerTask):
    def transform(self, orchestrator_data: OrchestratorData):
        raise Exception


class Tester(unittest.TestCase):
    def test_mocked_transformer(self):
        test_orchestrator_data = OrchestratorData()
        transformer = Mock(return_value=MockTransformer())
        with self.assertRaises(Exception):
            transformer().transform(test_orchestrator_data)

    def test_transformed_data(self):
        test_orchestrator_data = OrchestratorData()
        transformer = WorkdayToAnaplanFSSTransformer()
        self.assertIsNone(test_orchestrator_data.input)
        self.assertIsNone(test_orchestrator_data.output)
        self.assertFalse(test_orchestrator_data.success)
        transformer.transform(test_orchestrator_data)

        self.assertIsNotNone(test_orchestrator_data.output)

    def test_workday_report_transformed(self):
        test_orchestrator_data = OrchestratorData()
        transformer = WorkdayToAnaplanFSSTransformer()
        transformer.transform(test_orchestrator_data)

if __name__ =="__main__":
    unittest.main()