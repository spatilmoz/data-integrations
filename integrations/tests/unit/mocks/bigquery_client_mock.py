class BigqueryClientMock():
    def __init__(self, tables=[]):
        self.tables = tables

    def list_tables(self,dataset : str):
        return self.tables

    def get_dataset(self, dataset_id: str):
        return 'dataset'

    def extract_table(self,bucket_name, dataset_id, table_id,file_extension,location):
        pass