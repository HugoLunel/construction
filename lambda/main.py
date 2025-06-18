from collections import defaultdict
from datetime import datetime, timedelta, timezone
from gcal import CALENDAR_ID, CalendarEvent, get_calendar_events
from spreadsheet import (
    SpreadsheetEntry,
    clear_sheet,
    get_submitions,
    write_to_spreadsheet,
)
from dataclasses import dataclass
from typing import Optional


@dataclass
class CombinedMapEntry:
    event: Optional[CalendarEvent] = None
    submission: Optional[SpreadsheetEntry] = None


CombinedMapKey = tuple[str, datetime, datetime]


def create_entry_key(
    email: str,
    start: datetime,
    end: datetime,
) -> CombinedMapKey:
    return (email, start, end)


def combine_calendar_and_spreadsheet(
    events: list[CalendarEvent],
    submissions: list[SpreadsheetEntry],
) -> dict[CombinedMapKey, CombinedMapEntry]:
    combined_map: dict[CombinedMapKey, CombinedMapEntry] = defaultdict(CombinedMapEntry)

    for event in events:
        for attendee in event.attendees:
            # responseStatus = attendee.get("responseStatus") // TODO: might need to use this to know if an employee accepted the work
            # email = attendee.get("email") // TODO: might need to use email later on to match with email submissions
            email = attendee.get("displayName")
            if email and "Machine" not in attendee.get("displayName"):
                key = create_entry_key(email, event.start, event.end)
                combined_map[key].event = event

    for submission in submissions:
        email = submission.submitter
        if email:
            key = create_entry_key(email, submission.start, submission.end)
            combined_map[key].submission = submission

    return combined_map


def find_discrepancies(
    combined_map: dict[CombinedMapKey, CombinedMapEntry],
) -> tuple[dict[str, list[CalendarEvent]], dict[str, list[SpreadsheetEntry]]]:
    unmatched_events_by_employee = defaultdict(list[CalendarEvent])
    unmatched_submissions_by_employee = defaultdict(list[SpreadsheetEntry])
    for key, entry in combined_map.items():
        email, _start, _end = key

        is_submission_missing = entry.event and not entry.submission
        if is_submission_missing:
            unmatched_events_by_employee[email].append(entry.event)
            continue

        is_extra_submission = entry.submission and not entry.event
        if is_extra_submission:
            unmatched_submissions_by_employee[email].append(entry.submission)
            continue

    return unmatched_events_by_employee, unmatched_submissions_by_employee


def handler(event, context):
    events = get_calendar_events(
        calendar_id=CALENDAR_ID,
        time_min=(datetime.now(tz=timezone.utc) - timedelta(days=15)).isoformat(),
        time_max=(datetime.now(tz=timezone.utc) + timedelta(days=15)).isoformat(),
    )
    # events_by_employee = defaultdict(CalendarEvent)
    # for event in events:
    #     for attendee in event.attendees:
    #         email = attendee.get("email")
    #         if email:
    #             events_by_employee[email] = event

    submissions = get_submitions()
    # submissions_by_employee = defaultdict(SpreadsheetEntry)
    # for submission in submissions:
    #     email = submission.submitter
    #     if email:
    #         submissions_by_employee[email] = submission

    combined_map = combine_calendar_and_spreadsheet(events, submissions)
    unmatched_events_by_employee, unmatched_submissions_by_employee = (
        find_discrepancies(combined_map)
    )

    HEADER = ["Employee", "Title", "Start", "End"]

    sheet_name1 = "missing_submission"
    clear_sheet(sheet_name1)
    print("Unmatched Events by Employee:")
    for email, events in unmatched_events_by_employee.items():
        print(f"{email}: {len(events)} unmatched events")
        write_to_spreadsheet(
            rows=(
                [HEADER]
                + [
                    [email] + CalendarEvent.to_spreadsheet_row(event)
                    for event in events
                ]
            ),
            sheet_name=sheet_name1,
        )

    sheet_name2 = "extra_submission"
    clear_sheet(sheet_name2)
    print("\nUnmatched Submissions by Employee:")
    for email, submissions in unmatched_submissions_by_employee.items():
        print(f"{email}: {len(submissions)} unmatched submissions")
        write_to_spreadsheet(
            rows=(
                [HEADER]
                + [
                    [email] + SpreadsheetEntry.to_spreadsheet_row(submission)
                    for submission in submissions
                ]
            ),
            sheet_name=sheet_name2,
        )
