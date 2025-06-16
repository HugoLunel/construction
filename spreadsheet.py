from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build

DATE_FORMAT = "%d/%m/%Y %H:%M:%S"

def get_date(data: list, index: int, job_date: str) -> datetime:
    return datetime.strptime(f"{job_date} {data[index]}", DATE_FORMAT)


@dataclass
class SpreedsheetEntry:
    title: str
    start: datetime
    end: datetime
    duration_hours: float
    submitter: str
    submitted_at: datetime
    @classmethod
    def from_row(cls, data: list) -> Optional["SpreedsheetEntry"]:
        try:
            job_date = data[1]
            start = get_date(data, 3, job_date)
            end = get_date(data, 4, job_date)
            submitted_at = datetime.strptime(data[0], DATE_FORMAT)
            return cls(
                title=data[5],
                start=start,
                end=end,
                submitter=data[2],
                submitted_at=submitted_at,
                duration_hours=(end - start).total_seconds() / 3600,
            )
        except Exception as e:
            print(f"Error processing row {data}: {e}")
            return None


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
]
SERVICE_ACCOUNT_FILE = "service_account.json"
SPREADSHEET_ID = "1xqBjVJxNfW_U6Bg5sbtc6PlALxdQKt1oSiUMBZ_xPRA"
RANGE = "Form responses 1!A2:F"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build("sheets", "v4", credentials=credentials)

sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()

entries = [
    SpreedsheetEntry.from_row(row)
    for row in result.get("values", [])
    if SpreedsheetEntry.from_row(row) is not None
]
print("Spreadsheet values:", entries)
