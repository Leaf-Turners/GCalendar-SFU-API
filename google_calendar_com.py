from datetime import datetime
from pathlib import Path

from googleapiclient.discovery import build
from google.oauth2 import service_account

# Replace with your Google Calendar API credentials file (JSON)
credentials_file = 'banded-object-402902-339fe70621d4.json'

# Define the calendar ID (can be your primary calendar or a specific calendar)
calendar_id = 'klitvin101@gmail.com'

# Function to create a Google Calendar event
def create_event(event_data):
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file, scopes=['https://www.googleapis.com/auth/calendar']
    )
    service = build('calendar', 'v3', credentials=credentials)

    event = service.events().insert(calendarId=calendar_id, body=event_data).execute()

    print(f'Event created: {event.get("htmlLink")}')

# Define event details with Pacific Time Zone
event_data = {
    'summary': 'Event Title',
    'description': 'Event Description',
    'start': {
        'dateTime': '2023-10-23T10:00:00-07:00',  # Pacific Time Zone (PST)
        'timeZone': 'America/Los_Angeles',  # Time zone identifier
    },
    'end': {
        'dateTime': '2023-10-23T12:00:00-07:00',  # Pacific Time Zone (PST)
        'timeZone': 'America/Los_Angeles',  # Time zone identifier
    },
    'reminders': {
        'useDefault': False,
        'overrides': [
            {'method': 'popup', 'minutes': 10},
        ],
    },
}

create_event(event_data)
    
