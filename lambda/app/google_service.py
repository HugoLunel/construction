import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import boto3

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
]
SERVICE_ACCOUNT_SECRET_KEY = "construction/google-service-account"


def get_credentials():
    print("Loading Google service account credentials...")
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager", 
        region_name=os.environ["AWS_REGION"],
    )
    import json
    secret = client.get_secret_value(SecretId=SERVICE_ACCOUNT_SECRET_KEY)[
        "SecretString"
    ]
    secret_dict = json.loads(secret)
    return service_account.Credentials.from_service_account_info(secret_dict, scopes=SCOPES)


CREDENTIALS = get_credentials()


def get_sheet_service():
    print("Initializing Google Sheets service...")
    return build("sheets", "v4", credentials=CREDENTIALS).spreadsheets()


SHEET_SERVICE = get_sheet_service()


def get_calendar_service():
    print("Initializing Google Calendar service...")
    return build("calendar", "v3", credentials=CREDENTIALS)


CALENDAR_SERVICE = get_calendar_service()
