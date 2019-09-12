from behave import *

from integrations.api.connectors.google.google_sheet_connector import GoogleSheetConnector


class GoogleSheetToBQStep:

    @when('we invoke a google sheet with this google sheet id {sheet_id}')
    def step_impl(context, sheet_id: str):
        GoogleSheetConnector(sheet_id).read()

    @then("I receive a google sheet response")
    def step_impl(context):
        pass


