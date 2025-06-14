from collections import defaultdict
from datetime import datetime, timedelta, timezone
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
]
SERVICE_ACCOUNT_FILE = "service_account.json"
CALENDAR_ID = "12b4c1c05ddfa92da3773151b5a3d2712138c410162cf0dcab3b4d0f84ecfe67@group.calendar.google.com"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build("calendar", "v3", credentials=credentials)

# events_result = service.events().list(calendarId=CALENDAR_ID).execute()
# events = events_result.get("items", [])

# attendees_list = [event.get("attendees") for event in events]
# print(attendees_list)


def get_calendar_events(calendar_id: str, time_min: str, time_max: str):
    """Retrieve events from a specific calendar within a time range."""
    events_result = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    return events_result.get("items", [])

# Get events from the past 15 days
events = get_calendar_events(
  calendar_id=CALENDAR_ID,
  time_min=(datetime.now(tz=timezone.utc) - timedelta(days=15)).isoformat(),
time_max=(datetime.now(tz=timezone.utc) + timedelta(days=15)).isoformat(),
)

employee_times = defaultdict(float)

for event in events:
  event["start"]
  # Parse start and end times as datetime objects
  start_str = event["start"].get("dateTime", event["start"].get("date"))
  end_str = event["end"].get("dateTime", event["end"].get("date"))
  start = datetime.fromisoformat(start_str)
  end = datetime.fromisoformat(end_str)

  duration_hours = (end - start).total_seconds() / 3600

  attendees = event.get("attendees", [])
  for attendee in attendees:
    name = attendee.get('displayName')
    if name:
      employee_times[name] += duration_hours

# Print total working time per employee
for name, hours in employee_times.items():
  print(f"{name}: {hours:.2f} hours")

