from bonobo.config import use_context

from integrations.orchestrators.abstract.orchestrated_task import OrchestratedTask

class WorkdayToAnaplanFSSTransformer(OrchestratedTask):


    def execute(self, input_data=None):
        # This method should do the necessary steps for the Connector
        # if input_data is not None:
        #     print(input_data)
        #     raise Exception("Not expecting input_data for pulling from Workday SFTP Connector (at this time).")
        #
        # self.connect()
        # yield {self.fetch_data()}
        print("WorkdayToAnaplanFSSTransformer")
