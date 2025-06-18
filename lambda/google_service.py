from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
]
SERVICE_ACCOUNT_FILE = "service_account.json"


def get_credentials():
    print("Loading Google service account credentials...")
    return service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )


CREDENTIALS = get_credentials()


def get_sheet_service():
    print("Initializing Google Sheets service...")
    return build("sheets", "v4", credentials=CREDENTIALS).spreadsheets()


SHEET_SERVICE = get_sheet_service()


def get_calendar_service():
    print("Initializing Google Calendar service...")
    return build("calendar", "v3", credentials=CREDENTIALS)


CALENDAR_SERVICE = get_calendar_service()
