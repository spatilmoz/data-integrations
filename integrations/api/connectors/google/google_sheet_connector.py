
class GoogleSheetConnector:
    def __init__(self, sheet_id):
        self.sheet_id = sheet_id
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        self.sample_range_name = 'Current!AF3:AO5'

    def read(self):
        pass