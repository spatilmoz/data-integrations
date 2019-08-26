from integrations.orchestrators.abstract.orchestrated_task import OrchestratedTask


class WorkdayToAnaplanFSS(OrchestratedTask):
    def transform(self, input_data):
        print("Transforming data from Workday to Anaplan")
        return input_data

    def execute(self, input_data=None):
        return self.transform(input_data)