from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import pytz

from google_service import SHEET_SERVICE

DATE_FORMAT = "%d/%m/%Y %H:%M:%S"

LONDON_TZ = pytz.timezone("Europe/London")


def get_date(datetime_str: str) -> datetime:
    dt = datetime.strptime(datetime_str, DATE_FORMAT)
    if dt.tzinfo is None:
        dt = LONDON_TZ.localize(dt)
    return dt


@dataclass
class SpreadsheetEntry:
    title: str
    start: datetime
    end: datetime
    duration_hours: float
    submitter: str
    submitted_at: datetime

    @classmethod
    def from_row(cls, data: list) -> Optional["SpreadsheetEntry"]:
        try:
            job_date = data[1]
            start = get_date(f"{job_date} {data[3]}")
            end = get_date(f"{job_date} {data[4]}")
            submitted_at = get_date(data[0])
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

    @classmethod
    def to_spreadsheet_row(cls, entry: "SpreadsheetEntry") -> list:
        return [
            entry.title,
            entry.start.isoformat(),
            entry.end.isoformat(),
        ]


SPREADSHEET_ID = "1xqBjVJxNfW_U6Bg5sbtc6PlALxdQKt1oSiUMBZ_xPRA"
READ_RANGE = "Form responses 1!A2:F"


def get_submitions() -> list[SpreadsheetEntry]:
    """Fetches submissions from the Google Sheets API."""
    result = (
        SHEET_SERVICE.values().get(spreadsheetId=SPREADSHEET_ID, range=READ_RANGE).execute()
    )

    return [
        SpreadsheetEntry.from_row(row)
        for row in result.get("values", [])
        if SpreadsheetEntry.from_row(row) is not None
    ]


def clear_sheet(sheet_name: str) -> None:
    print(f"Clearing sheet: {sheet_name}")
    SHEET_SERVICE.values().clear(
        spreadsheetId=SPREADSHEET_ID,
        range=sheet_name + "!A1:Z",
        body={},
    ).execute()


def write_to_spreadsheet(rows: list, sheet_name: str) -> None:
    """Writes entries to the Google Sheets API."""
    body = {"values": rows}
    print(f"Writing {body} rows to spreadsheet...")
    SHEET_SERVICE.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=sheet_name + "!A1",
        valueInputOption="RAW",
        body=body,
    ).execute()
