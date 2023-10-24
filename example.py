import sfu_api_wrapper
import asyncio
import google_calendar_com
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime, timedelta
from enum import Enum



#map sfu api days strings to google calendar api indices
days_mapping = {
    'Mo': 0,
    'Tu': 1,
    'We': 2,
    'Th': 3,
    'Fr': 4,
    'Sa': 5,
    'Su': 6
}
month_mapping = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}

class CustomDaysOfWeek(Enum):
    MO = 0
    TU = 1
    WE = 2
    TH = 3
    FR = 4
    SA = 5
    SU = 6
    
async def main():
    data = await sfu_api_wrapper.course_offering('cmpt', '120', 'd100')
    print(data.instructors[0].name)


    #the schedule is the same regardless of the day
    start_date = data.course_schedule[0].start_date
    end_date = data.course_schedule[0].end_date
    
    days = [sched.days for sched in data.course_schedule]
    start_time = [sched.start_time for sched in data.course_schedule]
    end_time = [sched.start_time for sched in data.course_schedule]

    print(start_date)
    print(end_date)

    print(days)
    print(start_time)
    print(end_time)



if __name__ == '__main__':
    #asyncio.run(main())
    pass





 # Define event details.
start_date = datetime(2023, 9, 6)  # Start date (Wed Sep 06 00:00:00 PDT 2023)
end_date = datetime(2023, 9, 20)   # End date (Tue Dec 05 00:00:00 PST 2023)
time_zone = 'America/Los_Angeles'  # Time zone for your location

desired_days = [CustomDaysOfWeek.MO, CustomDaysOfWeek.TU, CustomDaysOfWeek.WE]
start_times = ['12:30', '12:30', '12:30']
end_times = ['14:20', '14:20', '13:20']

# Replace with your Google Calendar API credentials file (JSON)
credentials_file = 'banded-object-402902-339fe70621d4.json'

# Define the calendar ID (can be your primary calendar or a specific calendar)
calendar_id = 'klitvin101@gmail.com'

# Function to create a Google Calendar event.
def create_event(start_datetime, end_datetime):
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file, scopes=['https://www.googleapis.com/auth/calendar']
    )
    service = build('calendar', 'v3', credentials=credentials)

    event = {
        'summary': 'Event Title',
        'description': 'Event Description',
        'start': {
            'dateTime': start_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': time_zone,
        },
        'end': {
            'dateTime': end_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': time_zone,
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    service.events().insert(calendarId=calendar_id, body=event).execute()

# Create events for the specified date range, days of the week, and times.
current_date = start_date
while current_date <= end_date:
    if CustomDaysOfWeek(current_date.weekday()) in desired_days:
        day_index = desired_days.index(CustomDaysOfWeek(current_date.weekday()))
        start_time = start_times[day_index]
        end_time = end_times[day_index]
        start_datetime = datetime(current_date.year, current_date.month, current_date.day, int(start_time.split(':')[0]), int(start_time.split(':')[1]))
        end_datetime = datetime(current_date.year, current_date.month, current_date.day, int(end_time.split(':')[0]), int(end_time.split(':')[1]))
        create_event(start_datetime, end_datetime)
    current_date += timedelta(days=1)