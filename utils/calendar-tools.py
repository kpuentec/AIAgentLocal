import os
import datetime as dt

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langchain_core.tools import tool

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_calendar_service():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except HttpError as error:
        print("Google Calendar Error:", error)
        return None


@tool
def add_calendar_event(summary: str, start: str, end: str, timezone: str = 'UTC') -> str:
    """
    Add an event to the user's Google Calendar.

    Args:
        summary: Title of the event
        start: Start datetime (format: YYYY-MM-DD HH:MM)
        end: End datetime (format: YYYY-MM-DD HH:MM)
        timezone: Timezone string (default: UTC)

    Returns:
        Confirmation message or error.
    """
    try:
        start_dt = dt.datetime.strptime(start, "%Y-%m-%d %H:%M")
        end_dt = dt.datetime.strptime(end, "%Y-%m-%d %H:%M")
        service = get_calendar_service()
        if not service:
            return "Failed to connect to Google Calendar."

        event = {
            'summary': summary,
            'start': {'dateTime': start_dt.isoformat(), 'timeZone': timezone},
            'end': {'dateTime': end_dt.isoformat(), 'timeZone': timezone},
        }

        created_event = service.events().insert(calendarId='primary', body=event).execute()
        return f"Event created: {created_event.get('htmlLink')}"

    except Exception as e:
        return f"Failed to create event: {str(e)}"