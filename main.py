from collections import defaultdict
from datetime import datetime, timedelta, timezone
from gcal import CALENDAR_ID, CalendarEvent, get_calendar_events
from spreadsheet import SpreadsheetEntry, get_submitions
from dataclasses import dataclass
from typing import Optional


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


@dataclass
class EventSubmissionEntry:
    event: Optional[CalendarEvent] = None
    submission: Optional[SpreadsheetEntry] = None


def create_entry_key(
    email: str, start: datetime, end: datetime
) -> tuple[str, float, float]:
    return (email, start.timestamp(), end.timestamp)


def find_unmatched_events_and_submissions(
    events: list[CalendarEvent], submissions: list[SpreadsheetEntry]
) -> tuple[dict[str, list[CalendarEvent]], dict[str, list[SpreadsheetEntry]]]:
    # key: (email, start, end) -> EventSubmissionEntry
    combined_map = defaultdict(EventSubmissionEntry)

    for event in events:
        for attendee in event.attendees:
            email = attendee.get("email")
            if email:
                key = create_entry_key(email, event.start, event.end)
                combined_map[key].event = event

    for submission in submissions:
        email = submission.submitter
        if email:
            key = create_entry_key(email, submission.start, submission.end)
            combined_map[key].submission = submission

    unmatched_events_by_employee = defaultdict(list[CalendarEvent])
    unmatched_submissions_by_employee = defaultdict(list[SpreadsheetEntry])
    for key, entry in combined_map.items():
        email, _start, _end = key
        if entry.event and not entry.submission:
            unmatched_events_by_employee[email].append(entry.event)
        if entry.submission and not entry.event:
            unmatched_submissions_by_employee[email].append(entry.submission)

    return unmatched_events_by_employee, unmatched_submissions_by_employee


unmatched_events_by_employee, unmatched_submissions_by_employee = (
    find_unmatched_events_and_submissions(events, submissions)
)

print("Unmatched Events by Employee:")
for email, events in unmatched_events_by_employee.items():
    print(f"{email}: {len(events)} unmatched events")
    for event in events:
        print(f"  - {event.title} ({event.start} to {event.end})")

print("\nUnmatched Submissions by Employee:")
for email, submissions in unmatched_submissions_by_employee.items():
    print(f"{email}: {len(submissions)} unmatched submissions")
    for submission in submissions:
        print(f"  - {submission.title} ({submission.start} to {submission.end})")
