from dataclasses import dataclass
from datetime import datetime
from google_service import CALENDAR_SERVICE


CALENDAR_ID = "12b4c1c05ddfa92da3773151b5a3d2712138c410162cf0dcab3b4d0f84ecfe67@group.calendar.google.com"


def get_date(data: dict, key: str) -> datetime:
    date_dict = data.get(key, {})
    if not date_dict:
        raise ValueError(f"Missing date key: {key} in data: {data}")
    date_value = date_dict.get("dateTime") or date_dict.get("date")
    if not date_value:
        raise ValueError(f"Missing date value for key: {key} in data: {data}")
    return datetime.fromisoformat(date_value)


@dataclass
class CalendarEvent:
    title: str
    start: datetime
    end: datetime
    attendees: list[dict]
    location: str
    html_link: str
    created: datetime
    updated: datetime
    duration_hours: float

    @classmethod
    def from_dict(cls, data: dict) -> "CalendarEvent":
        start = get_date(data, "start")
        end = get_date(data, "end")
        return cls(
            title=data.get("summary", ""),
            start=start,
            end=end,
            attendees=data.get("attendees", []),
            location=data.get("location", ""),
            html_link=data.get("htmlLink", ""),
            created=datetime.fromisoformat(
                data.get("created", "").replace("Z", "+00:00")
            ),
            updated=datetime.fromisoformat(
                data.get("updated", "").replace("Z", "+00:00")
            ),
            duration_hours=(end - start).total_seconds() / 3600,
        )

    @classmethod
    def to_spreadsheet_row(cls, event: "CalendarEvent") -> list:
        return [
            event.title,
            event.start.isoformat(),
            event.end.isoformat(),
        ]


def get_calendar_events(
    calendar_id: str, time_min: str, time_max: str
) -> list[CalendarEvent]:
    events_result = (
        CALENDAR_SERVICE.events()
        .list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    return [CalendarEvent.from_dict(event) for event in events_result.get("items", [])]


# Get events from the past 15 days
# events = get_calendar_events(
#     calendar_id=CALENDAR_ID,
#     time_min=(datetime.now(tz=timezone.utc) - timedelta(days=15)).isoformat(),
#     time_max=(datetime.now(tz=timezone.utc) + timedelta(days=15)).isoformat(),
# )

# employee_times = defaultdict(float)

# for event in events:

#     for attendee in event.attendees:
#         name = attendee.get("displayName")
#         if name:
#             employee_times[name] += event.duration_hours

# # Print total working time per employee
# for name, hours in employee_times.items():
#     print(f"{name}: {hours:.2f} hours")
