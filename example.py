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
    'Mon': 0,
    'Tu': 1,
    'Tue':1,
    'We': 2,
    'Wed':2,
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

def split_day(date: str):
    split_date = date.split(" ")
    month = split_date[1]
    day = split_date[2]
    year = split_date[5] 
    date_time_args = (int(year), month_mapping[month], int(day))

    return date_time_args
    
async def add_course_schedule_to_caledar():
    data = await sfu_api_wrapper.course_offering('cmpt', '120', 'd100')  

    start_dates = [datetime(*split_day(sched.start_date)) for sched in data.course_schedule]
    end_dates = [datetime(*split_day(sched.end_date)) for sched in data.course_schedule]
    desired_days = [CustomDaysOfWeek(days_mapping[sched.days]) for sched in data.course_schedule]
    start_times = [sched.start_time for sched in data.course_schedule]
    end_times = [sched.end_time for sched in data.course_schedule]

    
    time_zone = 'America/Los_Angeles'  # Time zone for your location

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
            'summary': 'CMPT 120',
            'description': 'Lecture',
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

    # #Writes the data for the midterms, lectures, and labs
    # for (start_date, end_date) in list(zip(start_dates, end_dates)):
    for index in range(len(start_dates)):
        end_date = datetime(2023,10,11)
        current_date = start_dates[index]

        while current_date <= end_date:
            if CustomDaysOfWeek(current_date.weekday()) == desired_days[index]:
                # day_index = desired_days.index(CustomDaysOfWeek(current_date.weekday()))
                start_time = start_times[index]
                end_time = end_times[index]
                start_datetime = datetime(current_date.year, current_date.month, current_date.day, int(start_time.split(':')[0]), int(start_time.split(':')[1]))
                end_datetime = datetime(current_date.year, current_date.month, current_date.day, int(end_time.split(':')[0]), int(end_time.split(':')[1]))
                create_event(start_datetime, end_datetime)
            current_date += timedelta(days=1)


if __name__ == '__main__':
    asyncio.run(add_course_schedule_to_caledar())





