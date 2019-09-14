# import pickle
# import os.path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from google.oauth2 import service_account
# import googleapiclient.discovery
from integrations.api.connectors.abstract.connector_pull_task import ConnectorPullTask

class GoogleSheetConnector(ConnectorPullTask):
    def __init__(self, sheet_id):
        self.sheet_id = sheet_id
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        self.sample_range_name = 'Current!AF3:AO5'

    def read(self):
        pass
        # credentials = service_account.Credentials.from_service_account_file(
        #     SERVICE_ACCOUNT_FILE, scopes=self.scopes)
        # sqladmin = googleapiclient.discovery.build('sqladmin', 'v1beta3', credentials=credentials)



        # creds = None
        # # The file token.pickle stores the user's access and refresh tokens, and is
        # # created automatically when the authorization flow completes for the first
        # # time.
        # # if os.path.exists('token.pickle'):
        # #     with open('token.pickle', 'rb') as token:
        # #         creds = pickle.load(token)
        # # If there are no (valid) credentials available, let the user log in.
        # if not creds or not creds.valid:
        #     if creds and creds.expired and creds.refresh_token:
        #         creds.refresh(Request())
        #     else:
        #         flow = InstalledAppFlow.from_client_secrets_file(os.environ['GOOGLE_SHEET_CREDENTIALS'], self.scopes)
        #         flow.fetch_token()
        #         creds = flow.authorized_session()
        #         creds = flow.run_local_server(port=0)
        #     # Save the credentials for the next run
        #     with open('token.pickle', 'wb') as token:
        #         pickle.dump(creds, token)
        #
        # service = build('sheets', 'v4', credentials=creds)
        #
        # # Call the Sheets API
        # sheet = service.spreadsheets()
        # result = sheet.values().get(spreadsheetId=self.sheet_id,
        #                             range=self.sample_range_name).execute()
        # values = result.get('values', [])
        #
        # if not values:
        #     print('No data found.')
        # else:
        #     print('Name, Major:')
        #     for row in values:
        #         # Print columns A and E, which correspond to indices 0 and 4.
        #         print('%s, %s' % (row[0], row[4]))
